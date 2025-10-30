"""Setup and configuration for structlog in MetaExpert."""

import logging
import logging.handlers
import sys
import threading
import weakref
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
        # Добавляем SensitiveDataFilter ПЕРВЫМ для безопасности
        SensitiveDataFilter(),
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
        # Add PerformanceMonitor
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


# Global state for thread-safe reconfiguration
_setup_lock = threading.Lock()
_current_config: LoggerConfig | None = None
# Track our handlers using WeakSet to avoid memory leaks
_our_handlers = weakref.WeakSet()


def setup_logging(config: LoggerConfig) -> None:
    """Setup complete logging system with structlog.

    Thread-safe and can be called multiple times safely.
    First call configures structlog, subsequent calls only update handlers.
    """
    global _current_config

    with _setup_lock:  # Thread-safety protection
        try:
            # Always configure stdlib logging first (avoids duplication)
            _configure_stdlib_logging_safely(config)

            # Check if structlog is already configured
            if structlog.is_configured():
                # If config changed, reconfigure structlog completely
                if _current_config is not None and _current_config != config:
                    _reconfigure_structlog(config)
                return

            # Initial structlog configuration
            structlog.configure(
                processors=[
                    *get_processors(config),
                    structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
                ],
                context_class=dict,
                logger_factory=structlog.stdlib.LoggerFactory(),
                wrapper_class=structlog.stdlib.BoundLogger,
                cache_logger_on_first_use=config.cache_logger_on_first_use,
            )

            _current_config = config

        except Exception as e:
            # Log error but don't crash - setup basic logging as fallback
            logging.error(f"Failed to setup advanced logging: {e}")
            _setup_basic_logging()


def _configure_stdlib_logging_safely(config: LoggerConfig) -> None:
    """Configure stdlib logging while preserving other components' handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(config.log_level)

    # Preserve handlers from other components
    existing_handlers = [
        handler for handler in root_logger.handlers if handler not in _our_handlers
    ]

    # Remove only our handlers
    root_logger.handlers = [
        handler for handler in root_logger.handlers if handler in _our_handlers
    ]

    # Add our handlers
    _add_handlers(config)

    # Restore other components' handlers
    root_logger.handlers.extend(existing_handlers)


def _add_handlers(config: LoggerConfig) -> None:
    """Add MetaExpert handlers and track them in WeakSet."""
    processors = get_processors(config)

    # Console handler
    if config.log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(config.log_level)

        console_formatter = structlog.stdlib.ProcessorFormatter(
            processor=get_console_renderer(colors=config.use_colors),
            foreign_pre_chain=processors,
        )
        console_handler.setFormatter(console_formatter)
        logging.getLogger().addHandler(console_handler)
        _our_handlers.add(console_handler)  # Track our handler

    # File handlers
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
        logging.getLogger().addHandler(main_handler)
        _our_handlers.add(main_handler)

        # Trade log file (INFO and above)
        trade_handler = _create_rotating_handler(
            config.log_dir / config.trade_log_file,
            config.max_bytes,
            config.backup_count,
        )
        trade_handler.setLevel(logging.INFO)
        trade_handler.addFilter(_TradeLogFilter())
        trade_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(trade_handler)
        _our_handlers.add(trade_handler)

        # Error log file (ERROR and above)
        error_handler = _create_rotating_handler(
            config.log_dir / config.error_log_file,
            config.max_bytes,
            config.backup_count,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(error_handler)
        _our_handlers.add(error_handler)


def _reconfigure_structlog(config: LoggerConfig) -> None:
    """Reconfigure structlog when config changes."""
    # Reset structlog to allow reconfiguration
    structlog.reset_defaults()

    # Reconfigure with new settings
    structlog.configure(
        processors=[
            *get_processors(config),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=config.cache_logger_on_first_use,
    )


def _setup_basic_logging() -> None:
    """Setup basic logging as fallback when advanced setup fails."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")
