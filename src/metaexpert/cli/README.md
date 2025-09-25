# CLI Module (Command Line Interface)

## Description

The CLI (Command Line Interface) module provides a command-line interface for configuring and managing the trading bot. It includes argument parsing, validation, help generation, and template management commands.

## Module Structure

### [`__init__.py`](__init__.py)

The main interface of the CLI module. Provides functions for parsing command-line arguments and adding template commands.

#### Functions (`__init__.py`)

- `add_template_commands(parser)` - Adds template-related commands to the argument parser
- `parse_arguments()` - Parses command-line arguments and returns the parsed arguments
- `parse_cli_arguments(request)` - Entry point for parsing command-line arguments via HTTP

### [`argument_group_manager.py`](argument_group_manager.py)

Argument group manager for organizing command-line arguments.

#### Classes (`argument_group_manager.py`)

- `ArgumentGroup` - Represents a logical grouping of related command-line arguments
- `CommandLineArgument` - Represents a single command-line argument with its properties
- `ArgumentGroupManager` - Manages logical grouping of command-line arguments for better organization

#### Methods (`ArgumentGroupManager`)

- `add_group(name, description, order)` - Adds a new argument group
- `add_argument(arg)` - Adds a command-line argument to the manager
- `get_group_arguments(group_name)` - Gets all arguments belonging to a specific group
- `get_groups()` - Gets all argument groups, sorted by order
- `get_argument(name)` - Gets a specific argument by name

### [`argument_parser.py`](argument_parser.py)

Arguments parser for the trading bot.

#### Functions (`argument_parser.py`)

- `parse_arguments()` - Parses command-line arguments

### [`argument_validation.py`](argument_validation.py)

Argument validation utilities for command-line arguments.

#### Exception and Utilities

- `ArgumentValidationError` - Exception raised for argument validation errors
- `ArgumentValidationUtils` - Utilities for validating command-line argument values

#### Methods (`ArgumentValidationUtils`)

- `validate_exchange(exchange, valid_exchanges)` - Validates exchange value
- `validate_percentage(value, min_value, max_value)` - Validates percentage value
- `validate_positive_float(value)` - Validates that a float value is positive
- `validate_date_format(date_str)` - Validates date format (YYYY-MM-DD)
- `validate_trading_pair(pair)` - Validates trading pair format
- `validate_timeframe(timeframe)` - Validates timeframe format
- `validate_log_level(level)` - Validates log level
- `validate_trade_mode(mode)` - Validates trade mode
- `validate_market_type(market_type)` - Validates market type

### [`endpoint.py`](endpoint.py)

CLI endpoint for parsing command-line arguments.

#### Functions (`endpoint.py`)

- `parse_cli_arguments(request)` - Parses command-line arguments and returns the parsed configuration

### [`help_generator.py`](help_generator.py)

Help documentation generator for command-line arguments.

#### Classes

- `HelpDocumentationGenerator` - Generates user-facing documentation for command-line options and usage

#### Methods (`HelpDocumentationGenerator`)

- `generate_help_text(program_name, description)` - Generates comprehensive help text for all arguments
- `generate_group_help(group_name)` - Generates help text for a specific argument group
- `generate_usage_examples()` - Generates usage examples for common scenarios

### [`template_commands.py`](template_commands.py)

CLI commands for template creation and management.

#### Functions (`template_commands.py`)

- `create_template(args)` - Creates a new trading strategy template
- `list_exchanges(args)` - Lists supported exchanges
- `list_parameters(args)` - Lists configurable template parameters
- `validate_config(args)` - Validates configuration parameters
- `add_template_commands(parser)` - Adds template-related commands to the argument parser

## Usage

### Basic Usage

```bash
# Run the trading bot with basic parameters
python template.py --exchange binance --pair BTCUSDT --timeframe 1h

# Run in different modes
python template.py --trade-mode paper
python template.py --trade-mode backtest --start-date 2024-01-01 --end-date 2024-12-31
python template.py --trade-mode live --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET

# Configure risk management
python template.py --stop-loss 2.0 --take-profit 4.0 --size 0.1
```

### Template Creation

```bash
# Create a new trading strategy template
python -m metaexpert --new my_trading_strategy

# Use template commands
python template.py create my_strategy ./strategies
python template.py exchanges
python template.py parameters
python template.py validate param1=value1 param2=value2
```

## Argument Groups

Command-line arguments are organized into logical groups for better navigation:

1. **Core Configuration** - Basic settings for the trading system
2. **Trading Parameters** - Market and trading configuration
3. **Risk Management** - Position sizing and risk controls
4. **Backtesting** - Parameters for backtesting strategies
5. **Authentication** - API credentials and security settings
6. **Template Management** - Options for creating and managing expert templates
