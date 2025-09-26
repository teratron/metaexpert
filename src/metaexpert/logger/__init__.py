"""
MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

from logging import Logger
from typing import Any


class MetaLogger(Logger):
    """
    MetaLogger class for enhanced logging functionality.

    This class extends the standard Python Logger to provide MetaExpert-specific
    logging features including structured logging, asynchronous logging, and
    specialized handlers for different types of log messages.
    """

    def __init__(
        self,
        log_level: str = "INFO",
        log_file: str = "expert.log",
        trade_log_file: str = "trades.log",
        error_log_file: str = "errors.log",
        log_to_console: bool = True,
        structured_logging: bool = False,
        async_logging: bool = False
    ) -> None:
        """
        Initialize the MetaLogger with enhanced configuration.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            log_to_console: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
        """
        # Configure the logging system using the LogManager
        log_manager.configure(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_to_console=log_to_console,
            structured_logging=structured_logging,
            async_logging=async_logging,
            log_directory=log_directory,
            max_file_size=LogConfig.get_max_file_size(),
            backup_count=LogConfig.get_backup_count(),
        )

        # Initialize the Logger with the application name
        super().__init__(LogConfig.LOG_NAME)

    def get_trade_logger(self) -> Logger:
        """Get the trade-specific logger."""
        return log_manager.get_trade_logger()

    def get_error_logger(self) -> Logger:
        """Get the error-specific logger."""
        return log_manager.get_error_logger()

    def log_trade(self, message: str, **kwargs) -> None:
        """Log a trade-related message.

        Args:
            message: Log message
            **kwargs: Additional trade context data
        """
        log_manager.log_trade(message, **kwargs)

    def log_error(
        self, message: str, exception: Exception | None = None, **kwargs
    ) -> None:
        """Log an error message with context.

        Args:
            message: Error message
            exception: Exception object if available
            **kwargs: Additional error context data
        """
        log_manager.log_error(message, exception=exception, **kwargs)

