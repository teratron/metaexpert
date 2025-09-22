# Quickstart: MetaExpert CLI System Enhancement

## Purpose
This document provides a quickstart guide for developers who want to use the enhanced command-line interface in the MetaExpert library.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- Basic understanding of command-line interfaces

## Key Features of the Enhanced CLI System

### Logical Argument Grouping
Arguments are now organized into logical groups for easier navigation and understanding.

### Improved Help Documentation
Enhanced help text provides clearer guidance on argument usage.

### Backward Compatibility
All existing command-line usage patterns continue to work without changes.

### Alignment with template.py
CLI arguments map directly to template.py configuration parameters for consistency.

## Common CLI Commands

### Creating a New Trading Strategy
```bash
metaexpert --new my_trading_strategy
```

This command creates a new directory with a template.py file copied into it.

### Running a Trading Strategy
```bash
python template.py --exchange binance --pair BTCUSDT --timeframe 1h
```

### Running in Different Modes
```bash
# Paper trading mode
python template.py --trade-mode paper

# Backtesting mode
python template.py --trade-mode backtest --start-date 2024-01-01 --end-date 2024-12-31

# Live trading mode
python template.py --trade-mode live --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET
```

### Configuring Risk Management
```bash
python template.py --stop-loss 2.0 --take-profit 4.0 --size 0.1
```

## Argument Groups

### Core Configuration
- `--log-level`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--exchange`: Select the exchange to trade on

### Trading Parameters
- `--trade-mode`: Set trading mode (backtest, paper, live)
- `--market-type`: Set market type (spot, futures, options, margin)
- `--contract-type`: Set contract type for futures (usd_m, coin_m)
- `--pair`: Set the trading pair (e.g., BTCUSDT)
- `--timeframe`: Set the trading timeframe

### Risk Management
- `--size`: Set maximum position size
- `--stop-loss`: Set stop loss percentage
- `--take-profit`: Set take profit percentage
- `--trailing-stop`: Set trailing stop percentage

### Backtesting
- `--start-date`: Set backtest start date
- `--end-date`: Set backtest end date
- `--balance`: Set initial balance for backtesting
- `--output`: Set output file for backtest results

### Authentication
- `--api-key`: Set API key for exchange authentication
- `--api-secret`: Set API secret for exchange authentication
- `--base-url`: Set base URL for exchange API

### Template Management
- `--new`: Create a new expert file from template

## Help Commands

### General Help
```bash
metaexpert --help
```

### Group-Specific Help
```bash
metaexpert --help core
metaexpert --help trading
metaexpert --help risk
metaexpert --help backtest
metaexpert --help auth
metaexpert --help template
```

## Best Practices

### Use Descriptive Argument Names
While short forms are available, using descriptive long-form argument names makes scripts more readable:

```bash
# Preferred for scripts
python template.py --exchange binance --pair BTCUSDT --timeframe 1h

# Short form (acceptable for interactive use)
python template.py -e binance -p BTCUSDT -tf 1h
```

### Validate Arguments Before Running
Use the help commands to verify argument values before running strategies:

```bash
python template.py --help trading
```

### Handle Sensitive Information Carefully
Never include API keys or secrets directly in command lines that might be logged or visible in process lists. Use environment variables or configuration files instead.

## Troubleshooting

### Invalid Argument Values
If you receive an error about invalid argument values, check:
- That the value is of the correct type
- That the value is within allowed choices
- That required arguments are provided

### Missing Required Arguments
If you receive an error about missing required arguments, check:
- That all required arguments for your chosen mode are provided
- That argument names are spelled correctly

### Performance Issues
If you experience slow startup times:
- Check that your system has sufficient resources
- Verify that network connectivity to exchange APIs is working properly
- Consider reducing the number of arguments that require API calls during startup

## Migration from Previous Versions

### No Breaking Changes
All existing command-line usage patterns continue to work without changes.

### Enhanced Help Text
Enhanced help text provides more detailed information about each argument.

### Improved Error Messages
More descriptive error messages help identify and resolve issues faster.