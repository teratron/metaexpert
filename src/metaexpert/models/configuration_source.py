"""ConfigurationSource model representing a source of configuration values."""

from dataclasses import dataclass


@dataclass
class ConfigurationSource:
    """Represents a source of configuration values.

    Attributes:
        type: Type of configuration source (environment, cli, file, default)
        priority: Priority order for applying configuration values
        description: Description of the configuration source
    """

    type: str
    priority: int
    description: str

    def __post_init__(self) -> None:
        """Validate the configuration source after initialization."""
        if not self.type:
            raise ValueError("Configuration source type cannot be empty")
        if self.priority < 0:
            raise ValueError("Configuration source priority must be non-negative")
        if not self.description:
            raise ValueError("Configuration source description cannot be empty")
