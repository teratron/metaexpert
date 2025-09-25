"""Enhanced Logger module for MetaExpert trading system.

This module provides comprehensive logging functionality including:
- Multiple specialized loggers (main, trade, error)
- Asynchronous and synchronous logging
- Structured JSON logging
- Rotating file handlers
- Console output with different levels
- Environment-based configuration
- Template parameter support

Usage:
    # Simple usage with default configuration
    from metaexpert.logger import get_logger
    logger = get_logger()
    logger.info("Application started")

    # Advanced usage with LogManager
    from metaexpert.logger import log_manager
    log_manager.configure(
        log_level="DEBUG",
        structured_logging=True,
        async_logging=True
    )

    # Specialized loggers
    trade_logger = log_manager.get_trade_logger()
    error_logger = log_manager.get_error_logger()

    # Convenience methods
    log_manager.log_trade("Order executed", symbol="BTCUSDT", price=50000)
    log_manager.log_error("Connection failed", exception=some_exception)
"""

import logging
from typing import Any

from metaexpert.logger.async_handler import AsyncHandler

# Configuration imports
from metaexpert.logger.config import (
    ASYNC_LOGGING_ENABLED,
    DEFAULT_LOG_FILE_PATH,
    LOG_BACKUP_COUNT,
    LOG_DIRECTORY,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_SIZE,
    LOG_NAME,
    STRUCTURED_LOGGING_ENABLED,
    LoggingConfig,
)
from metaexpert.logger.formatter import (
    ErrorFormatter,
    MainFormatter,
    TradeFormatter,
)

# Integration imports
from metaexpert.logger.integration import (
    configure_logging as configure_expert_logging,
)
from metaexpert.logger.integration import (
    create_handlers_config,
    get_logger_config,
    log_expert_error,
    log_expert_shutdown,
    log_expert_startup,
    log_trade_execution,
    validate_logging_params,
)

