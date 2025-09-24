"""Enhanced logging manager for MetaExpert trading system.

This module provides centralized logging management with support for:
- Multiple specialized loggers (main, trade, error)
- Asynchronous and synchronous logging
- Structured JSON logging
- Rotating file handlers
- Console output with different levels
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any, TypedDict

from metaexpert.logger.async_log_handler import AsyncLogHandler
from metaexpert.logger.enhanced_config import LoggingConfig
from metaexpert.logger.structured_formatter import StructuredFormatter


class HandlerConfig(TypedDict):
    """Type definition for handler configuration."""
    name: str
    file: Path
    level: str
    logger_name: str


class LogManager:
    """Centralized logging manager for the MetaExpert system."""

    def __init__(self):
        """Initialize the log manager."""
        self._loggers: dict[str, logging.Logger] = {}
        self._handlers: dict[str, logging.Handler] = {}
        self._configured = False

    def configure(
        self,
        *,
        log_level: str = "INFO",
        log_file: str = "expert.log",
        trade_log_file: str = "trades.log",
        error_log_file: str = "errors.log",
        log_to_console: bool = True,
        structured_logging: bool = False,
        async_logging: bool = False,
        log_directory: str | None = None,
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
    ) -> dict[str, Any]:
        """Configure the logging system with enhanced options.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            log_to_console: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
            log_directory: Directory for log files (defaults to 'logs')
            max_file_size: Maximum size for rotating log files
            backup_count: Number of backup files to keep

        Returns:
            Configuration result with status and message
        """
        try:
            # Clear existing handlers
            self._clear_existing_loggers()

            # Set up log directory
            log_dir = Path(log_directory or LoggingConfig.get_log_directory())
            log_dir.mkdir(exist_ok=True)

            # Create formatters
            formatter = self._create_formatter(structured_logging)

            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(log_level.upper())

            # Create and configure handlers
            handlers_config: list[HandlerConfig] = [
                HandlerConfig(
                    name="main",
                    file=log_dir / log_file,
                    level=log_level,
                    logger_name=LoggingConfig.LOG_NAME
                ),
                HandlerConfig(
                    name="trade",
                    file=log_dir / trade_log_file,
                    level="INFO",
                    logger_name=f"{LoggingConfig.LOG_NAME}.trade"
                ),
                HandlerConfig(
                    name="error",
                    file=log_dir / error_log_file,
                    level="ERROR",
                    logger_name=f"{LoggingConfig.LOG_NAME}.error"
                )
            ]

            # Create file handlers
            for config in handlers_config:
                handler = self._create_file_handler(
                    config["file"],
                    config["level"],
                    formatter,
                    max_file_size,
                    backup_count
                )

                if async_logging:
                    handler = AsyncLogHandler(handler)

                self._handlers[f"{config['name']}_file"] = handler

                # Create logger for this handler
                logger = logging.getLogger(config["logger_name"])
                logger.setLevel(config["level"])
                logger.addHandler(handler)
                logger.propagate = False
                self._loggers[config["name"]] = logger

            # Add console handler if requested
            if log_to_console:
                console_handler = self._create_console_handler(formatter)
                if async_logging:
                    console_handler = AsyncLogHandler(console_handler)

                self._handlers["console"] = console_handler
                root_logger.addHandler(console_handler)

            self._configured = True

            return {
                "status": "success",
                "message": "Enhanced logging system configured successfully",
                "handlers": list(self._handlers.keys()),
                "loggers": list(self._loggers.keys())
            }

        except Exception as e:
            # Fallback to basic logging
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] %(levelname)s: (LOGGING-FALLBACK) %(message)s",
            )
            logging.error("Failed to configure enhanced logging: %s", e, exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to configure enhanced logging: {e}"
            }

    def get_logger(self, name: str = "main") -> logging.Logger:
        """Get a specialized logger by name.

        Args:
            name: Logger name ('main', 'trade', 'error')

        Returns:
            Logger instance
        """
        if not self._configured:
            # Return basic logger if not configured
            return logging.getLogger(LoggingConfig.LOG_NAME)

        return self._loggers.get(name, logging.getLogger(LoggingConfig.LOG_NAME))

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

    def log_error(self, message: str, exception: Exception | None = None, **kwargs) -> None:
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

    def shutdown(self) -> None:
        """Shutdown the logging system and clean up resources."""
        for handler in self._handlers.values():
            if hasattr(handler, 'close'):
                handler.close()

        self._handlers.clear()
        self._loggers.clear()
        self._configured = False

    def _clear_existing_loggers(self) -> None:
        """Clear existing loggers and handlers."""
        # Clear root logger handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            if hasattr(handler, 'close'):
                handler.close()

        # Clear our managed handlers
        for handler in self._handlers.values():
            if hasattr(handler, 'close'):
                handler.close()

        self._handlers.clear()
        self._loggers.clear()

    def _create_formatter(self, structured: bool) -> logging.Formatter:
        """Create appropriate formatter based on configuration.

        Args:
            structured: Whether to use structured JSON formatting

        Returns:
            Formatter instance
        """
        if structured:
            return StructuredFormatter()
        else:
            return logging.Formatter(LoggingConfig.get_log_format())

    def _create_file_handler(
        self,
        filepath: Path,
        level: str,
        formatter: logging.Formatter,
        max_size: int,
        backup_count: int
    ) -> logging.Handler:
        """Create a rotating file handler.

        Args:
            filepath: Path to log file
            level: Logging level
            formatter: Log formatter
            max_size: Maximum file size before rotation
            backup_count: Number of backup files to keep

        Returns:
            Configured file handler
        """
        handler = logging.handlers.RotatingFileHandler(
            filepath,
            maxBytes=max_size,
            backupCount=backup_count,
            encoding="utf-8"
        )
        handler.setLevel(level.upper())
        handler.setFormatter(formatter)
        return handler

    def _create_console_handler(self, formatter: logging.Formatter) -> logging.Handler:
        """Create a console handler.

        Args:
            formatter: Log formatter

        Returns:
            Configured console handler
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        return handler


# Global log manager instance
log_manager = LogManager()
