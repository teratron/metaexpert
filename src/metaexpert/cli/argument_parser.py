"""Argument parsing utilities for MetaExpert CLI."""

import argparse
from pathlib import Path


class ArgumentParserError(Exception):
    """Custom exception for argument parser errors."""

    pass


class MetaExpertArgumentParser(argparse.ArgumentParser):
    """Custom argument parser for MetaExpert with enhanced validation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_rules = {}

    def add_argument_with_validation(
        self, *args, validation_func=None, validation_message=None, **kwargs
    ):
        """Add an argument with custom validation function."""
        dest = kwargs.get("dest")
        if dest is None:
            # Extract dest from args (e.g., '--exchange' -> 'exchange')
            for arg in args:
                if arg.startswith("--"):
                    dest = arg[2:].replace("-", "_")
                    break
                elif arg.startswith("-"):
                    dest = arg[1:]
                    break

        if dest:
            self.validation_rules[dest] = {
                "func": validation_func,
                "message": validation_message,
            }

        return super().add_argument(*args, **kwargs)

    def parse_args(self, args=None, namespace=None):
        """Parse arguments and run validations."""
        parsed_args = super().parse_args(args, namespace)

        # Run validations
        for attr_name, validation_info in self.validation_rules.items():
            if hasattr(parsed_args, attr_name):
                value = getattr(parsed_args, attr_name)
                validation_func = validation_info["func"]
                validation_message = validation_info["message"]

                if validation_func and not validation_func(value):
                    error_msg = (
                        validation_message
                        or f"Invalid value for argument {attr_name}: {value}"
                    )
                    raise ArgumentParserError(error_msg)

        return parsed_args


def validate_exchange(value: str) -> bool:
    """Validate exchange name."""
    valid_exchanges = {"binance", "bybit", "okx", "bitget", "kucoin"}
    return value.lower() in valid_exchanges


def validate_market_type(value: str) -> bool:
    """Validate market type."""
    valid_types = {"spot", "futures", "options"}
    return value.lower() in valid_types


def validate_timeframe(value: str) -> bool:
    """Validate timeframe format."""
    valid_timeframes = {
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    }
    return value.lower() in valid_timeframes


def validate_symbol(value: str) -> bool:
    """Validate symbol format (e.g., BTCUSDT)."""
    import re

    # Basic pattern: uppercase letters, numbers, and optionally a separator like BTCUSDT
    pattern = r"^[A-Z0-9]+(?:[A-Z0-9]+)+$"
    return bool(re.match(pattern, value))


def validate_trade_mode(value: str) -> bool:
    """Validate trade mode."""
    valid_modes = {"paper", "live", "backtest"}
    return value.lower() in valid_modes


def validate_date_format(value: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    import re
    from datetime import datetime

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return False

    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_file_path(value: str) -> bool:
    """Validate file path exists and is accessible."""
    try:
        path = Path(value)
        return path.exists() and path.is_file()
    except (OSError, TypeError):
        return False


def validate_directory_path(value: str) -> bool:
    """Validate directory path exists and is accessible."""
    try:
        path = Path(value)
        return path.exists() and path.is_dir()
    except (OSError, TypeError):
        return False


def validate_positive_number(value: str) -> bool:
    """Validate that value is a positive number."""
    try:
        num = float(value)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_percentage(value: str) -> bool:
    """Validate that value is a percentage (0-100)."""
    try:
        num = float(value)
        return 0 <= num <= 100
    except (ValueError, TypeError):
        return False


class MetaExpertArgumentValidator:
    """Validator class for MetaExpert specific arguments."""

    @staticmethod
    def validate_new_command_args(args: argparse.Namespace) -> list[str]:
        """Validate arguments for the 'new' command."""
        errors = []

        # Validate strategy name
        if not args.name or not args.name.strip():
            errors.append("Strategy name cannot be empty")

        errors.extend(MetaExpertArgumentValidator._validate_exchange_arg(args))
        errors.extend(MetaExpertArgumentValidator._validate_market_type_arg(args))
        errors.extend(MetaExpertArgumentValidator._validate_symbol_arg(args))
        errors.extend(MetaExpertArgumentValidator._validate_timeframe_arg(args))
        errors.extend(MetaExpertArgumentValidator._validate_output_dir_arg(args))

        return errors

    @staticmethod
    def _validate_exchange_arg(args: argparse.Namespace) -> list[str]:
        """Validate exchange argument."""
        errors = []
        if hasattr(args, "exchange") and args.exchange:
            if not validate_exchange(args.exchange):
                errors.append(
                    f"Invalid exchange: {args.exchange}. Valid options: binance, bybit, okx, bitget, kucoin"
                )
        return errors

    @staticmethod
    def _validate_market_type_arg(args: argparse.Namespace) -> list[str]:
        """Validate market type argument."""
        errors = []
        if hasattr(args, "market_type") and args.market_type:
            if not validate_market_type(args.market_type):
                errors.append(
                    f"Invalid market type: {args.market_type}. Valid options: spot, futures, options"
                )
        return errors

    @staticmethod
    def _validate_symbol_arg(args: argparse.Namespace) -> list[str]:
        """Validate symbol argument."""
        errors = []
        if hasattr(args, "symbol") and args.symbol:
            if not validate_symbol(args.symbol):
                errors.append(
                    f"Invalid symbol format: {args.symbol}. Use format like BTCUSDT"
                )
        return errors

    @staticmethod
    def _validate_timeframe_arg(args: argparse.Namespace) -> list[str]:
        """Validate timeframe argument."""
        errors = []
        if hasattr(args, "timeframe") and args.timeframe:
            if not validate_timeframe(args.timeframe):
                errors.append(
                    f"Invalid timeframe: {args.timeframe}. Valid options: 1m, 5m, 1h, 1d, etc."
                )
        return errors

    @staticmethod
    def _validate_output_dir_arg(args: argparse.Namespace) -> list[str]:
        """Validate output directory argument."""
        errors = []
        if hasattr(args, "output_dir") and args.output_dir:
            if not validate_directory_path(args.output_dir):
                errors.append(f"Output directory does not exist: {args.output_dir}")
        return errors

    @staticmethod
    def validate_run_command_args(args: argparse.Namespace) -> list[str]:
        """Validate arguments for the 'run' command."""
        errors = []

        # Validate strategy file
        if not args.file or not args.file.strip():
            errors.append("Strategy file path cannot be empty")
        elif not validate_file_path(args.file):
            errors.append(f"Strategy file does not exist: {args.file}")

        # Validate trade mode if provided
        if hasattr(args, "mode") and args.mode:
            if not validate_trade_mode(args.mode):
                errors.append(
                    f"Invalid trade mode: {args.mode}. Valid options: paper, live, backtest"
                )

        # Validate backtest dates if provided
        if hasattr(args, "backtest_start") and args.backtest_start:
            if not validate_date_format(args.backtest_start):
                errors.append(
                    f"Invalid backtest start date format: {args.backtest_start}. Use YYYY-MM-DD"
                )

        if hasattr(args, "backtest_end") and args.backtest_end:
            if not validate_date_format(args.backtest_end):
                errors.append(
                    f"Invalid backtest end date format: {args.backtest_end}. Use YYYY-MM-DD"
                )

        return errors

    @staticmethod
    def validate_list_command_args(args: argparse.Namespace) -> list[str]:
        """Validate arguments for the 'list' command."""
        errors = []

        # Validate path if provided
        if hasattr(args, "path") and args.path:
            if not validate_directory_path(args.path):
                errors.append(f"Directory does not exist: {args.path}")

        return errors


def create_argument_parser() -> MetaExpertArgumentParser:
    """Create a configured argument parser for MetaExpert CLI."""
    parser = MetaExpertArgumentParser(
        prog="metaexpert",
        description="MetaExpert Trading Library - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    return parser


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments with validation."""
    parser = create_argument_parser()

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # New command
    new_parser = subparsers.add_parser(
        "new",
        help="Create a new trading strategy from template",
        description="Create a new trading strategy file from the standard template",
    )
    new_parser.add_argument(
        "name", help="Name of the new trading strategy (without .py extension)"
    )
    new_parser.add_argument_with_validation(
        "--exchange",
        choices=["binance", "bybit", "okx", "bitget", "kucoin"],
        default="binance",
        validation_func=validate_exchange,
        validation_message="Invalid exchange. Valid options: binance, bybit, okx, bitget, kucoin",
        help="Cryptocurrency exchange to use (default: binance)",
    )
    new_parser.add_argument_with_validation(
        "--market-type",
        choices=["spot", "futures", "options"],
        default="futures",
        validation_func=validate_market_type,
        validation_message="Invalid market type. Valid options: spot, futures, options",
        help="Type of financial instruments (default: futures)",
    )
    new_parser.add_argument_with_validation(
        "--symbol",
        default="BTCUSDT",
        validation_func=validate_symbol,
        validation_message="Invalid symbol format. Use format like BTCUSDT",
        help="Trading symbol (default: BTCUSDT)",
    )
    new_parser.add_argument_with_validation(
        "--timeframe",
        default="1h",
        validation_func=validate_timeframe,
        validation_message="Invalid timeframe. Valid options: 1m, 5m, 1h, 1d, etc.",
        help="Trading timeframe (default: 1h)",
    )
    new_parser.add_argument_with_validation(
        "--output-dir",
        default=".",
        validation_func=validate_directory_path,
        validation_message="Output directory does not exist",
        help="Output directory for the new strategy file (default: current directory)",
    )

    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run an existing trading strategy",
        description="Execute an existing trading strategy file",
    )
    run_parser.add_argument_with_validation(
        "file",
        validation_func=validate_file_path,
        validation_message="Strategy file does not exist",
        help="Path to the trading strategy file to run",
    )
    run_parser.add_argument_with_validation(
        "--mode",
        choices=["paper", "live", "backtest"],
        default="paper",
        validation_func=validate_trade_mode,
        validation_message="Invalid trade mode. Valid options: paper, live, backtest",
        help="Trading mode: paper (simulated), live (real trading), or backtest (default: paper)",
    )
    run_parser.add_argument(
        "--testnet", action="store_true", help="Use testnet instead of live exchange"
    )
    run_parser.add_argument_with_validation(
        "--backtest-start",
        validation_func=validate_date_format,
        validation_message="Invalid date format. Use YYYY-MM-DD",
        help="Start date for backtesting (format: YYYY-MM-DD)",
    )
    run_parser.add_argument_with_validation(
        "--backtest-end",
        validation_func=validate_date_format,
        validation_message="Invalid date format. Use YYYY-MM-DD",
        help="End date for backtesting (format: YYYY-MM-DD)",
    )

    # List command
    list_parser = subparsers.add_parser(
        "list",
        help="List available trading strategies",
        description="List trading strategy files in the current directory or specified path",
    )
    list_parser.add_argument_with_validation(
        "--path",
        default=".",
        validation_func=validate_directory_path,
        validation_message="Directory does not exist",
        help="Directory path to search for strategy files (default: current directory)",
    )
    list_parser.add_argument(
        "--pattern", default="*.py", help="File pattern to match (default: *.py)"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a trading strategy file",
        description="Validate the structure and syntax of a trading strategy file",
    )
    validate_parser.add_argument_with_validation(
        "file",
        validation_func=validate_file_path,
        validation_message="Strategy file does not exist",
        help="Path to the trading strategy file to validate",
    )

    # Info command
    subparsers.add_parser(
        "info",
        help="Show information about MetaExpert library",
        description="Display version and information about the MetaExpert library",
    )

    # Parse and validate arguments
    try:
        args = parser.parse_args()

        # Additional validation based on command
        validator = MetaExpertArgumentValidator()
        errors = []

        if args.command == "new":
            errors = validator.validate_new_command_args(args)
        elif args.command == "run":
            errors = validator.validate_run_command_args(args)
        elif args.command == "list":
            errors = validator.validate_list_command_args(args)

        if errors:
            for error in errors:
                print(f"Error: {error}")
            parser.print_usage()
            exit(1)

        return args

    except ArgumentParserError as e:
        print(f"Argument error: {e}")
        parser.print_usage()
        exit(1)
    except SystemExit:
        # Let argparse handle its own exits (like --help)
        raise
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        parser.print_usage()
        exit(1)
