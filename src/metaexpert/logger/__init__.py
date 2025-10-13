""""""

import logging

import structlog

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_DETAILED_FORMAT,
    LOG_DIRECTORY,
    LOG_ERROR_LEVEL,
    LOG_FALLBACK_FORMAT,
    LOG_FORMAT,
    LOG_MAX_FILE_SIZE,
    LOG_NAME,
    LOG_TRADE_LEVEL,
)


class MetaLogger(logging.Logger):
    """MetaLogger class for enhanced logging functionality.

    This class integrates structlog for structured logging while preserving
    the existing public interface. It provides MetaExpert-specific logging
    features including structured logging, asynchronous logging, and
    specialized handlers for different types of log messages.
    """

    def __init__(
        self,
        log_level: str,
        log_file: str,
        trade_log_file: str,
        error_log_file: str,
        log_to_console: bool,
        structured_logging: bool,
        async_logging: bool,
    ) -> None:
        """Initialize the MetaLogger with enhanced configuration.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            log_to_console: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
        """
        # Configure the logging system
        self.log_level: str = log_level.upper()
        self.log_file: str = log_file
        self.trade_log_file: str = trade_log_file
        self.error_log_file: str = error_log_file
        self.log_to_console: bool = log_to_console
        self.structured_logging: bool = structured_logging
        self.async_logging: bool = async_logging
