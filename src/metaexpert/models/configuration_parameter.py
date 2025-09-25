"""ConfigurationParameter model representing a configuration parameter in the template."""

from dataclasses import dataclass


@dataclass
class ConfigurationParameter:
    """Represents a configuration parameter in the template.

    Attributes:
        name: Name of the parameter
        description: Description of what the parameter does
        default_value: Default value of the parameter
        category: Category/group the parameter belongs to
        required: Whether the parameter is required
        env_var_name: Corresponding environment variable name
        cli_arg_name: Corresponding command-line argument name
    """

    name: str
    description: str
    default_value: str
    category: str
    required: bool
    env_var_name: str | None = None
    cli_arg_name: str | None = None

    def __post_init__(self) -> None:
        """Validate the configuration parameter after initialization."""
        if not self.name:
            raise ValueError("Configuration parameter name cannot be empty")
        if not self.description:
            raise ValueError("Configuration parameter description cannot be empty")
        if not self.category:
            raise ValueError("Configuration parameter category cannot be empty")
