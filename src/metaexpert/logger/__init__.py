"""
MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

from logging import Logger

from metaexpert.logger.config import LOG_BACKUP_COUNT, LOG_DIRECTORY, LOG_MAX_FILE_SIZE


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
        """
        Initialize the MetaLogger with enhanced configuration.

        Args:
            name: Application name
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

        # Initialize the Logger with the application name
        super().__init__(self.name)

import json
import logging
import os
import sys
from logging import Formatter, Logger, StreamHandler, getLogger
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path

from metaexpert.logger.config import LOG_CONFIG_FILE, LOG_FILE, LOG_FORMAT, LOG_LEVEL


def setup_logger(name: str | None = None, level: str | None = None) -> Logger:
    """Set up and configure the logger.

    Args:
        name (str, optional): Logger name. Defaults to None.
        level (str, optional): Logging level. Defaults to None.

    Returns:
        Logger: Configured logger instance.
    """
    # Set default logger name if not provided
    if name is None:
        name = ""#LOG_NAME

    # Create logger instance
    logger = get_logger(name)

    # Check if log config file exists
    if os.path.isfile(LOG_CONFIG_FILE):
        try:
            # Load config from JSON file
            with open(LOG_CONFIG_FILE, encoding="utf-8") as file:
                config = json.load(file)

            dictConfig(config)

            return get_logger(name)
        except FileNotFoundError as e:
            logger.error("Error loading logging configuration file: %s", e)

    # Get log level from environment or config
    if level is None:
        level = os.getenv("LOG_LEVEL", LOG_LEVEL)

    # Configure logger
    logger.setLevel(getattr(logging, level) if level else LOG_LEVEL)

    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Create formatter
    formatter = Formatter(LOG_FORMAT)

    # Create console handler
    console_handler = StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create logs directory if it doesn't exist
    # log_dir = Path(str.join("..", "logs"))
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / LOG_FILE,
        maxBytes=LOG_MAX_FILE_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
        )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> Logger:
    """Get the logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger instance.
    """
    return getLogger(name)
