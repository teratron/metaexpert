"""Configuration for the MetaExpert logging system."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from metaexpert.config import APP_NAME

_ = load_dotenv()

# Basic configuration constants
LOG_NAME: str = APP_NAME

# Default log levels
DEFAULT_LOG_LEVEL: str = "INFO"
TRADE_LOG_LEVEL: str = "INFO"
ERROR_LOG_LEVEL: str = "ERROR"

# Default file names
DEFAULT_LOG_FILE: str = "expert.log"
DEFAULT_TRADE_LOG_FILE: str = "trades.log"
DEFAULT_ERROR_LOG_FILE: str = "errors.log"

# Directory configuration
DEFAULT_LOG_DIRECTORY: str = "logs"

# File rotation settings
DEFAULT_MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
DEFAULT_BACKUP_COUNT: int = 5

# Format strings
SIMPLE_FORMAT: str = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
DETAILED_FORMAT: str = (
    "[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s"
)


class LogConfig:
    """Configuration class for logging with validation and environment variable handling."""

    @staticmethod
    def get_log_level(env_var: str = "LOG_LEVEL") -> str:
        """Get log level from environment or default."""
        return os.getenv(env_var, DEFAULT_LOG_LEVEL).upper()

    @staticmethod
    def get_log_file(env_var: str = "LOG_FILE") -> str:
        """Get log file name from environment or default."""
        return os.getenv(env_var, DEFAULT_LOG_FILE)

    @staticmethod
    def get_trade_log_file(env_var: str = "TRADE_LOG_FILE") -> str:
        """Get trade log file name from environment or default."""
        return os.getenv(env_var, DEFAULT_TRADE_LOG_FILE)

    @staticmethod
    def get_error_log_file(env_var: str = "ERROR_LOG_FILE") -> str:
        """Get error log file name from environment or default."""
        return os.getenv(env_var, DEFAULT_ERROR_LOG_FILE)

    @staticmethod
    def get_log_directory(env_var: str = "LOG_DIRECTORY") -> str:
        """Get log directory from environment or default."""
        return os.getenv(env_var, DEFAULT_LOG_DIRECTORY)

    @staticmethod
    def get_max_file_size(env_var: str = "LOG_MAX_SIZE") -> int:
        """Get maximum log file size from environment or default."""
        try:
            return int(os.getenv(env_var, str(DEFAULT_MAX_FILE_SIZE)))
        except ValueError:
            return DEFAULT_MAX_FILE_SIZE

    @staticmethod
    def get_backup_count(env_var: str = "LOG_BACKUP_COUNT") -> int:
        """Get backup count from environment or default."""
        try:
            return int(os.getenv(env_var, str(DEFAULT_BACKUP_COUNT)))
        except ValueError:
            return DEFAULT_BACKUP_COUNT

    @staticmethod
    def is_structured_logging_enabled(
            env_var: str = "STRUCTURED_LOGGING_ENABLED",
    ) -> bool:
        """Check if structured logging is enabled."""
        return os.getenv(env_var, "false").lower() == "true"

    @staticmethod
    def is_async_logging_enabled(env_var: str = "ASYNC_LOGGING_ENABLED") -> bool:
        """Check if async logging is enabled."""
        return os.getenv(env_var, "false").lower() == "true"

    @staticmethod
    def is_console_logging_enabled(env_var: str = "LOG_TO_CONSOLE") -> bool:
        """Check if console logging is enabled."""
        return os.getenv(env_var, "true").lower() == "true"

    @staticmethod
    def get_log_format(env_var: str = "LOG_FORMAT") -> str:
        """Get log format from environment or default."""
        return os.getenv(env_var, SIMPLE_FORMAT)

    @staticmethod
    def create_default_config() -> dict[str, Any]:
        """Create default logging configuration dictionary."""
        return {
            "log_level": LogConfig.get_log_level(),
            "log_file": LogConfig.get_log_file(),
            "trade_log_file": LogConfig.get_trade_log_file(),
            "error_log_file": LogConfig.get_error_log_file(),
            "log_to_console": LogConfig.is_console_logging_enabled(),
            "structured_logging": LogConfig.is_structured_logging_enabled(),
            "async_logging": LogConfig.is_async_logging_enabled(),
            "log_directory": LogConfig.get_log_directory(),
            "max_file_size": LogConfig.get_max_file_size(),
            "backup_count": LogConfig.get_backup_count(),
        }

    @staticmethod
    def create_config_from_template_params(
            log_level: str = "INFO",
            log_file: str = "expert.log",
            trade_log_file: str = "trades.log",
            error_log_file: str = "errors.log",
            log_to_console: bool = True,
            structured_logging: bool = False,
            async_logging: bool = False,
    ) -> dict[str, Any]:
        """Create configuration from template parameters (as used in MetaExpert.__init__)."""
        return {
            "log_level": log_level,
            "log_file": log_file,
            "trade_log_file": trade_log_file,
            "error_log_file": error_log_file,
            "log_to_console": log_to_console,
            "structured_logging": structured_logging,
            "async_logging": async_logging,
            "log_directory": LogConfig.get_log_directory(),
            "max_file_size": LogConfig.get_max_file_size(),
            "backup_count": LogConfig.get_backup_count(),
        }


# Backward compatibility with old LoggingConfig class
class LoggingConfig(LogConfig):
    """Legacy compatibility class - use LogConfig instead."""

    # Expose constants as class attributes for backward compatibility
    LOG_NAME = LOG_NAME
    DEFAULT_LOG_LEVEL = DEFAULT_LOG_LEVEL
    TRADE_LOG_LEVEL = TRADE_LOG_LEVEL
    ERROR_LOG_LEVEL = ERROR_LOG_LEVEL
    DEFAULT_LOG_FILE = DEFAULT_LOG_FILE
    DEFAULT_TRADE_LOG_FILE = DEFAULT_TRADE_LOG_FILE
    DEFAULT_ERROR_LOG_FILE = DEFAULT_ERROR_LOG_FILE
    DEFAULT_LOG_DIRECTORY = DEFAULT_LOG_DIRECTORY
    DEFAULT_MAX_FILE_SIZE = DEFAULT_MAX_FILE_SIZE
    DEFAULT_BACKUP_COUNT = DEFAULT_BACKUP_COUNT
    SIMPLE_FORMAT = SIMPLE_FORMAT
    DETAILED_FORMAT = DETAILED_FORMAT


# Pre-computed values using LogConfig
LOG_LEVEL = LogConfig.get_log_level()
LOG_FORMAT = LogConfig.get_log_format()
LOG_FILE = LogConfig.get_log_file()
LOG_MAX_SIZE = LogConfig.get_max_file_size()
LOG_BACKUP_COUNT = LogConfig.get_backup_count()
LOG_DIRECTORY = LogConfig.get_log_directory()
DEFAULT_LOG_FILE_PATH = str(Path(LOG_DIRECTORY) / LOG_FILE)

# Enhanced configuration flags
STRUCTURED_LOGGING_ENABLED = LogConfig.is_structured_logging_enabled()
ASYNC_LOGGING_ENABLED = LogConfig.is_async_logging_enabled()
