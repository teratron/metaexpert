"""Configuration for MetaExpert logger using Pydantic."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from metaexpert.config import (
    LOG_ASYNC_LOGGING,
    LOG_BACKUP_COUNT,
    LOG_CONSOLE_LOGGING,
    LOG_DETAILED_FORMAT,
    LOG_DIRECTORY,
    LOG_ERROR_FILE,
    LOG_ERROR_LEVEL,
    LOG_FALLBACK_FORMAT,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_LEVEL_CRITICAL,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_INFO,
    LOG_LEVEL_WARNING,
    LOG_MAX_FILE_SIZE,
    LOG_NAME,
    LOG_STRUCTURED_LOGGING,
    LOG_TRADE_FILE,
    LOG_TRADE_LEVEL,
)


class LoggerConfig(BaseModel):
    """Configuration for MetaExpert logger."""

    # Log levels
    log_level: str = Field(
        default=LOG_LEVEL,
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ).upper()
    log_trade_level: str = Field(
        default=LOG_TRADE_LEVEL, description="Trade-specific log level"
    ).upper()
    log_error_level: str = Field(
        default=LOG_ERROR_LEVEL, description="Error-specific log level"
    ).upper()

    # File names
    log_file: str = Field(default=LOG_FILE, description="Main log file name")
    trade_log_file: str = Field(
        default=LOG_TRADE_FILE, description="Trade-specific log file name"
    )
    error_log_file: str = Field(
        default=LOG_ERROR_FILE, description="Error-specific log file name"
    )

    # Directory configuration
    log_directory: str = Field(
        default=LOG_DIRECTORY, description="Directory for log files"
    )

    # File rotation settings
    log_max_file_size: int = Field(
        default=LOG_MAX_FILE_SIZE,
        description="Maximum log file size in bytes (default 10MB)",
    )
    log_backup_count: int = Field(
        default=LOG_BACKUP_COUNT, description="Number of backup log files to keep"
    )

    # Format settings
    log_format: str = Field(
        default=LOG_FORMAT,
        description="Standard log format",
    )
    log_detailed_format: str = Field(
        default=LOG_DETAILED_FORMAT,
        description="Detailed log format",
    )
    log_fallback_format: str = Field(
        default=LOG_FALLBACK_FORMAT,
        description="Fallback log format",
    )

    # Enhanced configuration flags
    console_logging: bool = Field(
        default=LOG_CONSOLE_LOGGING, description="Whether to output logs to console"
    )
    structured_logging: bool = Field(
        default=LOG_STRUCTURED_LOGGING,
        description="Whether to use JSON structured logging",
    )
    async_logging: bool = Field(
        default=LOG_ASYNC_LOGGING, description="Whether to use asynchronous logging"
    )

    # Logger name
    log_name: str = Field(default=LOG_NAME, description="Name of the logger")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value):
        """Validate that log level is one of the allowed values."""
        allowed_levels = {
            LOG_LEVEL_DEBUG,
            LOG_LEVEL_INFO,
            LOG_LEVEL_WARNING,
            LOG_LEVEL_ERROR,
            LOG_LEVEL_CRITICAL,
        }
        if value.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {', '.join(allowed_levels)}")
        return value.upper()

    @field_validator("log_max_file_size")
    @classmethod
    def validate_log_max_file_size(cls, value):
        """Validate that log file size is positive."""
        if value <= 0:
            raise ValueError("Log max file size must be positive")
        if value > 1024 * 1024 * 1024:  # 1GB
            raise ValueError("Log max file size must not exceed 1GB")
        return value

    model_config = ConfigDict(
        extra="forbid",  # Don't allow extra fields
        str_strip_whitespace=True,  # Strip whitespace from string fields
    )
