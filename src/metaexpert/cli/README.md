# MetaExpert CLI Module

The CLI (Command Line Interface) module provides a comprehensive command-line interface for the MetaExpert trading library.

## Features

- **Create**: Generate new trading strategies from templates with customizable parameters
- **Run**: Execute trading strategies in different modes (paper, live, backtest)
- **List**: Discover available trading strategies in your project
- **Validate**: Check the syntax and structure of strategy files
- **Info**: Display information about the MetaExpert library

## Commands

### `new` - Create a new trading strategy

```bash
metaexpert new <name> [options]
```

**Options:**

- `--exchange`: Cryptocurrency exchange (binance, bybit, okx, bitget, kucoin)
- `--market-type`: Market type (spot, futures, options)
- `--symbol`: Trading symbol (e.g., BTCUSDT)
- `--timeframe`: Trading timeframe (e.g., 1h, 1d)
- `--output-dir`: Output directory (default: current directory)

**Example:**

```bash
metaexpert new my_strategy --exchange bybit --symbol ETHUSDT --timeframe 1h
```

### `run` - Execute a trading strategy

```bash
metaexpert run <file> [options]
```

**Options:**

- `--mode`: Trading mode (paper, live, backtest) - default: paper
- `--testnet`: Use testnet instead of live exchange
- `--backtest-start`: Start date for backtesting (YYYY-MM-DD)
- `--backtest-end`: End date for backtesting (YYYY-MM-DD)

**Example:**

```bash
metaexpert run my_strategy.py --mode live --testnet
metaexpert run my_strategy.py --mode backtest --backtest-start 2024-01-01 --backtest-end 2024-12-31
```

### `list` - List available trading strategies

```bash
metaexpert list [options]
```

**Options:**

- `--path`: Directory to search (default: current directory)
- `--pattern`: File pattern to match (default: *.py)

**Example:**

```bash
metaexpert list
metaexpert list --path ./strategies --pattern "*_strat.py"
```

### `validate` - Validate a strategy file

```bash
metaexpert validate <file>
```

**Example:**

```bash
metaexpert validate my_strategy.py
```

### `info` - Show library information

```bash
metaexpert info
```

## Validation

The CLI includes comprehensive input validation:

- Exchange names are validated against supported exchanges
- Market types are checked for validity
- Timeframes are validated for proper format
- File paths are checked for existence
- Date formats are validated as YYYY-MM-DD
- Symbol formats are validated

## Help System

Detailed help is available for all commands:

- `metaexpert --help` - Show general help
- `metaexpert <command> --help` - Show help for a specific command

## Architecture

The CLI module is organized into several components:

- `__init__.py` - Main entry point and command routing
- `argument_parser.py` - Advanced argument parsing with validation
- `commands.py` - Command-specific handlers
- `help.py` - Comprehensive help system
