"""Centralized configuration constants for MetaExpert logger."""

from typing import Final

# File rotation settings
LOG_MAX_FILE_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT: Final[int] = 5

# Performance settings
LOG_CACHE_LOGGER_ON_FIRST_USE: Final[bool] = True
PERFORMANCE_MONITOR_THRESHOLD_MS: Final[float] = 100.0

# Default log levels
LOG_LEVEL: Final[str] = "DEBUG"
LOG_TRADE_LEVEL: Final[str] = "INFO"
LOG_ERROR_LEVEL: Final[str] = "ERROR"

# Default file names
LOG_FILE: Final[str] = "expert.log"
LOG_TRADE_FILE: Final[str] = "trades.log"
LOG_ERROR_FILE: Final[str] = "errors.log"

# Directory settings
LOG_DIRECTORY: Final[str] = "logs"

# Output settings
LOG_CONSOLE_LOGGING: Final[bool] = True
LOG_FILE_LOGGING: Final[bool] = True
LOG_USE_COLORS: Final[bool] = True
LOG_STRUCTURED_LOGGING: Final[bool] = False

# Sensitive data keys for filtering
SENSITIVE_KEYS: Final[set[str]] = {
    "password",
    "token",
    "api_key",
    "secret",
    "private_key",
    "apikey",
    "api_secret",
    "access_token",
    "refresh_token",
}

# Required fields for different event types
TRADE_EVENT_REQUIRED_FIELDS: Final[set[str]] = {"symbol", "side", "quantity"}
ERROR_EVENT_REQUIRED_FIELDS: Final[set[str]] = {"level", "message"}

# Performance thresholds
SLOW_OPERATION_THRESHOLD_MS: Final[float] = 1000.0
LOG_SIZE_WARNING_THRESHOLD_BYTES: Final[int] = 50 * 1024 * 1024  # 50MB
