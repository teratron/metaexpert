"""StrategyParameter model representing a strategy-specific parameter in the template."""

from dataclasses import dataclass


@dataclass
class StrategyParameter:
    """Represents a strategy-specific parameter in the template.

    Attributes:
        name: Name of the parameter
        description: Description of what the parameter does
        default_value: Default value of the parameter
        category: Category/group the parameter belongs to
        required: Whether the parameter is required
    """

    name: str
    description: str
    default_value: str
    category: str
    required: bool

    def __post_init__(self) -> None:
        """Validate the strategy parameter after initialization."""
        if not self.name:
            raise ValueError("Strategy parameter name cannot be empty")
        if not self.description:
            raise ValueError("Strategy parameter description cannot be empty")
        if not self.category:
            raise ValueError("Strategy parameter category cannot be empty")
