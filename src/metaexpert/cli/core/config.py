# src/metaexpert/cli/core/config.py
"""CLI configuration management."""

import os
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CLIConfig(BaseSettings):
    """Global CLI configuration."""

    model_config = SettingsConfigDict(
        env_prefix="METAEXPERT_CLI_",
        env_file=".metaexpert",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    profile: str = Field(default="default", description="Configuration profile name")

    # Debug and logging settings
    debug: bool = Field(default=False, description="Enable debug mode")
    verbose: bool = Field(default=False, description="Verbose output")
    quiet: bool = Field(default=False, description="Suppress non-critical output")
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    log_file: Path | None = Field(default=None, description="Path to log file")
    log_max_size: str = Field(default="10MB", description="Maximum log file size")
    log_backup_count: int = Field(
        default=5, description="Number of log backups to keep"
    )

    # Output settings
    no_color: bool = Field(default=False, description="Disable colored output")
    output_format: str = Field(
        default="table", description="Default output format (table, json, csv)"
    )

    # Project settings
    default_exchange: str = Field(default="binance", description="Default exchange")
    default_strategy: str = Field(default="template", description="Default strategy")
    default_timeout: int = Field(
        default=30, description="Default timeout for operations in seconds"
    )

    # Process management
    pid_dir: Path = Field(default=Path.cwd(), description="PID files directory")
    pid_file_suffix: str = Field(default=".pid", description="PID file suffix")
    log_dir: Path = Field(default=Path("logs"), description="Logs directory")

    # Template settings
    template_dir: Path | None = Field(
        default=None, description="Custom template directory"
    )

    # Performance and caching
    cache_enabled: bool = Field(default=True, description="Enable caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")
    max_workers: int = Field(default=4, description="Maximum number of worker threads")

    # API and network settings
    api_timeout: int = Field(default=10, description="API request timeout in seconds")
    api_retries: int = Field(default=3, description="Number of API request retries")
    api_delay: float = Field(
        default=0.1, description="Delay between API requests in seconds"
    )

    @field_validator("pid_dir", "log_file", "template_dir")
    @classmethod
    def ensure_dir_exists(cls, v: Path | None) -> Path | None:
        """Ensure directory exists."""
        if v is not None:
            parent = v if v.suffix == "" else v.parent
            parent.mkdir(parents=True, exist_ok=True)
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()

    @classmethod
    def load(cls, profile: str | None = None) -> "CLIConfig":
        """Load configuration from environment and config file."""
        profile_name = profile or os.getenv("METAEXPERT_PROFILE", "default")
        config_file = Path.home() / ".metaexpert" / f"{profile_name}.env"

        if config_file.exists():
            # Create a temporary class with the specific config file
            temp_cls = type(
                "TempConfig",
                (BaseSettings,),
                {
                    "__module__": __name__,
                    "model_config": SettingsConfigDict(
                        env_prefix="METAEXPERT_CLI_",
                        env_file=config_file,
                        env_file_encoding="utf-8",
                        extra="ignore",
                    ),
                },
            )

            # Add all fields from the original class to the temporary class
            for field_name, field_info in cls.model_fields.items():
                setattr(temp_cls, field_name, field_info)

            temp_config = temp_cls()

            # Create the actual CLIConfig instance with values from temp config
            config_values = {}
            for field_name in cls.model_fields:
                if hasattr(temp_config, field_name):
                    config_values[field_name] = getattr(temp_config, field_name)

            # Ensure profile is set correctly
            config_values["profile"] = profile_name

            return cls(**config_values)

        return cls()

    def save(self, path: Path | None = None) -> None:
        """Save configuration to file."""
        if path is None:
            path = Path.cwd() / ".metaexpert"

        with open(path, "w") as f:
            for field, value in self.model_dump().items():
                # Convert Path objects to strings for saving
                if isinstance(value, Path):
                    value = (
                        value.as_posix()
                    )  # Use POSIX format for paths (with forward slashes)
                f.write(f"METAEXPERT_CLI_{field.upper()}={value}\n")

    def get_pid_file_path(self, project_name: str) -> Path:
        """Get PID file path for a specific project."""
        return self.pid_dir / f"{project_name}{self.pid_file_suffix}"

    def get_log_file_path(self, project_name: str) -> Path:
        """Get log file path for a specific project."""
        if self.log_file:
            return self.log_file
        return self.log_dir / f"{project_name}.log"
