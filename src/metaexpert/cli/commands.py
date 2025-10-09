"""Command handlers for MetaExpert CLI."""

import sys
from argparse import Namespace
from pathlib import Path

from metaexpert.template import create_expert_from_template


def validate_strategy_file(file_path: str) -> bool:
    """Validate a trading strategy file."""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"Error: File '{file_path}' does not exist")
            return False

        if not path.suffix == ".py":
            print(f"Error: File '{file_path}' is not a Python file")
            return False

        # Try to parse the file to check for syntax errors
        with open(path, encoding="utf-8") as f:
            content = f.read()

        # Basic syntax check
        compile(content, path, "exec")

        # Check for required components (basic validation)
        required_components = [
            "from metaexpert import MetaExpert",
            "@expert.on_init",
            "def main() -> None:",
        ]

        missing_components = []
        for component in required_components:
            if component not in content:
                missing_components.append(component)

        if missing_components:
            print(
                f"Warning: The following required components are missing from '{file_path}':"
            )
            for component in missing_components:
                print(f"  - {component}")

        return True

    except SyntaxError as e:
        print(f"Syntax error in '{file_path}': {e}")
        return False
    except Exception as e:
        print(f"Error validating '{file_path}': {e}")
        return False


def handle_new(args: Namespace) -> None:
    """Handle the 'new' command to create a new trading strategy."""
    try:
        # Prepare parameters for template customization
        parameters = {
            "exchange": args.exchange,
            "market_type": args.market_type,
            "symbol": args.symbol,
            "timeframe": args.timeframe,
        }

        # Create the strategy file from template
        output_path = create_expert_from_template(
            file_path=f"{args.output_dir}/{args.name}", parameters=parameters
        )

        print(f"Successfully created new trading strategy: {output_path}")
        print(f"Exchange: {args.exchange}")
        print(f"Market type: {args.market_type}")
        print(f"Symbol: {args.symbol}")
        print(f"Timeframe: {args.timeframe}")
        print("\nTo run the strategy:")
        print(f"  python -m metaexpert run {output_path}")

    except Exception as e:
        print(f"Error creating new strategy: {e}")
        sys.exit(1)


def handle_run(args: Namespace) -> None:
    """Handle the 'run' command to execute a trading strategy."""
    try:
        strategy_path = Path(args.file)

        if not strategy_path.exists():
            print(f"Error: Strategy file '{args.file}' does not exist")
            sys.exit(1)

        # Validate the strategy file before running
        if not validate_strategy_file(str(strategy_path)):
            print("Cannot run strategy due to validation errors")
            sys.exit(1)

        # For now, we'll just simulate running the strategy
        # In a real implementation, this would import and execute the strategy
        print(f"Running strategy from: {strategy_path}")
        print(f"Mode: {args.mode}")
        if args.testnet:
            print("Using testnet")
        if args.backtest_start:
            print(f"Backtest start: {args.backtest_start}")
        if args.backtest_end:
            print(f"Backtest end: {args.backtest_end}")

        # In a real implementation, we would execute the strategy file here
        print(
            "Note: This is a simulation. In a real implementation, the strategy would be executed."
        )

    except Exception as e:
        print(f"Error running strategy: {e}")
        sys.exit(1)


def handle_list(args: Namespace) -> None:
    """Handle the 'list' command to list available trading strategies."""
    try:
        search_path = Path(args.path)
        if not search_path.exists():
            print(f"Error: Path '{args.path}' does not exist")
            sys.exit(1)

        # Find strategy files matching the pattern
        pattern = args.pattern
        if not pattern.endswith(".py"):
            pattern += ".py"  # Only look for Python files by default

        strategy_files = list(search_path.glob(pattern))

        if not strategy_files:
            print(
                f"No strategy files found in '{args.path}' with pattern '{args.pattern}'"
            )
            return

        print(f"Found {len(strategy_files)} strategy file(s) in '{args.path}':")
        for i, file_path in enumerate(sorted(strategy_files), 1):
            print(f"  {i}. {file_path.name}")

    except Exception as e:
        print(f"Error listing strategies: {e}")
        sys.exit(1)


def handle_info(args: Namespace) -> None:
    """Handle the 'info' command to display MetaExpert information."""
    from metaexpert import __version__ as version

    print("MetaExpert Trading Library")
    print("==========================")
    print(f"Version: {version}")
    print("A Python-based trading library for cryptocurrency exchanges")
    print("\nSupported Exchanges:")
    print("  - Binance")
    print("  - Bybit")
    print("  - OKX")
    print("  - Bitget")
    print("  - KuCoin")
    print("\nFeatures:")
    print("  - Unified API for multiple exchanges")
    print("  - Event-driven trading strategies")
    print("  - Risk management tools")
    print("  - Paper trading and backtesting")


def handle_validate(args: Namespace) -> None:
    """Handle the 'validate' command to validate a strategy file."""
    is_valid = validate_strategy_file(args.file)
    if is_valid:
        print(f"✓ Strategy file '{args.file}' is valid")
    else:
        print(f"✗ Strategy file '{args.file}' has validation issues")
        sys.exit(1)
