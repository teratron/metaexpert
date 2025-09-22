"""Exchange model representing a supported exchange."""

from dataclasses import dataclass


@dataclass
class Exchange:
    """Represents a supported exchange.

    Attributes:
        name: Name of the exchange
        supported_features: List of features supported by the exchange
        api_documentation_url: URL to the exchange's API documentation
        requires_passphrase: Whether the exchange requires an API passphrase
    """

    name: str
    supported_features: list[str]
    api_documentation_url: str
    requires_passphrase: bool

    def __post_init__(self) -> None:
        """Validate the exchange after initialization."""
        if not self.name:
            raise ValueError("Exchange name cannot be empty")
        if not self.api_documentation_url:
            raise ValueError("Exchange API documentation URL cannot be empty")
