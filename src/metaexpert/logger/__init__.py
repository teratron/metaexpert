"""MetaLogger: Enhanced logging system for MetaExpert trading framework using structlog.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging with structlog, asynchronous logging,
and specialized handlers for trade and error logging.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any, Self, TypedDict

import structlog
from structlog.stdlib import BoundLogger

from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.config import LoggerConfig


class HandlerConfig(TypedDict):
    """Type definition for handler configuration."""

    name: str
    file: Path
    level: str
    logger_name: str
    formatter: logging.Formatter


class MetaLogger(BoundLogger):
    """MetaLogger class for enhanced logging functionality using structlog.

    This class extends the standard Python Logger to provide MetaExpert-specific
    logging features, including structured logging with structlog, asynchronous logging,
    and specialized handlers for different types of log messages. It streamlines
    the configuration of structlog processors and logging handlers by centralizing
    their creation and setup logic. It centralizes the configuration of structlog processors and logging handlers, ensuring consistent and efficient logging across the application.
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

        # Initialize the parent BoundLogger first
        # Configure structlog processors based on structured_logging setting
        processors = self._get_structlog_processors(self.config.structured_logging)
        super().__init__(logger, processors, context)
        self._loggers: dict[str, BoundLogger] = {}
        self._handlers: dict[str, logging.Handler] = {}
        self._configured = False

        # Create the standard logger
        std_logger = logging.getLogger(self.config.log_name)
        std_logger.setLevel(self.config.log_level)

        # Configure structlog
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Initialize the logging system
        _root_config: dict[str, Any] = self.configure()

    @staticmethod
    def _get_structlog_processors(structured_logging: bool) -> list[Any]:
        """Return a list of structlog processors based on the structured_logging flag.

        This static method centralizes the logic for selecting the appropriate
        structlog processors depending on whether structured (JSON) or human-readable
        logging is configured.

        Args:
            structured_logging: Flag indicating if structured logging should be used.

        Returns:
            A list of structlog processor functions configured for the specified
            logging format (JSON or human-readable).
        """
        if structured_logging:
            # JSON structured logging processors
            return [
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
            return [
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
    ) -> Self:
        """Factory method to create a MetaLogger instance with proper initialization.

        This method handles the complete setup of structlog processors and the underlying
        standard Python logger, then returns a configured MetaLogger instance.

        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Main log file name
            trade_log_file: Trade-specific log file name
            error_log_file: Error-specific log file name
            console_logging: Whether to output logs to console
            structured_logging: Whether to use JSON structured logging
            async_logging: Whether to use asynchronous logging

        Returns:
            MetaLogger: A fully configured MetaLogger instance
        """
        # Configure the logging system using the config object
        cls.config = LoggerConfig(
            log_level=log_level,
            log_file=log_file,
            trade_log_file=trade_log_file,
            error_log_file=error_log_file,
            console_logging=console_logging,
            structured_logging=structured_logging,
            async_logging=async_logging,
        )

        # Configure structlog processors first
        processors = cls._get_structlog_processors(structured_logging)

        # Create the standard logger
        std_logger = logging.getLogger(cls.config.log_name)
        std_logger.setLevel(cls.config.log_level)

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
            # log_level=cls.config.log_level,
            # log_file=cls.config.log_file,
            # trade_log_file=trade_log_file,
            # error_log_file=error_log_file,
            # console_logging=console_logging,
            # structured_logging=structured_logging,
            # async_logging=async_logging,
        )

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
                    wrapper_class=BoundLogger,
                )
            return self._loggers.get(name) or structlog.get_logger(self.config.log_name)
        return structlog.get_logger(self.config.log_name)

    def get_main_logger(self) -> BoundLogger:
        """Get the main application logger."""
        return self.get_logger("main")

    def get_trade_logger(self) -> BoundLogger:
        """Get the trade-specific logger."""
        return self.get_logger("trade")

    def get_error_logger(self) -> BoundLogger:
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

    def _setup_handler_and_logger(
        self,
        handler: logging.Handler,
        name: str,
        level: str,
        logger_name: str | None = None,
        is_console: bool = False,
    ) -> logging.Handler:
        """Set up a handler and its associated logger.

        This method configures a logging handler with the specified parameters,
        including level, formatter, and optional asynchronous processing. It then
        creates or retrieves a standard Python logger, associates the handler with it,
        and wraps it with structlog for enhanced logging capabilities.

        Args:
            handler: The logging handler to configure.
            name: Name for the handler (e.g., "main_file", "console").
            level: Logging level for the handler.
            logger_name: Name for the logger to associate (defaults to name).
            is_console: Flag indicating if the handler is a console handler.

        Returns:
            The configured logging handler.
        """
        # Determine the formatter based on structured_logging setting
        if self.config.structured_logging:
            formatter = logging.Formatter("%(message)s")
        else:
            formatter = logging.Formatter(self.config.log_format)

        handler.setLevel(level)
        handler.setFormatter(formatter)

        if self.config.async_logging:
            handler = AsyncHandler(handler, max_queue_size=10000)

        self._handlers.__setitem__(name, handler)

        # Create logger for this handler
        if is_console:
            std_logger = logging.getLogger()
        else:
            std_logger = logging.getLogger(logger_name or name)

        std_logger.setLevel(level)
        std_logger.addHandler(handler)
        if not is_console:  # Only set propagate to False for non-root loggers
            std_logger.propagate = False

        self._loggers.__setitem__(
            logger_name or name,
            structlog.wrap_logger(
                std_logger,
                wrapper_class=BoundLogger,
            ),
        )
        return handler

    def _create_file_handler(self, config: HandlerConfig) -> logging.Handler:
        """Create a rotating file handler.

        Args:
            config: Handler configuration

        Returns:
            Configured file handler
        """
        file_handler = logging.handlers.RotatingFileHandler(
            config["file"],
            maxBytes=self.config.log_max_file_size,
            backupCount=self.config.log_backup_count,
            encoding="utf-8",
        )
        return self._setup_handler_and_logger(
            file_handler,
            f"{config['name']}_file",
            config["level"],
            config["logger_name"],
        )

    def _create_console_handler(self) -> logging.Handler:
        """Create a console handler.

        Returns:
            Configured console handler
        """
        console_handler = logging.StreamHandler(stream=sys.stdout)
        return self._setup_handler_and_logger(
            console_handler,
            "console",
            self.config.log_level,
            "console",
            is_console=True,
        )


def get_logger(name: str = "main") -> structlog.stdlib.BoundLogger:
    """Get a specialized logger by name.

    This is a convenience function that wraps structlog.get_logger() to provide
    a consistent interface for obtaining loggers within the MetaExpert framework.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return structlog.get_logger(name)