# Core components
from metaexpert.logger.manager import LogManager, log_manager


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get a logger instance with enhanced functionality.

    This function provides backward compatibility while leveraging
    the new LogManager system when available.

    Args:
        name: Logger name. If None, uses the configured LOG_NAME.
              Special names: 'trade', 'error' return specialized loggers.

    Returns:
        Logger instance
    """
    if name in ("trade", "error", "main"):
        return log_manager.get_logger(name)

    return logging.getLogger(name or LOG_NAME)


def get_main_logger() -> logging.Logger:
    """Get the main application logger."""
    return log_manager.get_main_logger()


def get_trade_logger() -> logging.Logger:
    """Get the trade-specific logger."""
    return log_manager.get_trade_logger()


def get_error_logger() -> logging.Logger:
    """Get the error-specific logger."""
    return log_manager.get_error_logger()


def configure_logging(config: dict[str, Any]) -> dict[str, Any]:
    """
    Configure the enhanced logging system.

    This function maintains backward compatibility with the original
    configure_logging function while providing enhanced functionality.

    Args:
        config: Configuration dictionary with logging settings

    Returns:
        Configuration result with status and message
    """
    # Extract configuration parameters
    log_level = config.get("default_level", "INFO")
    async_logging = config.get("async_logging", False)
    structured_logging = config.get("structured_logging", False)
    handlers_config = config.get("handlers", {})

    # Determine file names from handlers config
    log_file = "expert.log"
    trade_log_file = "trades.log"
    error_log_file = "errors.log"
    log_to_console = False

    # Parse handlers configuration
    for name, handler_config in handlers_config.items():
        if handler_config.get("type") == "file":
            filename = handler_config.get("filename", "")
            if "trade" in name.lower():
                trade_log_file = filename
            elif "error" in name.lower():
                error_log_file = filename
            else:
                log_file = filename
        elif handler_config.get("type") == "console":
            log_to_console = True

    # Configure using LogManager
    return log_manager.configure(
        log_level=log_level,
        log_file=log_file,
        trade_log_file=trade_log_file,
        error_log_file=error_log_file,
        log_to_console=log_to_console,
        structured_logging=structured_logging,
        async_logging=async_logging,
    )


def configure_from_template_params(
    log_level: str = "INFO",
    log_file: str = "expert.log",
    trade_log_file: str = "trades.log",
    error_log_file: str = "errors.log",
    log_to_console: bool = True,
    structured_logging: bool = False,
    async_logging: bool = False,
) -> dict[str, Any]:
    """
    Configure logging using template parameters (as used in MetaExpert.__init__).

    This function provides a direct interface for the parameters used
    in the template.py file and MetaExpert class initialization.

    Args:
        log_level: Logging level
        log_file: Main log file name
        trade_log_file: Trade-specific log file name
        error_log_file: Error-specific log file name
        log_to_console: Whether to output logs to console
        structured_logging: Whether to use JSON structured logging
        async_logging: Whether to use asynchronous logging

    Returns:
        Configuration result with status and message
    """
    return configure_expert_logging(
        log_level=log_level,
        log_file=log_file,
        trade_log_file=trade_log_file,
        error_log_file=error_log_file,
        log_to_console=log_to_console,
        structured_logging=structured_logging,
        async_logging=async_logging,
    )


def log_trade(message: str, **kwargs) -> None:
    """
    Convenience function to log trade-related messages.

    Args:
        message: Log message
        **kwargs: Additional context data
    """
    log_manager.log_trade(message, **kwargs)


def log_error(message: str, exception: Exception | None = None, **kwargs) -> None:
    """
    Convenience function to log error messages.

    Args:
        message: Error message
        exception: Exception object if available
        **kwargs: Additional context data
    """
    log_manager.log_error(message, exception, **kwargs)


def shutdown_logging() -> None:
    """Shutdown the logging system and clean up resources."""
    log_manager.shutdown()


# Legacy compatibility functions
# Legacy helper functions - kept for backward compatibility
def _create_formatter(use_structured: bool, log_format: str) -> logging.Formatter:
    """Legacy formatter creation function."""
    if use_structured:
        return MainFormatter()
    return logging.Formatter(log_format)


def _create_console_handler() -> logging.StreamHandler:
    """Legacy console handler creation function."""
    return logging.StreamHandler()


def _create_file_handler(handler_config: dict[str, Any]) -> logging.Handler | None:
    """Legacy file handler creation function."""
    filename = handler_config.get("filename")
    if not filename:
        return None

    import logging.handlers
    from pathlib import Path

    log_dir = Path(LOG_DIRECTORY)
    log_dir.mkdir(exist_ok=True)
    filepath = log_dir / filename

    max_size = handler_config.get("max_size", LOG_MAX_SIZE)
    backup_count = handler_config.get("backup_count", LOG_BACKUP_COUNT)

    return logging.handlers.RotatingFileHandler(
        filepath, maxBytes=max_size, backupCount=backup_count, encoding="utf-8"
    )


# Export all public components
__all__ = [
    #
    # --- Configuration constants ---
    "ASYNC_LOGGING_ENABLED",
    "DEFAULT_LOG_FILE_PATH",
    "LOG_BACKUP_COUNT",
    "LOG_DIRECTORY",
    "LOG_FILE",
    "LOG_FORMAT",
    "LOG_LEVEL",
    "LOG_MAX_SIZE",
    "LOG_NAME",
    "STRUCTURED_LOGGING_ENABLED",
    #
    # --- Classes ---
    "AsyncHandler",
    "ErrorFormatter",
    "LogManager",
    "LoggingConfig",
    "MainFormatter",
    "TradeFormatter",
    #
    # --- Main functions ---
    "configure_expert_logging",
    "configure_from_template_params",
    "configure_logging",
    #
    # --- Integration functions ---
    "create_handlers_config",
    "get_error_logger",
    "get_logger",
    "get_logger_config",
    "get_main_logger",
    "get_trade_logger",
    "log_error",
    "log_expert_error",
    "log_expert_shutdown",
    "log_expert_startup",
    #
    # --- Global instances ---
    "log_manager",
    "log_trade",
    "log_trade_execution",
    "shutdown_logging",
    "validate_logging_params",
]
