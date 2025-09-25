"""Argument group manager for organizing CLI arguments."""

from dataclasses import dataclass


@dataclass
class ArgumentGroup:
    """Represents a logical grouping of related command-line arguments."""

    name: str
    description: str
    order: int = 0


@dataclass
class CommandLineArgument:
    """Represents a single command-line argument with its properties."""

    name: str
    short_name: str | None = None
    type: str = "string"
    default_value: str | None = None
    choices: list[str] | None = None
    required: bool = False
    help_text: str = ""
    group: str = ""
    deprecated: bool = False


class ArgumentGroupManager:
    """Manages logical grouping of command-line arguments for better organization."""

    def __init__(self):
        """Initialize the argument group manager."""
        self.groups: dict[str, ArgumentGroup] = {}
        self.arguments: dict[str, CommandLineArgument] = {}

    def add_group(self, name: str, description: str, order: int = 0) -> None:
        """Add a new argument group.

        Args:
            name: Name of the argument group
            description: Description of what arguments in this group control
            order: Display order for the group in help documentation
        """
        self.groups[name] = ArgumentGroup(name, description, order)

    def add_argument(self, arg: CommandLineArgument) -> None:
        """Add a command-line argument to the manager.

        Args:
            arg: CommandLineArgument object to add
        """
        self.arguments[arg.name] = arg
        # Ensure the group exists
        if arg.group and arg.group not in self.groups:
            self.add_group(arg.group, f"Group for {arg.group} arguments")

    def get_group_arguments(self, group_name: str) -> list[CommandLineArgument]:
        """Get all arguments belonging to a specific group.

        Args:
            group_name: Name of the group

        Returns:
            List of CommandLineArgument objects in the group
        """
        return [arg for arg in self.arguments.values() if arg.group == group_name]

    def get_groups(self) -> list[ArgumentGroup]:
        """Get all argument groups, sorted by order.

        Returns:
            List of ArgumentGroup objects sorted by order
        """
        return sorted(self.groups.values(), key=lambda g: g.order)

    def get_argument(self, name: str) -> CommandLineArgument | None:
        """Get a specific argument by name.

        Args:
            name: Name of the argument

        Returns:
            CommandLineArgument object or None if not found
        """
        return self.arguments.get(name)
