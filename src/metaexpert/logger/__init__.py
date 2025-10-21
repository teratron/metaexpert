"""MetaLogger: Enhanced logging system for MetaExpert trading framework using structlog.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging with structlog, asynchronous logging,
and specialized handlers for trade and error logging.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any, TypedDict

import structlog

from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.config import LoggerConfig


class HandlerConfig(TypedDict):
    """Type definition for handler configuration."""

    name: str
    file: Path
    level: str
    logger_name: str
    formatter: logging.Formatter


class MetaLogger(structlog.stdlib.BoundLogger):
    """MetaLogger class for enhanced logging functionality using structlog.

    This class extends the standard Python Logger to provide MetaExpert-specific
    logging features including structured logging with structlog, asynchronous logging,
    and specialized handlers for different types of log messages.
    """

    def __init__(
        self,
        logger,
        processors,
        context,
        log_level: str = "DEBUG",
        log_file: str = "expert.log",
        trade_log_file: str = "trades.log",
        error_log_file: str = "errors.log",
        console_logging: bool = True,
        structured_logging: bool = False,
        async_logging: bool = False,
    ) -> None:
        """Initialize the MetaLogger with enhanced configuration.

        Args:
            logger: The underlying logger instance
            processors: Structlog processors
            context: Initial context
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            console_logging: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
        """
        # Initialize the parent BoundLogger first
        super().__init__(logger, processors, context)

        # Configure the logging system using the config object
        self.config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            console_logging=console_logging,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )
        self._loggers: dict[str, structlog.stdlib.BoundLogger] = {}
        self._handlers: dict[str, logging.Handler] = {}
        self._configured = False

        # Configure structlog with appropriate processors based on structured_logging setting
        self._configure_structlog_processors()

        # Initialize the logging system
        _root_config: dict[str, Any] = self.configure()

    @classmethod
    def create(
        cls,
        log_level: str,
        log_file: str,
        trade_log_file: str,
        error_log_file: str,
        console_logging: bool,
        structured_logging: bool,
        async_logging: bool,
    ):
        """Factory method to create a MetaLogger instance with proper initialization.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            console_logging: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging
        """
        # Create config first
        config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            console_logging=console_logging,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )

        # Configure structlog processors first
        if structured_logging:
            # JSON structured logging processors
            processors = [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ]
        else:
            # Human-readable logging processors
            processors = [
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=True),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(),
            ]

        # Create the standard logger
        std_logger = logging.getLogger(config.log_name)
        std_logger.setLevel(log_level)

        # Configure structlog
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Create and return the MetaLogger instance
        return cls(
            logger=std_logger,
            processors=processors,
            context={},
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            console_logging=console_logging,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )

    def _configure_structlog_processors(self) -> None:
        """Configure structlog processors based on configuration."""
        # This method is kept for compatibility but structlog is already configured in the factory method
        # The processors are already set during initialization
        pass

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
            if self.config.console_logging:
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
                level=self.config.log_level,
                format=self.config.log_fallback_format,
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

    def get_logger(self, name: str = "main") -> structlog.stdlib.BoundLogger:
        """Get a specialized logger by name.

        Args:
            name: Logger name ('main', 'trade', 'error')

        Returns:
            Logger instance
        """
        if self._configured:
            if name not in self._loggers:
                # Create a new logger if it doesn't exist
                std_logger = logging.getLogger(f"{self.config.log_name}.{name}")
                self._loggers[name] = structlog.wrap_logger(
                    std_logger,
                    wrapper_class=structlog.stdlib.BoundLogger,
                )
            return self._loggers.get(name) or structlog.get_logger(self.config.log_name)
        return structlog.get_logger(self.config.log_name)

    def get_main_logger(self) -> structlog.stdlib.BoundLogger:
        """Get the main application logger."""
        return self.get_logger("main")

    def get_trade_logger(self) -> structlog.stdlib.BoundLogger:
        """Get the trade-specific logger."""
        return self.get_logger("trade")

    def get_error_logger(self) -> structlog.stdlib.BoundLogger:
        """Get the error-specific logger."""
        return self.get_logger("error")

    def log_trade(self, message: str, **kwargs) -> None:
        """Log a trade-related message with structured data.

        Args:
            message: Log message
            **kwargs: Additional context data to be logged as structured fields
        """
        trade_logger = self.get_trade_logger()
        trade_logger.info(message, **kwargs)

    def log_error(
        self, message: str, exception: Exception | None = None, **kwargs
    ) -> None:
        """Log an error message with structured data.

        Args:
            message: Error message
            exception: Exception object if available
            **kwargs: Additional context data to be logged as structured fields
        """
        error_logger = self.get_error_logger()

        if exception:
            error_logger.error(message, exception=str(exception), **kwargs)
        else:
            error_logger.error(message, **kwargs)

    def _configure_handlers(self) -> list[HandlerConfig]:
        """Create and configure handlers."""
        # Create logs directory if it doesn't exist
        log_dir = Path(self.config.log_directory)
        log_dir.mkdir(exist_ok=True)

        # Determine the format based on structured_logging setting
        if self.config.structured_logging:
            # For structured logging, we use a basic formatter since structlog handles formatting
            formatter = logging.Formatter("%(message)s")
        else:
            formatter = logging.Formatter(self.config.log_format)

        return [
            HandlerConfig(
                name="main",
                file=log_dir / self.config.log_file,
                level=self.config.log_level,
                logger_name=self.config.log_name,
                formatter=formatter,
            ),
            HandlerConfig(
                name="trade",
                file=log_dir / self.config.trade_log_file,
                level=self.config.log_trade_level,
                logger_name=f"{self.config.log_name}.trade",
                formatter=formatter,
            ),
            HandlerConfig(
                name="error",
                file=log_dir / self.config.error_log_file,
                level=self.config.log_error_level,
                logger_name=f"{self.config.log_name}.error",
                formatter=formatter,
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
            maxBytes=self.config.log_max_file_size,
            backupCount=self.config.log_backup_count,
            encoding="utf-8",
        )
        handler.setLevel(config["level"])
        handler.setFormatter(config["formatter"])

        if self.config.async_logging:
            handler = AsyncHandler(handler, max_queue_size=10000)

        # self._handlers[f"{config['name']}_file"] = handler
        self._handlers.__setitem__(f"{config['name']}_file", handler)

        # Create logger for this handler
        logger = logging.getLogger(config["logger_name"])
        logger.setLevel(config["level"])
        logger.addHandler(handler)
        logger.propagate = False
        # self._loggers[config["name"]] = logger
        self._loggers.__setitem__(
            config["name"],
            structlog.wrap_logger(
                logger,
                wrapper_class=structlog.stdlib.BoundLogger,
            ),
        )
        return handler

    def _create_console_handler(self) -> logging.Handler:
        """Create a console handler.

        Returns:
            Configured console handler
        """
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setLevel(self.config.log_level)

        # Determine the format based on structured_logging setting
        if self.config.structured_logging:
            formatter = logging.Formatter("%(message)s")
        else:
            formatter = logging.Formatter(self.config.log_format)

        handler.setFormatter(formatter)

        if self.config.async_logging:
            handler = AsyncHandler(handler, max_queue_size=10000)

        # self._handlers["console"] = handler
        self._handlers.__setitem__("console", handler)

        # Create logger for this handler
        logger = logging.getLogger()
        logger.setLevel(self.config.log_level)
        logger.addHandler(handler)
        self._loggers.__setitem__(
            "console",
            structlog.wrap_logger(
                logger,
                wrapper_class=structlog.stdlib.BoundLogger,
            ),
        )
        return handler


def get_logger(name: str = "main") -> structlog.stdlib.BoundLogger:
    """Get a specialized logger by name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return structlog.get_logger(name)
