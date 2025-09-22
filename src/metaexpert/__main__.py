"""Main entry point for the MetaExpert package."""

import argparse
import sys

from metaexpert._argument import parse_arguments
from metaexpert.template_creator import create_expert_from_template
from metaexpert.cli.template_commands import add_template_commands


def main() -> None:
    """Main entry point for the MetaExpert package."""
    # Create the main argument parser
    parser = argparse.ArgumentParser(description="MetaExpert Trading Library")
    
    # Add existing arguments
    # Note: We're simplifying this for now. In a real implementation, 
    # we would integrate the existing argument parsing with the new commands.
    
    # Add template-related commands
    add_template_commands(parser)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if a template command was specified
    if hasattr(args, 'func'):
        # Execute the appropriate command
        args.func(args)
        sys.exit(0)
    
    # Check if the user wants to create a new expert file from template (legacy)
    if hasattr(args, 'new') and args.new:
        create_expert_from_template(args.new)
        sys.exit(0)

    # Other functionality can be added here
    print("MetaExpert CLI")
    print(f"Arguments: {args}")


if __name__ == "__main__":
    main()
