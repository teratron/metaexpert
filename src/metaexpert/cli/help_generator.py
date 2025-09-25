"""Help documentation generator for CLI arguments."""

from metaexpert.cli.argument_group_manager import ArgumentGroupManager


class HelpDocumentationGenerator:
    """Generates user-facing documentation for command-line options and usage."""

    def __init__(self, group_manager: ArgumentGroupManager):
        """Initialize the help documentation generator.

        Args:
            group_manager: ArgumentGroupManager instance
        """
        self.group_manager = group_manager

    @staticmethod
    def _format_argument_display(arg) -> str:
        """Format argument display string based on argument properties.

        Args:
            arg: Argument object with properties like name, short_name, type, choices

        Returns:
            Formatted argument display string
        """
        if arg.short_name:
            arg_display = f"  {arg.short_name}, --{arg.name}"
        else:
            arg_display = f"  --{arg.name}"

        # Add type and choices information
        if arg.type != "string":
            arg_display += f" {arg.type.upper()}"
        if arg.choices:
            arg_display += f" {{{', '.join(arg.choices)}}}"

        return arg_display

    def _add_argument_to_help_text(self, help_text: str, arg) -> str:
        """Add argument information to help text with proper formatting.

        Args:
            help_text: Current help text being built
            arg: Argument object with properties like help_text, default_value

        Returns:
            Updated help text with argument information added
        """
        arg_display = self._format_argument_display(arg)
        help_text += f"{arg_display:<30} {arg.help_text}\n"

        # Add default value if present
        if arg.default_value is not None:
            help_text += f"{'':<30} (default: {arg.default_value})\n"
        return help_text

    def generate_help_text(
        self,
        program_name: str = "metaexpert",
        description: str = "Expert Trading System",
    ) -> str:
        """Generate comprehensive help text for all arguments.

        Args:
            program_name: Name of the program
            description: Overall description of the program

        Returns:
            Formatted help text as string
        """
        help_text = f"usage: {program_name} [-h] [options]\n\n{description}\n\n"

        # Add global options section
        help_text += "optional arguments:\n"
        help_text += "  -h, --help            show this help message and exit\n\n"

        # Add grouped arguments
        for group in self.group_manager.get_groups():
            help_text += f"{group.name}:\n"
            help_text += f"  {group.description}\n"

            # Get arguments for this group
            group_args = self.group_manager.get_group_arguments(group.name)
            if group_args:
                for arg in group_args:
                    help_text = self._add_argument_to_help_text(help_text, arg)
            else:
                help_text += "  No arguments in this group.\n"

            help_text += "\n"

        return help_text

    def generate_group_help(self, group_name: str) -> str:
        """Generate help text for a specific argument group.

        Args:
            group_name: Name of the group to generate help for

        Returns:
            Formatted help text for the group
        """
        group = self.group_manager.groups.get(group_name)
        if not group:
            return f"Group '{group_name}' not found."

        help_text = f"{group.name}:\n"
        help_text += f"  {group.description}\n\n"

        # Get arguments for this group
        group_args = self.group_manager.get_group_arguments(group_name)
        if group_args:
            for arg in group_args:
                help_text = self._add_argument_to_help_text(help_text, arg)
        else:
            help_text += "  No arguments in this group.\n"

        return help_text

    @staticmethod
    def generate_usage_examples() -> str:
        """Generate usage examples for common scenarios.

        Returns:
            Formatted usage examples as string
        """
        examples = """
Examples:
 # Create a new trading strategy
  metaexpert --new my_trading_strategy

  # Run a trading strategy with specific parameters
  python template.py --exchange binance --pair BTCUSDT --timeframe 1h

  # Run in different modes
  python template.py --trade-mode paper
  python template.py --trade-mode backtest --start-date 2024-01-01 --end-date 2025-12-31
  python template.py --trade-mode live --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET

  # Configure risk management
  python template.py --stop-loss 2.0 --take-profit 4.0 --size 0.1
        """.strip()

        return examples
