"""MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

import json
import logging
import logging.config
import logging.handlers
import os
import sys
# from logging.config import dictConfig
# from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TypedDict

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CONFIG_FILE,
    LOG_DIRECTORY,
    LOG_FORMAT,
    LOG_MAX_FILE_SIZE,
    LOG_TRADE_LEVEL_NUM, LOG_REPORT_LEVEL_NUM, LOG_TRADE_LEVEL_NAME, LOG_REPORT_LEVEL_NAME, LOG_NAME, LOG_TRADE_LEVEL,
    LOG_ERROR_LEVEL,
)
from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.formatter import MainFormatter

# Define custom log levels
logging.addLevelName(LOG_TRADE_LEVEL_NUM, LOG_TRADE_LEVEL_NAME)
logging.addLevelName(LOG_REPORT_LEVEL_NUM, LOG_REPORT_LEVEL_NAME)


class HandlerConfig(TypedDict):
    """Type definition for handler configuration."""

    name: str
    file: Path
    level: str
    logger_name: str


class MetaLogger(logging.Logger):
    """MetaLogger class for enhanced logging functionality.

    This class extends the standard Python Logger to provide MetaExpert-specific
    logging features including structured logging, asynchronous logging, and
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
            async_logging: bool
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
        # Initialize the Logger with the application name
        super().__init__(self.name)

        # Configure the logging system
        self.log_level = log_level.upper()
        self.log_file = log_file
        self.trade_log_file = trade_log_file
        self.error_log_file = error_log_file
        self.log_to_console = log_to_console
        self.structured_logging = structured_logging
        self.async_logging = async_logging
        self._root_logger = logging.getLogger()
        self._loggers: dict[str, logging.Logger] = {}
        self._handlers: dict[str, logging.Handler] = {}
        self._configured = False

        # Clear existing handlers
        self._clear_existing_loggers()

        # Check if log config file exists
        if os.path.isfile(LOG_CONFIG_FILE):
            try:
                # Load config from JSON file
                with open(LOG_CONFIG_FILE, encoding="utf-8") as file:
                    config = json.load(file)
                logging.config.dictConfig(config)
            except FileNotFoundError as e:
                self.error("Error loading logging configuration file: %s", e)
            finally:
                return

        # Create logs directory if it doesn't exist
        log_dir = Path(LOG_DIRECTORY)
        log_dir.mkdir(exist_ok=True)

        # Configure log levels
        # self.setLevel(self.log_level)
        self._root_logger.setLevel(self.log_level)

        # Create and configure handlers
        handlers_config: list[HandlerConfig] = [
            HandlerConfig(
                name="main",
                file=log_dir / self.log_file,
                level=self.log_level,
                logger_name=LOG_NAME,
            ),
            HandlerConfig(
                name="trade",
                file=log_dir / self.trade_log_file,
                level=LOG_TRADE_LEVEL,
                logger_name=f"{LOG_NAME}.trade",
            ),
            HandlerConfig(
                name="error",
                file=log_dir / self.error_log_file,
                level=LOG_ERROR_LEVEL,
                logger_name=f"{LOG_NAME}.error",
            ),
        ]

        # Create formatter
        # formatter = Formatter(LOG_FORMAT)
        self._formatter = self._create_formatter()

        # Create file handlers
        for config in handlers_config:
            file_handler = self._create_file_handler(config)
            # handler = logging.handlers.RotatingFileHandler(
            #     config["file"],
            #     maxBytes=LOG_MAX_FILE_SIZE,
            #     backupCount=LOG_BACKUP_COUNT,
            #     encoding="utf-8",
            # )
            # handler.setLevel(config["level"])
            # handler.setFormatter(self._formatter)
            #
            # if async_logging:
            #     handler = AsyncHandler(handler)
            #
            # self._handlers[f"{config['name']}_file"] = handler
            #
            # # Create logger for this handler
            # logger = logging.getLogger(config["logger_name"])
            # logger.setLevel(config["level"])
            # logger.addHandler(handler)
            # logger.propagate = False
            # self._loggers[config["name"]] = logger

        # Create console handler if enabled
        # if self.log_to_console:
        #     console_handler = logging.StreamHandler(stream=sys.stdout)
        #     console_handler.setFormatter(self._formatter)
        #     self.addHandler(console_handler)

        # Add console handler if requested
        if self.log_to_console:
            console_handler = self._create_console_handler()

        self._configured = True

        # Create main file handler with rotation
        # file_handler = logging.handlers.RotatingFileHandler(
        #     log_dir / self.log_file,
        #     maxBytes=LOG_MAX_FILE_SIZE,
        #     backupCount=LOG_BACKUP_COUNT,
        #     encoding="utf-8",
        # )
        # file_handler.setFormatter(formatter)
        # self.addHandler(file_handler)
        #
        # # Create trade log file handler
        # trade_handler = RotatingFileHandler(
        #     log_dir / self.trade_log_file,
        #     maxBytes=LOG_MAX_FILE_SIZE,
        #     backupCount=LOG_BACKUP_COUNT,
        #     encoding="utf-8",
        # )
        # trade_handler.setFormatter(formatter)
        # self.addHandler(trade_handler)
        #
        # # Create error log file handler
        # error_handler = RotatingFileHandler(
        #     log_dir / self.error_log_file,
        #     maxBytes=LOG_MAX_FILE_SIZE,
        #     backupCount=LOG_BACKUP_COUNT,
        #     encoding="utf-8",
        # )
        # error_handler.setFormatter(formatter)
        # self.addHandler(error_handler)

    def _clear_existing_loggers(self) -> None:
        """Clear existing loggers and handlers."""
        # Clear root logger handlers
        for handler in self._root_logger.handlers[:]:
            self._root_logger.removeHandler(handler)
            if hasattr(handler, "close"):
                handler.close()

        # Clear our managed handlers
        for handler in self._handlers.values():
            if hasattr(handler, "close"):
                handler.close()

        self._handlers.clear()
        self._loggers.clear()

    def _create_formatter(self) -> logging.Formatter:
        """Create appropriate formatter based on configuration.

        Returns:
            Formatter instance
        """
        if self.structured_logging:
            return MainFormatter()
        return logging.Formatter(LOG_FORMAT)

    def _create_file_handler(self, config: HandlerConfig) -> logging.Handler:
        """Create a rotating file handler.

        Args:
            config: Handler configuration

        Returns:
            Configured file handler
        """
        handler = logging.handlers.RotatingFileHandler(
            config["file"],
            maxBytes=LOG_MAX_FILE_SIZE,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        handler.setLevel(config["level"])
        handler.setFormatter(self._formatter)

        if self.async_logging:
            handler = AsyncHandler(handler)

        self._handlers[f"{config['name']}_file"] = handler

        # Create logger for this handler
        logger = logging.getLogger(config["logger_name"])
        logger.setLevel(config["level"])
        logger.addHandler(handler)
        logger.propagate = False
        self._loggers[config["name"]] = logger
        return handler

    def _create_console_handler(self) -> logging.Handler:
        """Create a console handler.

        Returns:
            Configured console handler
        """
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(self._formatter)

        if self.async_logging:
            handler = AsyncHandler(handler)

        self._handlers["console"] = handler
        self._root_logger.addHandler(handler)
        return handler


def get_logger(name: str | None = None) -> logging.Logger:
    """Get the logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger instance.
    """
    return logging.getLogger(name)
