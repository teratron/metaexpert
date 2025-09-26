"""
MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

from logging import Logger
from typing import Any

from metaexpert.logger.config import LOG_BACKUP_COUNT, LOG_DIRECTORY, LOG_MAX_FILE_SIZE, LOG_NAME


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
        self.log_level = log_level,
        self.log_file = log_file,
        self.trade_log_file = trade_log_file,
        self.error_log_file = error_log_file,
        self.log_to_console = log_to_console,
        self.structured_logging = structured_logging,
        self.async_logging = async_logging,
        self.log_directory = LOG_DIRECTORY,
        self.max_file_size = LOG_MAX_FILE_SIZE,
        self.backup_count = LOG_BACKUP_COUNT,

        # Initialize the Logger with the application name
        super().__init__(LOG_NAME)


