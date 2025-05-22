"""Main entry point for the MetaExpert package."""

import sys

from metaexpert._argument import parse_arguments
from metaexpert.template_creator import create_expert_from_template


def main() -> None:
    """Main entry point for the MetaExpert package."""
    args = parse_arguments()

    # Check if the user wants to create a new expert file from template
    if args.new:
        create_expert_from_template(args.new)
        sys.exit(0)

    # Other functionality can be added here
    print("MetaExpert CLI")
    print(f"Arguments: {args}")


if __name__ == "__main__":
    main()
