"""Help system for MetaExpert CLI."""

import argparse


class HelpSystem:
    """Provides enhanced help functionality for the MetaExpert CLI."""

    # Command descriptions
    COMMAND_DESCRIPTIONS: dict[str, str] = {
        "new": "Create a new trading strategy from template",
        "run": "Run an existing trading strategy",
        "list": "List available trading strategies",
        "info": "Show information about MetaExpert library",
        "validate": "Validate a trading strategy file",
    }

    # Command usage examples
    USAGE_EXAMPLES: dict[str, list[str]] = {
        "new": [
            "metaexpert new my_strategy",
            "metaexpert new my_strategy --exchange bybit",
            "metaexpert new my_strategy --market-type spot --symbol ETHUSDT",
        ],
        "run": [
            "metaexpert run my_strategy.py",
            "metaexpert run my_strategy.py --mode live",
            "metaexpert run my_strategy.py --mode backtest --backtest-start 2024-01-01 --backtest-end 2024-12-31",
        ],
        "list": [
            "metaexpert list",
            "metaexpert list --path ./strategies",
            "metaexpert list --pattern strategy_*.py",
        ],
        "info": ["metaexpert info"],
        "validate": ["metaexpert validate my_strategy.py"],
    }

    @classmethod
    def get_command_help(cls, command: str) -> str:
        """Get detailed help for a specific command."""
        if command not in cls.COMMAND_DESCRIPTIONS:
            return f"Unknown command: {command}"

        help_text = f"Command: {command}\n"
        help_text += f"Description: {cls.COMMAND_DESCRIPTIONS[command]}\n\n"
        help_text += "Usage Examples:\n"

        for example in cls.USAGE_EXAMPLES.get(command, []):
            help_text += f"  {example}\n"

        return help_text

    @classmethod
    def get_full_help(cls) -> str:
        """Get full help text for all commands."""
        help_text = "MetaExpert Trading Library - Command Line Interface\n"
        help_text += "=" * 50 + "\n\n"

        help_text += "Available Commands:\n"
        for command, description in cls.COMMAND_DESCRIPTIONS.items():
            help_text += f"  {command:12} - {description}\n"

        help_text += "\nFor detailed help on a specific command, use: metaexpert <command> --help\n"
        help_text += "For general help, use: metaexpert --help\n"

        help_text += "\nCommon Options:\n"
        help_text += "  --help, -h    Show help message and exit\n"

        help_text += "\nExamples:\n"
        for command in cls.COMMAND_DESCRIPTIONS.keys():
            if command in cls.USAGE_EXAMPLES:
                for example in cls.USAGE_EXAMPLES[command][
                    :1
                ]:  # Show first example for each
                    help_text += f"  {example}\n"

        return help_text

    @classmethod
    def display_command_help(
        cls, command: str, parser: argparse.ArgumentParser | None = None
    ) -> None:
        """Display help for a specific command."""
        print(cls.get_command_help(command))
        if parser:
            parser.print_help()

    @classmethod
    def display_full_help(cls, parser: argparse.ArgumentParser | None = None) -> None:
        """Display full help."""
        print(cls.get_full_help())
        if parser:
            print("\n" + "=" * 50)
            parser.print_help()


def show_help(command: str | None = None) -> None:
    """Show help for the CLI."""
    help_system = HelpSystem()
    if command:
        print(help_system.get_command_help(command))
    else:
        print(help_system.get_full_help())


# For backward compatibility
def get_help_text(command: str | None = None) -> str:
    """Get help text (for integration with argument parser)."""
    help_system = HelpSystem()
    if command:
        return help_system.get_command_help(command)
    else:
        return help_system.get_full_help()
