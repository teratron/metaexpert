from configparser import ConfigParser
from pathlib import Path


class ProjectConfig:
    """Configuration for specific project."""

    def __init__(self, project_path: Path):
        self.config_file = project_path / ".metaexpert.ini"
        self.config = ConfigParser()
        if self.config_file.exists():
            self.config.read(self.config_file)

    def get(self, section: str, key: str, default: str | None = None) -> str | None:
        """Get config value."""
        try:
            return self.config.get(section, key)
        except (KeyError, AttributeError):
            return default

    def set(self, section: str, key: str, value: str) -> None:
        """Set config value."""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save()

    def save(self) -> None:
        """Save config to file."""
        with open(self.config_file, "w") as f:
            self.config.write(f)
