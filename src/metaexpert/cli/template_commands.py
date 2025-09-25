"""CLI commands for template creation and management."""

import argparse
import sys

from metaexpert.services.config_service import ConfigurationManagementService
from metaexpert.template.template_service import TemplateCreationService


def create_template(args: argparse.Namespace) -> None:
    """Create a new trading strategy template.

    Args:
        args: Parsed command-line arguments
    """
    try:
        # Initialize the template creation service
        service = TemplateCreationService()

        # Prepare parameters from command-line arguments
        parameters = {}
        if args.exchange:
            parameters["exchange"] = args.exchange
        if args.symbol:
            parameters["symbol"] = args.symbol
        if args.timeframe:
            parameters["timeframe"] = args.timeframe

        # Create the template
        output_path = service.create_template(
            strategy_name=args.strategy_name,
            output_directory=args.output_directory,
            parameters=parameters if parameters else None
        )

        print(f"Created new trading strategy template: {output_path}")

    except Exception as e:
        print(f"Error creating template: {e}", file=sys.stderr)
        sys.exit(1)

def list_exchanges(args: argparse.Namespace) -> None:
    """List supported exchanges.

    Args:
        args: Parsed command-line arguments
    """
    try:
        # Initialize the template creation service
        service = TemplateCreationService()

        # Get supported exchanges
        exchanges = service.get_supported_exchanges()

        print("Supported exchanges:")
        for exchange in exchanges:
            print(f"  - {exchange}")

    except Exception as e:
        print(f"Error listing exchanges: {e}", file=sys.stderr)
        sys.exit(1)

def list_parameters(args: argparse.Namespace) -> None:
    """List configurable template parameters.

    Args:
        args: Parsed command-line arguments
    """
    try:
        # Initialize the configuration management service
        service = ConfigurationManagementService()

        # Get parameters with optional filtering
        parameters = service.get_configuration_parameters(
            category=args.category,
            exchange=args.exchange
        )

        print("Configurable template parameters:")
        for param in parameters:
            required_str = " (required)" if param.required else ""
            print(f"  - {param.name}: {param.description}{required_str}")
            print(f"    Default: {param.default_value}")
            if param.env_var_name:
                print(f"    Environment variable: {param.env_var_name}")
            if param.cli_arg_name:
                print(f"    CLI argument: {param.cli_arg_name}")
            print()

    except Exception as e:
        print(f"Error listing parameters: {e}", file=sys.stderr)
        sys.exit(1)

def validate_config(args: argparse.Namespace) -> None:
    """Validate configuration parameters.

    Args:
        args: Parsed command-line arguments
    """
    try:
        # Initialize the configuration management service
        service = ConfigurationManagementService()

        # Prepare parameters from command-line arguments
        parameters = {}
        if args.parameters:
            for param in args.parameters:
                if "=" in param:
                    key, value = param.split("=", 1)
                    parameters[key] = value
                else:
                    print(f"Invalid parameter format: {param}. Use key=value format.", file=sys.stderr)
                    sys.exit(1)

        # Validate the configuration
        result = service.validate_configuration(parameters)

        if result["valid"]:
            print("Configuration is valid")
        else:
            print("Configuration is invalid:")
            for error in result["errors"]:
                print(f"  - {error['parameter']}: {error['error']}")
            sys.exit(1)

    except Exception as e:
        print(f"Error validating configuration: {e}", file=sys.stderr)
        sys.exit(1)

def add_template_commands(parser: argparse.ArgumentParser) -> None:
    """Add template-related commands to the argument parser.

    Args:
        parser: Argument parser to add commands to
    """
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create template command
    create_parser = subparsers.add_parser('create', help='Create a new trading strategy template')
    create_parser.add_argument('strategy_name', help='Name of the strategy')
    create_parser.add_argument('output_directory', help='Directory to create the template in')
    create_parser.add_argument('--exchange', help='Exchange to configure for')
    create_parser.add_argument('--symbol', help='Trading pair symbol')
    create_parser.add_argument('--timeframe', help='Trading timeframe')
    create_parser.set_defaults(func=create_template)

    # List exchanges command
    exchanges_parser = subparsers.add_parser('exchanges', help='List supported exchanges')
    exchanges_parser.set_defaults(func=list_exchanges)

    # List parameters command
    parameters_parser = subparsers.add_parser('parameters', help='List configurable template parameters')
    parameters_parser.add_argument('--category', help='Filter by category')
    parameters_parser.add_argument('--exchange', help='Filter by exchange')
    parameters_parser.set_defaults(func=list_parameters)

    # Validate config command
    validate_parser = subparsers.add_parser('validate', help='Validate configuration parameters')
    validate_parser.add_argument('parameters', nargs='*', help='Parameters to validate in key=value format')
    validate_parser.set_defaults(func=validate_config)
