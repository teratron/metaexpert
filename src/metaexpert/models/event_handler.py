"""EventHandler model representing an event handler function in the template."""

from dataclasses import dataclass


@dataclass
class EventHandler:
    """Represents an event handler function in the template.

    Attributes:
        name: Name of the event handler function
        description: Description of when the handler is called
        parameters: List of parameters the handler accepts
        decorator: The decorator used to register the handler
    """

    name: str
    description: str
    parameters: list[str]
    decorator: str

    def __post_init__(self) -> None:
        """Validate the event handler after initialization."""
        if not self.name:
            raise ValueError("Event handler name cannot be empty")
        if not self.description:
            raise ValueError("Event handler description cannot be empty")
        if not self.decorator:
            raise ValueError("Event handler decorator cannot be empty")
