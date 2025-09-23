# MetaExpert Command Line Interface

## Basic Commands

The MetaExpert package provides a command line interface (CLI) for convenient use of various functions. The CLI has been enhanced with logical argument grouping for better organization and usability.

### Creating a New Expert from Template

To create a new expert file based on a template, use the `--new` argument:

```bash
metaexpert --new my_expert
```

This command will create a new file `my_expert.py` in the current directory, using the `template.py` template.

You can also specify a directory path directly in the file path:

```bash
metaexpert --new ./experts/my_expert
```

This command will create a new file `my_expert.py` in the `./experts` directory.

### Argument Groups

The CLI arguments are now organized into logical groups for better navigation:

#### Core Configuration
Basic settings for the trading system:
- `--log-level`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

#### Trading Parameters
Market and trading configuration:
- `--exchange`: Select the exchange to trade on
- `--trade-mode`: Set trading mode (backtest, paper, live)
- `--market-type`: Set market type (spot, futures, options, margin)
- `--contract-type`: Set contract type for futures (usd_m, coin_m)
- `--pair`: Set the trading pair (e.g., BTCUSDT)
- `--timeframe`: Set the trading timeframe

#### Risk Management
Position sizing and risk controls:
- `--size`: Set maximum position size
- `--stop-loss`: Set stop loss percentage
- `--take-profit`: Set take profit percentage
- `--trailing-stop`: Set trailing stop percentage

#### Backtesting
Parameters for backtesting strategies:
- `--start-date`: Set backtest start date
- `--end-date`: Set backtest end date
- `--balance`: Set initial balance for backtesting
- `--output`: Set output file for backtest results

#### Authentication
API credentials and security settings:
- `--api-key`: Set API key for exchange authentication
- `--api-secret`: Set API secret for exchange authentication
- `--base-url`: Set base URL for the exchange API

#### Template Management
Options for creating and managing expert templates:
- `--new`: Create a new expert file from template

### Group-Specific Help

You can get help for specific argument groups:

```bash
# Get help for core configuration
metaexpert --help

# Get help for trading parameters
metaexpert --help trading

# Get help for risk management
metaexpert --help risk
```

### Other Command Line Arguments

MetaExpert supports various arguments for configuring trading parameters:

```bash
metaexpert --exchange binance --trade-mode paper --market-type futures --contract-type usd_m --pair BTCUSDT
```

A complete list of arguments can be obtained using the command:

```bash
metaexpert --help
```

### Backward Compatibility

All existing command-line usage patterns continue to work without changes. Both short and long forms of arguments are supported:

```bash
# Long form (recommended for scripts)
metaexpert --exchange binance --pair BTCUSDT --timeframe 1h

# Short form (acceptable for interactive use)
metaexpert -e binance -p BTCUSDT -tf 1h
```
