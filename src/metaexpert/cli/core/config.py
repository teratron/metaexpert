# src/metaexpert/cli/core/config.py
"""CLI configuration management."""

from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CLIConfig(BaseSettings):
    """Global CLI configuration."""

    model_config = SettingsConfigDict(
        env_prefix="METAEXPERT_CLI_",
        env_file=".metaexpert",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Output settings
    verbose: bool = Field(default=False, description="Verbose output")
    no_color: bool = Field(default=False, description="Disable colored output")
    output_format: str = Field(default="table", description="Default output format")

    # Project settings
    default_exchange: str = Field(default="binance", description="Default exchange")
    default_strategy: str = Field(default="template", description="Default strategy")

    # Process management
    pid_dir: Path = Field(default=Path.cwd(), description="PID files directory")
    log_dir: Path = Field(default=Path("logs"), description="Logs directory")

    # Template settings
    template_dir: Optional[Path] = Field(
        default=None, description="Custom template directory"
    )

    @field_validator("pid_dir", "log_dir")
    @classmethod
    def ensure_dir_exists(cls, v: Path) -> Path:
        """Ensure directory exists."""
        v.mkdir(parents=True, exist_ok=True)
        return v

    @classmethod
    def load(cls) -> "CLIConfig":
        """Load configuration from environment and config file."""
        return cls()

    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if path is None:
            path = Path.cwd() / ".metaexpert"

        with open(path, "w") as f:
            for field, value in self.model_dump().items():
                if value is not None:
                    f.write(f"METAEXPERT_CLI_{field.upper()}={value}\n")

