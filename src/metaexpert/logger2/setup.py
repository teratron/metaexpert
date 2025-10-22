"""Setup and configuration for structlog in MetaExpert."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

import structlog

from .config import LoggerConfig
from .formatters import get_console_renderer, get_file_renderer
from .processors import (
    ErrorEventEnricher,
    TradeEventFilter,
    add_app_context,
    add_process_info,
    rename_event_key,
)


def configure_stdlib_logging(config: LoggerConfig) -> None:
    """Configure standard library logging."""
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Add console handler
    if config.log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(config.log_level)
        root_logger.addHandler(console_handler)

    # Add file handlers
    if config.log_to_file:
        # Main log file
        main_handler = _create_rotating_handler(
            config.log_dir / config.log_file, config.max_bytes, config.backup_count
        )
        main_handler.setLevel(config.log_level)
        root_logger.addHandler(main_handler)

        # Trade log file (INFO and above)
        trade_handler = _create_rotating_handler(
            config.log_dir / config.trade_log_file,
            config.max_bytes,
            config.backup_count,
        )
        trade_handler.setLevel(logging.INFO)
        trade_handler.addFilter(_TradeLogFilter())
        root_logger.addHandler(trade_handler)

        # Error log file (ERROR and above)
        error_handler = _create_rotating_handler(
            config.log_dir / config.error_log_file,
            config.max_bytes,
            config.backup_count,
        )
        error_handler.setLevel(logging.ERROR)
        root_logger.addHandler(error_handler)


def _create_rotating_handler(
    filepath: Path, max_bytes: int, backup_count: int
) -> logging.handlers.RotatingFileHandler:
    """Create a rotating file handler."""
    handler = logging.handlers.RotatingFileHandler(
        filepath, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    return handler


class _TradeLogFilter(logging.Filter):
    """Filter to include only trade-related events."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Check if record is a trade event."""
        return hasattr(record, "_trade_event") and record._trade_event


def get_processors(config: LoggerConfig) -> list[Any]:
    """Get list of processors based on configuration."""
    processors = [
        # Add contextvars for context management
        structlog.contextvars.merge_contextvars,
        # Add custom context
        add_app_context,
        # Add log level filtering
        structlog.stdlib.filter_by_level,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Add log level
        structlog.stdlib.add_log_level,
        # Process positional arguments
        structlog.stdlib.PositionalArgumentsFormatter(),
        # Add timestamp
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        # Add call site info (file, line, function)
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            }
        ),
        # Add custom processors
        TradeEventFilter(),
        ErrorEventEnricher(),
        # Add process/thread info for debugging
        # add_process_info,  # Uncomment if needed
        # Stack info renderer
        structlog.processors.StackInfoRenderer(),
        # Format exceptions
        structlog.processors.format_exc_info,
        # Unicode decoder
        structlog.processors.UnicodeDecoder(),
        # Rename event key
        rename_event_key,
    ]

    # Add final renderer based on destination
    if config.log_to_console and not config.json_logs:
        # Console with colors
        processors.append(get_console_renderer(config.use_colors))
    elif config.json_logs:
        # JSON for structured logging
        processors.append(structlog.processors.JSONRenderer())
    else:
        # Logfmt for files
        processors.append(get_file_renderer(config.json_logs))

    # Add ProcessorFormatter for stdlib integration
    processors.append(structlog.stdlib.ProcessorFormatter.wrap_for_formatter)

    return processors


def setup_logging(config: LoggerConfig) -> None:
    """Setup complete logging system with structlog."""
    # Configure stdlib logging first
    configure_stdlib_logging(config)

    # Configure structlog
    structlog.configure(
        processors=get_processors(config),
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=config.cache_logger_on_first_use,
    )

    # Configure stdlib formatter to use structlog processors
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=get_file_renderer(config.json_logs),
        foreign_pre_chain=get_processors(config),
    )

    # Apply formatter to all handlers
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)
