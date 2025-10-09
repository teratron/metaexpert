"""Main entry point for the MetaExpert package."""

import sys

from metaexpert.cli import main as cli_main


def main() -> None:
    """Main entry point for the MetaExpert package."""
    # Delegate to the CLI module's main function
    cli_main()


if __name__ == "__main__":
    main()