"""Configuration for MetaExpert logger using Pydantic."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CONSOLE_LOGGING,
    LOG_FILE_LOGGING,
    LOG_LEVEL,
    LOG_LEVEL_TYPE,
    LOG_MAX_FILE_SIZE,
)


class LoggerConfig(BaseModel):
    """Configuration for MetaExpert structured logger."""

    # Core settings
    log_level: LOG_LEVEL_TYPE = Field(default=LOG_LEVEL, description="Global logging level")

    # Output destinations
    log_to_console: bool = Field(default=LOG_CONSOLE_LOGGING, description="Enable console output")
    log_to_file: bool = Field(default=LOG_FILE_LOGGING, description="Enable file output")

    # File settings
    log_dir: Path = Field(default=Path("logs"), description="Directory for log files")
    log_file: str = Field(default="expert.log", description="Main log file name")
    trade_log_file: str = Field(
        default="trades.log", description="Trade-specific log file"
    )
    error_log_file: str = Field(
        default="errors.log", description="Error-specific log file"
    )

    # Rotation settings
    max_bytes: int = Field(
        default=LOG_MAX_FILE_SIZE,  # 10 * 1024 * 1024 = 10MB
        description="Max file size before rotation",
    )
    backup_count: int = Field(default=LOG_BACKUP_COUNT, description="Number of backup files to keep")

    # Format settings
    use_colors: bool = Field(default=True, description="Use colored output in console")
    json_logs: bool = Field(default=False, description="Output logs in JSON format")

    # Performance settings
    cache_logger_on_first_use: bool = Field(
        default=True, description="Cache loggers for better performance"
    )

    @field_validator("log_dir")
    @classmethod
    def ensure_log_dir_exists(cls, path: Path) -> Path:
        """Create log directory if it doesn't exist."""
        path.mkdir(parents=True, exist_ok=True)
        return path

    @field_validator("max_bytes")
    @classmethod
    def validate_max_bytes(cls, value: int) -> int:
        """Validate file size limit."""
        if value <= 0:
            raise ValueError("max_bytes must be positive")
        if value > 1024 * 1024 * 1024:  # 1GB
            raise ValueError("max_bytes must not exceed 1GB")
        return value

    model_config = ConfigDict(frozen=True)  # Make config immutable after creation
