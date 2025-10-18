"""MetaLogger class for enhanced logging functionality.

This class integrates structlog for structured logging while preserving
the existing public interface. It provides MetaExpert-specific logging
features including structured logging, asynchronous logging, and
specialized handlers for different types of log messages.
"""

import atexit
import logging
import os
import sys
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path
from queue import Queue
from typing import Any

import structlog

from .config import LogConfiguration
from .context import LogContext
from .formatters import get_console_formatter, get_json_formatter
from .processors import (
    add_context,
    add_timestamp,
    ensure_domain_context,
    mask_sensitive_data,
)

# Import file handlers


class MetaLogger:
    """MetaLogger class for enhanced logging functionality.

    This class integrates structlog for structured logging while preserving
    the existing public interface. It provides MetaExpert-specific logging
    features including structured logging, asynchronous logging, and
    specialized handlers for different types of log messages.
    """

    def __init__(self, config: LogConfiguration | None = None, **kwargs) -> None:
        """Initialize the MetaLogger with enhanced configuration.

        Args:
            config: LogConfiguration object with all configuration settings
            **kwargs: Additional parameters to override config values
        """
        # Create configuration using provided config or defaults, with kwargs as overrides
        if config is None:
            self.config = LogConfiguration(**kwargs)
        else:
            # Update config with any kwargs that might override the initial config
            config_dict = config.model_dump()
            config_dict.update(kwargs)
            self.config = LogConfiguration(**config_dict)

        # Create log directory if it doesn't exist
        log_dir = Path(self.config.log_directory)
        log_dir.mkdir(parents=True, exist_ok=True)

        # Initialize structlog with processors
        self._setup_structlog()

        # Initialize loggers for different log types
        self._setup_loggers()

        # Initialize asyncio components if async logging is enabled
        self._setup_async()

        # Register cleanup function to run at exit
        atexit.register(self._cleanup)

    def _setup_structlog(self):
        """Setup structlog with appropriate processors and formatters."""
        # Define processors based on configuration
        processors = [
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            add_timestamp,
            add_context,  # Custom processor to add contextual information
            ensure_domain_context,  # Ensure domain-specific context fields are included
            mask_sensitive_data
            if self.config.mask_sensitive_data
            else lambda x, y, z: z,  # Only add if masking is enabled
            structlog.processors.UnicodeDecoder(),
        ]

        # Configure structlog
        structlog.configure(
            processors=processors,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Configure the stdlib logger to work with structlog
        logging.basicConfig(
            format="%(message)s", level=self.config.log_level, handlers=[]
        )

    def _setup_loggers(self):
        """Setup different loggers for expert, trades, and errors."""
        # Import handlers based on whether async is enabled
        if self.config.enable_async:
            from .handlers.async_file import (
                AsyncErrorsFileHandler,
                AsyncExpertFileHandler,
                AsyncTradesFileHandler,
            )
        else:
            from .handlers.file import (
                ErrorsFileHandler,
                ExpertFileHandler,
                TradesFileHandler,
            )

        # Import disk space monitoring handler
        from .handlers.stderr import DiskSpaceMonitoringFileHandler

        # Create the base logger
        self.base_logger = logging.getLogger("metaexpert")
        self.base_logger.setLevel(self.config.log_level)

        # Remove any existing handlers
        self.base_logger.handlers.clear()

        # Create specialized handlers based on configuration with appropriate filters
        handlers = []

        # File handler for expert logs - captures all log levels based on config
        if self.config.enable_async:
            base_expert_handler = AsyncExpertFileHandler(
                os.path.join(self.config.log_directory, self.config.expert_log_file),
                maxBytes=self.config.max_file_size_mb
                * 1024
                * 1024,  # Convert MB to bytes
                backupCount=self.config.backup_count,
            )
        else:
            base_expert_handler = ExpertFileHandler(
                os.path.join(self.config.log_directory, self.config.expert_log_file),
                maxBytes=self.config.max_file_size_mb
                * 1024
                * 1024,  # Convert MB to bytes
                backupCount=self.config.backup_count,
            )

        # Wrap with disk space monitoring if needed
        if hasattr(self.config, "disk_space_check") and self.config.disk_space_check:
            expert_handler = DiskSpaceMonitoringFileHandler(
                os.path.join(self.config.log_directory, self.config.expert_log_file),
                console_handler=logging.StreamHandler(sys.stdout)
                if self.config.log_to_console
                else None,
                low_space_threshold_mb=10,  # Configurable threshold
            )
            expert_handler.setLevel(self.config.log_level)
            expert_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        else:
            expert_handler = base_expert_handler
            expert_handler.setLevel(self.config.log_level)
            expert_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        handlers.append(expert_handler)

        # File handler for trades logs - only logs trade-related entries
        if self.config.enable_async:
            base_trades_handler = AsyncTradesFileHandler(
                os.path.join(self.config.log_directory, self.config.trades_log_file),
                maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
            )
        else:
            base_trades_handler = TradesFileHandler(
                os.path.join(self.config.log_directory, self.config.trades_log_file),
                maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
            )

        # Wrap with disk space monitoring if needed
        if hasattr(self.config, "disk_space_check") and self.config.disk_space_check:
            trades_handler = DiskSpaceMonitoringFileHandler(
                os.path.join(self.config.log_directory, self.config.trades_log_file),
                console_handler=logging.StreamHandler(sys.stdout)
                if self.config.log_to_console
                else None,
                low_space_threshold_mb=100,  # Configurable threshold
            )
            trades_handler.setLevel(logging.INFO)
            trades_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        else:
            trades_handler = base_trades_handler
            trades_handler.setLevel(logging.INFO)
            trades_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
        handlers.append(trades_handler)

        # File handler for errors logs - only logs error and critical entries
        if self.config.enable_async:
            base_errors_handler = AsyncErrorsFileHandler(
                os.path.join(self.config.log_directory, self.config.errors_log_file),
                maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
            )
        else:
            base_errors_handler = ErrorsFileHandler(
                os.path.join(self.config.log_directory, self.config.errors_log_file),
                maxBytes=self.config.max_file_size_mb * 1024 * 1024,
                backupCount=self.config.backup_count,
            )

        # Wrap with disk space monitoring if needed
        if hasattr(self.config, "disk_space_check") and self.config.disk_space_check:
            errors_handler = DiskSpaceMonitoringFileHandler(
                os.path.join(self.config.log_directory, self.config.errors_log_file),
                console_handler=logging.StreamHandler(sys.stderr)
                if self.config.log_to_console
                else None,
                low_space_threshold_mb=100,  # Configurable threshold
            )
            errors_handler.setLevel(logging.ERROR)
        else:
            errors_handler = base_errors_handler
            errors_handler.setLevel(logging.ERROR)
        errors_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        handlers.append(errors_handler)

        # Console handler if enabled
        if self.config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            console_handler.setLevel(self.config.log_level)
            handlers.append(console_handler)

        # Add handlers to base logger
        for handler in handlers:
            self.base_logger.addHandler(handler)

        # Create structlog wrapper
        self.logger = structlog.get_logger("metaexpert")

    def _get_formatter_for_file(self):
        """Get the appropriate formatter for file output based on configuration."""
        if self.config.file_log_format == "json":
            return get_json_formatter()
        else:
            return get_console_formatter()

    def _create_file_handler(self, filename: str, level: str):
        """Create a rotating file handler for a specific log file."""
        filepath = os.path.join(self.config.log_directory, filename)
        max_bytes = self.config.max_file_size_mb * 1024 * 1024  # Convert MB to bytes

        handler = RotatingFileHandler(
            filepath, maxBytes=max_bytes, backupCount=self.config.backup_count
        )
        handler.setLevel(level)

        # Set up formatter based on configuration
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        return handler

    def _setup_console_formatter(self):
        """Setup console formatter based on configuration."""
        if self.config.console_log_format == "json":
            return get_json_formatter()
        else:
            return get_console_formatter()

    def _setup_async(self):
        """Setup asynchronous logging components if enabled."""
        if self.config.enable_async:
            self.log_queue = Queue()
            self.async_logger_thread = threading.Thread(
                target=self._async_log_worker, daemon=True
            )
            self.async_logger_thread.start()

    def _async_log_worker(self):
        """Worker thread for processing log entries asynchronously."""
        while True:
            try:
                record = self.log_queue.get(timeout=1)
                if record is None:  # Sentinel to stop the worker
                    break
                # Process the log record
                self.base_logger.handle(record)
                self.log_queue.task_done()
            except Exception:
                continue  # Continue processing other logs even if one fails

    def _cleanup(self):
        """Cleanup function to properly shut down async logging."""
        if hasattr(self, "async_logger_thread") and self.config.enable_async:
            self.log_queue.put(None)  # Send sentinel to stop worker
            self.async_logger_thread.join(timeout=2)  # Wait for thread to finish

    def bind(self, context: dict[str, Any]) -> "MetaLogger":
        """Create a new logger with additional context bound to it.

        Args:
            context: Key-value pairs to add as context

        Returns:
            A new MetaLogger instance with the context bound
        """
        # This returns a new logger with the context bound using structlog
        new_logger = self.logger.bind(**context)
        # Create a new MetaLogger with the bound logger
        new_meta_logger = MetaLogger(config=self.config)
        new_meta_logger.logger = new_logger
        return new_meta_logger

    def debug(self, event: str, **kwargs) -> None:
        """Log a debug message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs) -> None:
        """Log an info message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs) -> None:
        """Log a warning message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs) -> None:
        """Log an error message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.error(event, **kwargs)

    def critical(self, event: str, **kwargs) -> None:
        """Log a critical message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.critical(event, **kwargs)

    def trade(self, event: str, **kwargs) -> None:
        """Log a trade-specific message.

        Args:
            event: The event message to log
            **kwargs: Additional context fields to include
        """
        self.logger.info(event, category="trade", **kwargs)

    def context(self, **kwargs) -> LogContext:
        """Create a context manager for contextual logging.

        Args:
            **kwargs: Context fields to bind

        Returns:
            A LogContext manager
        """
        return LogContext(self, **kwargs)


def get_logger(name: str) -> logging.Logger:
    """Compatibility function to get a standard logger.

    Args:
        name: Name for the logger

    Returns:
        A standard Python logging.Logger instance
    """
    return logging.getLogger(name)
