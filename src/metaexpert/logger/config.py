"""Configuration logging system."""

from metaexpert.config import APP_NAME

# Logging configuration constants
LOG_NAME: str = APP_NAME

# Default log levels
LOG_LEVEL: str = "DEBUG"
LOG_TRADE_LEVEL: str = "INFO"
LOG_ERROR_LEVEL: str = "ERROR"

# Default file names
LOG_FILE: str = "expert.log"
LOG_TRADE_FILE: str = "trades.log"
LOG_ERROR_FILE: str = "errors.log"

# Directory configuration
LOG_DIRECTORY: str = "logs"

# File rotation settings
LOG_MAX_FILE_SIZE: int = 10485760  # 10 * 1024 * 1024 (10MB)
LOG_BACKUP_COUNT: int = 5

# Format settings
LOG_FORMAT: str = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
LOG_DETAILED_FORMAT: str = "[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s"
LOG_CONFIG_FILE: str = "config.json"

# Enhanced configuration flags
LOG_CONSOLE_LOGGING_ENABLED: bool = True
LOG_STRUCTURED_LOGGING_ENABLED: bool = False
LOG_ASYNC_LOGGING_ENABLED: bool = False


# def _is_logging_enabled(key: str, default: str = "true") -> bool:
#     return os.getenv(key, default).lower() == "true"

# class LogConfig:
#     """Configuration class for logging with validation and environment variable handling."""
#
#     @staticmethod
#     def get_log_level(env_var: str = "LOG_LEVEL") -> str:
#         """Get log level from environment or default."""
#         return os.getenv(env_var, DEFAULT_LOG_LEVEL).upper()
#
#     @staticmethod
#     def get_log_file(env_var: str = "LOG_FILE") -> str:
#         """Get log file name from environment or default."""
#         return os.getenv(env_var, DEFAULT_LOG_FILE)
#
#     @staticmethod
#     def get_trade_log_file(env_var: str = "TRADE_LOG_FILE") -> str:
#         """Get trade log file name from environment or default."""
#         return os.getenv(env_var, DEFAULT_TRADE_LOG_FILE)
#
#     @staticmethod
#     def get_error_log_file(env_var: str = "ERROR_LOG_FILE") -> str:
#         """Get error log file name from environment or default."""
#         return os.getenv(env_var, DEFAULT_ERROR_LOG_FILE)
#
#     @staticmethod
#     def get_log_directory(env_var: str = "LOG_DIRECTORY") -> str:
#         """Get log directory from environment or default."""
#         return os.getenv(env_var, DEFAULT_LOG_DIRECTORY)
#
#     @staticmethod
#     def get_max_file_size(env_var: str = "LOG_MAX_SIZE") -> int:
#         """Get maximum log file size from environment or default."""
#         try:
#             return int(os.getenv(env_var, str(DEFAULT_MAX_FILE_SIZE)))
#         except ValueError:
#             return DEFAULT_MAX_FILE_SIZE
#
#     @staticmethod
#     def get_backup_count(env_var: str = "LOG_BACKUP_COUNT") -> int:
#         """Get backup count from environment or default."""
#         try:
#             return int(os.getenv(env_var, str(DEFAULT_BACKUP_COUNT)))
#         except ValueError:
#             return DEFAULT_BACKUP_COUNT
#
#     @staticmethod
#     def is_structured_logging_enabled(
#         env_var: str = "STRUCTURED_LOGGING_ENABLED",
#     ) -> bool:
#         """Check if structured logging is enabled."""
#         return os.getenv(env_var, "false").lower() == "true"
#
#     @staticmethod
#     def is_async_logging_enabled(env_var: str = "ASYNC_LOGGING_ENABLED") -> bool:
#         """Check if async logging is enabled."""
#         return os.getenv(env_var, "false").lower() == "true"
#
#     @staticmethod
#     def is_console_logging_enabled(env_var: str = "LOG_TO_CONSOLE") -> bool:
#         """Check if console logging is enabled."""
#         return os.getenv(env_var, "true").lower() == "true"
#
#     @staticmethod
#     def get_log_format(env_var: str = "LOG_FORMAT") -> str:
#         """Get log format from environment or default."""
#         return os.getenv(env_var, SIMPLE_FORMAT)
#
#     @staticmethod
#     def create_default_config() -> dict[str, Any]:
#         """Create default logging configuration dictionary."""
#         return {
#             "log_level": LogConfig.get_log_level(),
#             "log_file": LogConfig.get_log_file(),
#             "trade_log_file": LogConfig.get_trade_log_file(),
#             "error_log_file": LogConfig.get_error_log_file(),
#             "log_to_console": LogConfig.is_console_logging_enabled(),
#             "structured_logging": LogConfig.is_structured_logging_enabled(),
#             "async_logging": LogConfig.is_async_logging_enabled(),
#             "log_directory": LogConfig.get_log_directory(),
#             "max_file_size": LogConfig.get_max_file_size(),
#             "backup_count": LogConfig.get_backup_count(),
#         }
#
#     @staticmethod
#     def create_config_from_template_params(
#         log_level: str = "INFO",
#         log_file: str = "expert.log",
#         trade_log_file: str = "trades.log",
#         error_log_file: str = "errors.log",
#         log_to_console: bool = True,
#         structured_logging: bool = False,
#         async_logging: bool = False,
#     ) -> dict[str, Any]:
#         """Create configuration from template parameters (as used in MetaExpert.__init__)."""
#         return {
#             "log_level": log_level,
#             "log_file": log_file,
#             "trade_log_file": trade_log_file,
#             "error_log_file": error_log_file,
#             "log_to_console": log_to_console,
#             "structured_logging": structured_logging,
#             "async_logging": async_logging,
#             "log_directory": LogConfig.get_log_directory(),
#             "max_file_size": LogConfig.get_max_file_size(),
#             "backup_count": LogConfig.get_backup_count(),
#         }
