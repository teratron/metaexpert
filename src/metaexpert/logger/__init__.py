"""MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

import json
import logging
import os
import sys
from logging import Formatter, Logger, StreamHandler, getLogger
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CONFIG_FILE,
    LOG_DIRECTORY,
    LOG_FORMAT,
    LOG_MAX_FILE_SIZE, LOG_DETAILED_FORMAT,
)


class MetaLogger(Logger):
    """
    MetaLogger class for enhanced logging functionality.

    This class extends the standard Python Logger to provide MetaExpert-specific
    logging features including structured logging, asynchronous logging, and
    specialized handlers for different types of log messages.
    """

    def __init__(
            self,
            name: str,
            *,
            log_level: str,
            log_file: str,
            trade_log_file: str,
            error_log_file: str,
            log_to_console: bool,
            structured_logging: bool,
            async_logging: bool
    ) -> None:
        """Initialize the MetaLogger with enhanced configuration.

        Args:
            name: Library name
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            log_to_console: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
        """
        # Configure the logging system using the LogManager
        self.name = name
        self.log_level = log_level
        self.log_file = log_file
        self.trade_log_file = trade_log_file
        self.error_log_file = error_log_file
        self.log_to_console = log_to_console
        self.structured_logging = structured_logging
        self.async_logging = async_logging
        self.log_directory = LOG_DIRECTORY
        self.max_file_size = LOG_MAX_FILE_SIZE
        self.backup_count = LOG_BACKUP_COUNT
        self.log_format = LOG_FORMAT
        self.log_detailed_format = LOG_DETAILED_FORMAT
        self.log_config_file = LOG_CONFIG_FILE

        # Initialize the Logger with the application name
        super().__init__(self.name)

        # Check if log config file exists
        if os.path.isfile(self.log_config_file):
            try:
                # Load config from JSON file
                with open(self.log_config_file, encoding="utf-8") as file:
                    config = json.load(file)
                dictConfig(config)
            except FileNotFoundError as e:
                self.error("Error loading logging configuration file: %s", e)

        # Configure logger
        self.setLevel(self.log_level)

        # Clear existing handlers to avoid duplicate logs
        if self.handlers:
            self.handlers.clear()

        # Create formatter
        formatter = Formatter(self.log_format)

        # Create console handler if enabled
        if self.log_to_console:
            console_handler = StreamHandler(stream=sys.stdout)
            console_handler.setFormatter(formatter)
            self.addHandler(console_handler)

        # Create logs directory if it doesn't exist
        log_dir = Path(self.log_directory)
        log_dir.mkdir(exist_ok=True)

        # Create main file handler with rotation
        file_handler = RotatingFileHandler(
            log_dir / self.log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        # Create trade log file handler
        trade_handler = RotatingFileHandler(
            log_dir / self.trade_log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        trade_handler.setFormatter(formatter)
        self.addHandler(trade_handler)

        # Create error log file handler
        error_handler = RotatingFileHandler(
            log_dir / self.error_log_file,
            maxBytes=self.max_file_size,
            backupCount=self.backup_count,
            encoding="utf-8",
        )
        error_handler.setFormatter(formatter)
        self.addHandler(error_handler)


def get_logger(name: str | None = None) -> Logger:
    """Get the logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger instance.
    """
    return getLogger(name)
