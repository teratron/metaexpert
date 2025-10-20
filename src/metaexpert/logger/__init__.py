""" """

import logging

# Remove unused import
# Remove unused imports
from .config import LoggerConfig


class MetaLogger(logging.Logger):
    """MetaLogger class for enhanced logging functionality.

    This class integrates structlog for structured logging while preserving
    the existing public interface. It provides MetaExpert-specific logging
    features including structured logging, asynchronous logging, and
    specialized handlers for different types of log messages.
    """

    def __init__(
        self,
        config: LoggerConfig,
    ) -> None:
        """Initialize the MetaLogger with enhanced configuration.

        Args:
            config: LoggerConfig instance containing all logging configuration
        """
        # Configure the logging system using the config object
        self.log_level: str = config.log_level.upper()
        self.log_file: str = config.log_file
        self.trade_log_file: str = config.trade_log_file
        self.error_log_file: str = config.error_log_file
        self.log_to_console: bool = config.log_console_logging
        self.structured_logging: bool = config.log_structured_logging
        self.async_logging: bool = config.log_async_logging

        super().__init__(config.log_name)


def get_logger(config: LoggerConfig | None = None):
    """
    Get a configured MetaLogger instance
    """
    if config is None:
        # Create default config using values from metaexpert.config
        from metaexpert.config import (
            LOG_ASYNC_LOGGING,
            LOG_CONSOLE_LOGGING,
            LOG_ERROR_FILE,
            LOG_FILE,
            LOG_LEVEL,
            LOG_NAME,
            LOG_STRUCTURED_LOGGING,
            LOG_TRADE_FILE,
        )

        config = LoggerConfig(
            log_level=LOG_LEVEL,
            log_file=LOG_FILE,
            trade_log_file=LOG_TRADE_FILE,
            error_log_file=LOG_ERROR_FILE,
            log_console_logging=LOG_CONSOLE_LOGGING,
            log_structured_logging=LOG_STRUCTURED_LOGGING,
            log_async_logging=LOG_ASYNC_LOGGING,
            log_name=LOG_NAME,
        )

    return MetaLogger(config)
