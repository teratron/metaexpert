"""Configuration for MetaExpert logger using Pydantic."""

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CACHE_LOGGER_ON_FIRST_USE,
    LOG_CONSOLE_LOGGING,
    LOG_DIRECTORY,
    LOG_ERROR_FILE,
    LOG_FILE,
    LOG_FILE_LOGGING,
    LOG_LEVEL,
    LOG_LEVEL_TYPE,
    LOG_MAX_FILE_SIZE,
    LOG_STRUCTURED_LOGGING,
    LOG_TRADE_FILE,
    LOG_USE_COLORS,
)


class LoggerConfig(BaseModel):
    """Configuration for MetaExpert structured logger."""

    # Core settings
    log_level: LOG_LEVEL_TYPE = Field(
        default=LOG_LEVEL, description="Global logging level"
    )

    # Output destinations
    log_to_console: bool = Field(
        default=LOG_CONSOLE_LOGGING, description="Enable console output"
    )
    log_to_file: bool = Field(
        default=LOG_FILE_LOGGING, description="Enable file output"
    )

    # File settings
    log_dir: Path = Field(
        default=Path(LOG_DIRECTORY), description="Directory for log files"
    )
    log_file: str = Field(default=LOG_FILE, description="Main log file name")
    log_trade_file: str = Field(
        default=LOG_TRADE_FILE, description="Trade-specific log file"
    )
    log_error_file: str = Field(
        default=LOG_ERROR_FILE, description="Error-specific log file"
    )

    # Rotation settings
    max_bytes: int = Field(
        default=LOG_MAX_FILE_SIZE,  # 10 * 1024 * 1024 = 10MB
        description="Max file size before rotation",
    )
    backup_count: int = Field(
        default=LOG_BACKUP_COUNT, description="Number of backup files to keep"
    )

    # Format settings
    use_colors: bool = Field(
        default=LOG_USE_COLORS, description="Use colored output in console"
    )
    json_logging: bool = Field(
        default=LOG_STRUCTURED_LOGGING, description="Output logs in JSON format"
    )

    # Performance settings
    cache_logger_on_first_use: bool = Field(
        default=LOG_CACHE_LOGGER_ON_FIRST_USE,
        description="Cache loggers for better performance",
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

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        """Validate that at least one output (console or file) is enabled."""
        if not self.log_to_console and not self.log_to_file:
            raise ValueError("At least one output must be enabled: console or file")
        return self

    @classmethod
    def for_development(cls) -> Self:
        """Create a configuration preset for development: DEBUG level, colors enabled, JSON logs disabled."""
        return cls(
            log_level="DEBUG",
            use_colors=True,
            json_logging=False,
            log_to_console=True,
            log_to_file=True,
        )

    @classmethod
    def for_production(cls) -> Self:
        """Create a configuration preset for production: WARNING level, colors disabled, JSON logs enabled."""
        return cls(
            log_level="WARNING",
            use_colors=False,
            json_logging=True,
            log_to_console=False,
            log_to_file=True,
        )

    @classmethod
    def for_backtesting(cls) -> Self:
        """Create a configuration preset for backtesting: INFO level, console output disabled, JSON logs enabled."""
        return cls(
            log_level="INFO",
            use_colors=False,
            json_logging=True,
            log_to_console=False,
            log_to_file=True,
        )

    model_config = ConfigDict(frozen=True)  # Make config immutable after creation
