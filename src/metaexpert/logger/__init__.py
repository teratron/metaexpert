"""Logger module.

This module provides enhanced logging functionality for the trading bot,
including structured logging, asynchronous logging, and centralized configuration.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.config import LOG_NAME
from metaexpert.logger.formatter import LogFormatter

from . import config as logger_config_module


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance.
    This is a simple wrapper around logging.getLogger.
    """
    return logging.getLogger(name or LOG_NAME)


def _create_formatter(use_structured: bool, log_format: str) -> logging.Formatter:
    """Create a log formatter."""
    if use_structured:
        return LogFormatter()
    return logging.Formatter(log_format)


def _create_console_handler() -> logging.StreamHandler:
    """Create a console log handler."""
    return logging.StreamHandler(sys.stdout)


def _create_file_handler(handler_config: dict[str, Any]) -> logging.Handler | None:
    """Create a rotating file log handler."""
    filename = handler_config.get("filename")
    if not filename:
        return None

    log_dir = Path(logger_config_module.LOG_DIRECTORY)
    log_dir.mkdir(exist_ok=True)
    filepath = log_dir / filename

    max_size = handler_config.get("max_size", 10 * 1024 * 1024)  # 10MB
    backup_count = handler_config.get("backup_count", 5)

    return logging.handlers.RotatingFileHandler(
        filepath, maxBytes=max_size, backupCount=backup_count, encoding="utf-8"
    )


def _create_handler(handler_config: dict[str, Any]) -> logging.Handler | None:
    """Factory function to create a handler from its config."""
    handler_type = handler_config.get("type")
    match handler_type:
        case "console":
            return _create_console_handler()
        case "file":
            return _create_file_handler(handler_config)
        case _:
            return None


def configure_logging(config: dict[str, Any]) -> dict[str, Any]:
    """
    Configure the centralized logging system based on a dictionary.
    """
    try:
        default_level = config.get("default_level", "INFO").upper()
        use_async = config.get("async_logging", False)
        use_structured = config.get("structured_logging", False)
        handler_configs = config.get("handlers", {})
        default_format = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(default_level)

        formatter = _create_formatter(use_structured, default_format)

        for name, handler_config in handler_configs.items():
            handler = _create_handler(handler_config)
            if not handler:
                continue

            handler_level = handler_config.get("level", default_level).upper()
            handler.setLevel(handler_level)
            handler.setFormatter(formatter)
            handler.name = name

            final_handler: logging.Handler = handler
            if use_async:
                final_handler = AsyncHandler(handler=handler)

            root_logger.addHandler(final_handler)

        return {"status": "success", "message": "Logging configured successfully."}

    except Exception as e:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s: (LOGGING-FALLBACK) %(message)s",
        )
        logging.error("Failed to configure logging: %s", e, exc_info=True)
        return {"status": "error", "message": f"Failed to configure logging: {e}"}


__all__ = ["configure_logging", "get_logger"]
