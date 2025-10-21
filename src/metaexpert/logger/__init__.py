"""MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any, TypedDict

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
from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.config import LoggerConfig
from metaexpert.logger.formatter import ErrorFormatter, MainFormatter, TradeFormatter


class HandlerConfig(TypedDict):
    """Type definition for handler configuration."""

    name: str
    file: Path
    level: str
    logger_name: str
    formatter: logging.Formatter


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
        self.log_level = log_level.upper()
        self.log_file = log_file
        self.trade_log_file = trade_log_file
        self.error_log_file = error_log_file
        self.log_to_console = log_to_console
        self.structured_logging = structured_logging
        self.async_logging = async_logging
        self._loggers: dict[str, logging.Logger] = {}
        self._handlers: dict[str, logging.Handler] = {}
        self._configured = False

        config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            log_console_logging=log_to_console,
            log_structured_logging=structured_logging,
            log_async_logging=async_logging,
        )

        # Configure the logging system using the config object
        self.log_level: str = config.log_level
        self.log_file: str = config.log_file
        self.trade_log_file: str = config.trade_log_file
        self.error_log_file: str = config.error_log_file
        self.log_to_console: bool = config.log_console_logging
        self.structured_logging: bool = config.log_structured_logging
        self.async_logging: bool = config.log_async_logging

        super().__init__(config.log_name)

        # Formatters
        self._main_formatter = (
            MainFormatter()
            if self.structured_logging
            else logging.Formatter(LOG_FORMAT)
        )
        self._trade_formatter = (
            TradeFormatter() if self.structured_logging else self._main_formatter
        )
        self._error_formatter = (
            ErrorFormatter()
            if self.structured_logging
            else logging.Formatter(LOG_DETAILED_FORMAT)
        )

        # Initialize the Logger with the application name
        super().__init__(LOG_NAME, self.log_level)

        _root_config: dict[str, Any] = self.configure()

    def configure(self) -> dict[str, Any]:
        """Configure the logging system with enhanced options.

        Returns:
            Configuration result with status and message
        """
        try:
            # Clear existing handlers
            self.shutdown()

            # Create file handlers
            for config in self._configure_handlers():
                _file_handler = self._create_file_handler(config)

            # Add console handler if requested
            if self.log_to_console:
                _console_handler = self._create_console_handler()

            self._configured = True
            return {
                "status": "success",
                "message": "Enhanced logging system configured successfully",
                "handlers": list(self._handlers.keys()),
                "loggers": list(self._loggers.keys()),
            }
        except Exception as e:
            # Fallback to basic logging
            logging.basicConfig(
                level=self.log_level,
                format=LOG_FALLBACK_FORMAT,
            )
            logging.error("Failed to configure enhanced logging: %s", e, exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to configure enhanced logging: {e}",
            }

    def shutdown(self) -> None:
        """Clear existing loggers and handlers."""
        # Clear our managed handlers
        for handler in self._handlers.values():
            if hasattr(handler, "close"):
                handler.close()

        self._handlers.clear()
        self._loggers.clear()
        self._configured = False

    def get_logger(self, name: str = "main") -> logging.Logger:
        """Get a specialized logger by name.

        Args:
            name: Logger name ('main', 'trade', 'error')

        Returns:
            Logger instance
        """
        if self._configured:
            return self._loggers.get(name, logging.getLogger(LOG_NAME))
        return logging.getLogger(LOG_NAME)

    def get_main_logger(self) -> logging.Logger:
        """Get the main application logger."""
        return self.get_logger("main")

    def get_trade_logger(self) -> logging.Logger:
        """Get the trade-specific logger."""
        return self.get_logger("trade")

    def get_error_logger(self) -> logging.Logger:
        """Get the error-specific logger."""
        return self.get_logger("error")

    def log_trade(self, message: str, **kwargs) -> None:
        """Log a trade-related message.

        Args:
            message: Log message
            **kwargs: Additional context data
        """
        trade_logger = self.get_trade_logger()
        if kwargs:
            trade_logger.info(f"{message} | Context: {kwargs}")
        else:
            trade_logger.info(message)

    def log_error(
        self, message: str, exception: Exception | None = None, **kwargs
    ) -> None:
        """Log an error message.

        Args:
            message: Error message
            exception: Exception object if available
            **kwargs: Additional context data
        """
        error_logger = self.get_error_logger()
        if exception:
            error_logger.error(f"{message} | Exception: {exception}", exc_info=True)
        else:
            error_logger.error(message)

        if kwargs:
            error_logger.error(f"Error context: {kwargs}")

    def _configure_handlers(self) -> list[HandlerConfig]:
        """Create and configure handlers."""
        # Create logs directory if it doesn't exist
        log_dir = Path(LOG_DIRECTORY)
        log_dir.mkdir(exist_ok=True)
        return [
            HandlerConfig(
                name="main",
                file=log_dir / self.log_file,
                level=self.log_level,
                logger_name=LOG_NAME,
                formatter=self._main_formatter,
            ),
            HandlerConfig(
                name="trade",
                file=log_dir / self.trade_log_file,
                level=LOG_TRADE_LEVEL,
                logger_name=f"{LOG_NAME}.trade",
                formatter=self._trade_formatter,
            ),
            HandlerConfig(
                name="error",
                file=log_dir / self.error_log_file,
                level=LOG_ERROR_LEVEL,
                logger_name=f"{LOG_NAME}.error",
                formatter=self._error_formatter,
            ),
        ]

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
        handler.setFormatter(config["formatter"])

        if self.async_logging:
            handler = AsyncHandler(handler, max_queue_size=10000)

        # self._handlers[f"{config['name']}_file"] = handler
        self._handlers.__setitem__(f"{config['name']}_file", handler)

        # Create logger for this handler
        logger = logging.getLogger(config["logger_name"])
        logger.setLevel(config["level"])
        logger.addHandler(handler)
        logger.propagate = False
        # self._loggers[config["name"]] = logger
        self._loggers.__setitem__(config["name"], logger)
        return handler

    def _create_console_handler(self) -> logging.Handler:
        """Create a console handler.

        Returns:
            Configured console handler
        """
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(self._main_formatter)

        if self.async_logging:
            handler = AsyncHandler(handler, max_queue_size=10000)

        # self._handlers["console"] = handler
        self._handlers.__setitem__("console", handler)

        # Create logger for this handler
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        logger.addHandler(handler)
        self._loggers.__setitem__("console", logger)
        return handler
