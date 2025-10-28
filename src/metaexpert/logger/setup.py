"""Setup and configuration for structlog in MetaExpert."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

import structlog

from metaexpert.logger.config import LoggerConfig
from metaexpert.logger.formatters import get_console_renderer, get_file_renderer
from metaexpert.logger.processors import (
    ErrorEventEnricher,
    PerformanceMonitor,
    SensitiveDataFilter,
    TradeEventFilter,
    add_app_context,
    rename_event_key,
)


class _TradeLogFilter(logging.Filter):
    """Filter to include only trade-related events."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Check if record is a trade event."""
        return getattr(record, "_trade_event", False)


def configure_stdlib_logging(config: LoggerConfig) -> None:
    """Configure standard library logging."""
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Get processors once
    processors = get_processors(config)

    # Add console handler with proper formatting
    if config.log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(config.log_level)

        console_formatter = structlog.stdlib.ProcessorFormatter(
            processor=get_console_renderer(colors=config.use_colors),
            foreign_pre_chain=processors,
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    # Add file handlers
    if config.log_to_file:
        # File formatter (shared)
        file_formatter = structlog.stdlib.ProcessorFormatter(
            processor=get_file_renderer(config.json_logs),
            foreign_pre_chain=processors,
        )

        # Main log file
        main_handler = _create_rotating_handler(
            config.log_dir / config.log_file, config.max_bytes, config.backup_count
        )
        main_handler.setLevel(config.log_level)
        main_handler.setFormatter(file_formatter)
        root_logger.addHandler(main_handler)

        # Trade log file (INFO and above)
        trade_handler = _create_rotating_handler(
            config.log_dir / config.trade_log_file,
            config.max_bytes,
            config.backup_count,
        )
        trade_handler.setLevel(logging.INFO)
        trade_handler.addFilter(_TradeLogFilter())
        trade_handler.setFormatter(file_formatter)
        root_logger.addHandler(trade_handler)

        # Error log file (ERROR and above)
        error_handler = _create_rotating_handler(
            config.log_dir / config.error_log_file,
            config.max_bytes,
            config.backup_count,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)


def _create_rotating_handler(
    filepath: Path, max_bytes: int, backup_count: int
) -> logging.handlers.RotatingFileHandler:
    """Create a rotating file handler."""
    handler = logging.handlers.RotatingFileHandler(
        filepath, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    return handler


def get_processors(config: LoggerConfig) -> list[Any]:
    """Get list of processors based on configuration."""
    processors = [
        # Add contextvars for context management
        structlog.contextvars.merge_contextvars,
        # Добавляем SensitiveDataFilter ПЕРВЫМ для безопасности
        SensitiveDataFilter(),
        # Add custom context
        add_app_context,
        # Add log level filtering
        structlog.stdlib.filter_by_level,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Add log level
        structlog.stdlib.add_log_level,
        # Add timestamp
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        # Add call site info (file, line, function)
        structlog.processors.CallsiteParameterAdder(
            frozenset(
                [
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            )
        ),
        # Add custom processors
        TradeEventFilter(),
        ErrorEventEnricher(),
        # Добавляем PerformanceMonitor
        PerformanceMonitor(threshold_ms=100.0),
        # Stack info renderer
        structlog.processors.StackInfoRenderer(),
        # Format exceptions
        structlog.processors.format_exc_info,
        # Unicode decoder
        structlog.processors.UnicodeDecoder(),
        # Rename event key
        rename_event_key,
    ]

    return processors


def setup_logging(config: LoggerConfig) -> None:
    """Setup complete logging system with structlog.

    Thread-safe and can be called multiple times safely.
    First call configures structlog, subsequent calls only update handlers.
    """
    # Reconfiguration protection
    if structlog.is_configured():
        # Recreate stdlib handlers, but don't reconfigure structlog
        configure_stdlib_logging(config)
        return

    # Configure stdlib logging first
    configure_stdlib_logging(config)

    # Configure structlog
    structlog.configure(
        processors=[
            *get_processors(config),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=config.cache_logger_on_first_use,
    )
