"""Command-line interface module for MetaExpert."""

import sys
from importlib import import_module

from metaexpert.cli.argument_parser import parse_arguments as parse_cli_arguments
from metaexpert.cli.commands import (
    handle_info,
    handle_list,
    handle_new,
    handle_run,
    handle_validate,
)


def add_template_commands(parser) -> None:
    """Add template-related commands to the argument parser.

    This function is imported by __main__.py and should maintain this exact signature.
    """
    # This function is now implemented in argument_parser.py
    # The commands are added there for better validation capabilities
    pass


def main() -> None:
    """Main entry point for the CLI module."""
    try:
        args = parse_cli_arguments()

        # Check if a command was specified and execute the appropriate handler
        if args.command == "new":
            handle_new(args)
        elif args.command == "run":
            handle_run(args)
        elif args.command == "list":
            handle_list(args)
        elif args.command == "info":
            handle_info(args)
        elif args.command == "validate":
            handle_validate(args)
        else:
            # No command specified, show help
            # from metaexpert.cli.argument_parser import create_argument_parser

            create_argument_parser = import_module("metaexpert.cli.argument_parser").create_argument_parser
            create_argument_parser().print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except SystemExit:
        # argparse calls sys.exit, so we let it pass through
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
