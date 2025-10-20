"""Configuration for MetaExpert logger using Pydantic."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LoggerConfig(BaseModel):
    """Configuration for MetaExpert logger."""

    # Log levels
    log_level: str = Field(
        default="DEBUG",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_trade_level: str = Field(default="INFO", description="Trade-specific log level")
    log_error_level: str = Field(
        default="ERROR", description="Error-specific log level"
    )

    # File names
    log_file: str = Field(default="expert.log", description="Main log file name")
    trade_log_file: str = Field(
        default="trades.log", description="Trade-specific log file name"
    )
    error_log_file: str = Field(
        default="errors.log", description="Error-specific log file name"
    )

    # Directory configuration
    log_directory: str = Field(default="logs", description="Directory for log files")

    # File rotation settings
    log_max_file_size: int = Field(
        default=10485760, description="Maximum log file size in bytes (default 10MB)"
    )
    log_backup_count: int = Field(
        default=5, description="Number of backup log files to keep"
    )

    # Format settings
    log_format: str = Field(
        default="[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
        description="Standard log format",
    )
    log_detailed_format: str = Field(
        default="[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s",
        description="Detailed log format",
    )
    log_fallback_format: str = Field(
        default="[%(asctime)s] %(levelname)s: (LOGGING-FALLBACK) %(message)s",
        description="Fallback log format",
    )

    # Enhanced configuration flags
    log_console_logging: bool = Field(
        default=True, description="Whether to output logs to console"
    )
    log_structured_logging: bool = Field(
        default=False, description="Whether to use JSON structured logging"
    )
    log_async_logging: bool = Field(
        default=False, description="Whether to use asynchronous logging"
    )

    # Logger name
    log_name: str = Field(default="MetaExpert", description="Name of the logger")

    @field_validator("log_level")
    def validate_log_level(cls, value):
        """Validate that log level is one of the allowed values."""
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if value.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {', '.join(allowed_levels)}")
        return value.upper()

    @field_validator("log_max_file_size")
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
