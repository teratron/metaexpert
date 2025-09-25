"""Enhanced configuration for the MetaExpert logging system."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from metaexpert.config import APP_NAME

_ = load_dotenv()


class LoggingConfig:
    """Enhanced logging configuration with environment variable support."""

    # Basic configuration
    APP_NAME: str = APP_NAME
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
    DETAILED_FORMAT: str = "[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s"

    @classmethod
    def get_log_level(cls, env_var: str = "LOG_LEVEL") -> str:
        """Get log level from environment or default."""
        return os.getenv(env_var, cls.DEFAULT_LOG_LEVEL).upper()

    @classmethod
    def get_log_file(cls, env_var: str = "LOG_FILE") -> str:
        """Get log file name from environment or default."""
        return os.getenv(env_var, cls.DEFAULT_LOG_FILE)

    @classmethod
    def get_trade_log_file(cls, env_var: str = "TRADE_LOG_FILE") -> str:
        """Get trade log file name from environment or default."""
        return os.getenv(env_var, cls.DEFAULT_TRADE_LOG_FILE)

    @classmethod
    def get_error_log_file(cls, env_var: str = "ERROR_LOG_FILE") -> str:
        """Get error log file name from environment or default."""
        return os.getenv(env_var, cls.DEFAULT_ERROR_LOG_FILE)

    @classmethod
    def get_log_directory(cls, env_var: str = "LOG_DIRECTORY") -> str:
        """Get log directory from environment or default."""
        return os.getenv(env_var, cls.DEFAULT_LOG_DIRECTORY)

    @classmethod
    def get_max_file_size(cls, env_var: str = "LOG_MAX_SIZE") -> int:
        """Get maximum log file size from environment or default."""
        try:
            return int(os.getenv(env_var, str(cls.DEFAULT_MAX_FILE_SIZE)))
        except ValueError:
            return cls.DEFAULT_MAX_FILE_SIZE

    @classmethod
    def get_backup_count(cls, env_var: str = "LOG_BACKUP_COUNT") -> int:
        """Get backup count from environment or default."""
        try:
            return int(os.getenv(env_var, str(cls.DEFAULT_BACKUP_COUNT)))
        except ValueError:
            return cls.DEFAULT_BACKUP_COUNT

    @classmethod
    def is_structured_logging_enabled(cls, env_var: str = "STRUCTURED_LOGGING_ENABLED") -> bool:
        """Check if structured logging is enabled."""
        return os.getenv(env_var, "false").lower() == "true"

    @classmethod
    def is_async_logging_enabled(cls, env_var: str = "ASYNC_LOGGING_ENABLED") -> bool:
        """Check if async logging is enabled."""
        return os.getenv(env_var, "false").lower() == "true"

    @classmethod
    def is_console_logging_enabled(cls, env_var: str = "LOG_TO_CONSOLE") -> bool:
        """Check if console logging is enabled."""
        return os.getenv(env_var, "true").lower() == "true"

    @classmethod
    def get_log_format(cls, env_var: str = "LOG_FORMAT") -> str:
        """Get log format from environment or default."""
        return os.getenv(env_var, cls.SIMPLE_FORMAT)

    @classmethod
    def create_default_config(cls) -> dict[str, Any]:
        """Create default logging configuration dictionary."""
        return {
            "log_level": cls.get_log_level(),
            "log_file": cls.get_log_file(),
            "trade_log_file": cls.get_trade_log_file(),
            "error_log_file": cls.get_error_log_file(),
            "log_to_console": cls.is_console_logging_enabled(),
            "structured_logging": cls.is_structured_logging_enabled(),
            "async_logging": cls.is_async_logging_enabled(),
            "log_directory": cls.get_log_directory(),
            "max_file_size": cls.get_max_file_size(),
            "backup_count": cls.get_backup_count(),
        }

    @classmethod
    def create_config_from_template_params(
        cls,
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
            "log_directory": cls.get_log_directory(),
            "max_file_size": cls.get_max_file_size(),
            "backup_count": cls.get_backup_count(),
        }


# Legacy compatibility - maintain existing interface
LOG_NAME = LoggingConfig.LOG_NAME
LOG_LEVEL = LoggingConfig.get_log_level()
LOG_FORMAT = LoggingConfig.get_log_format()
LOG_FILE = LoggingConfig.get_log_file()
LOG_MAX_SIZE = LoggingConfig.get_max_file_size()
LOG_BACKUP_COUNT = LoggingConfig.get_backup_count()
LOG_DIRECTORY = LoggingConfig.get_log_directory()
DEFAULT_LOG_FILE_PATH = str(Path(LOG_DIRECTORY) / LOG_FILE)

# Enhanced configuration
STRUCTURED_LOGGING_ENABLED = LoggingConfig.is_structured_logging_enabled()
ASYNC_LOGGING_ENABLED = LoggingConfig.is_async_logging_enabled()
