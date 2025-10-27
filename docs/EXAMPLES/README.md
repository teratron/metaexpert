# MetaExpert CLI Examples

This directory contains practical examples demonstrating how to use the MetaExpert CLI for various trading scenarios.

## Table of Contents

1. [Basic Expert Creation](#basic-expert-creation)
2. [Running an Expert](#running-an-expert)
3. [Backtesting a Strategy](#backtesting-a-strategy)
4. [Using Different Exchanges](#using-different-exchanges)
5. [Advanced Configuration](#advanced-configuration)
6. [Monitoring and Managing Experts](#monitoring-and-managing-experts)
7. [Additional Examples](#additional-examples)
    - [Creating a New Expert](../examples/creating_an_expert.md)
    - [Backtesting a Strategy](../examples/backtesting_a_strategy.md)
    - [Managing Experts](../examples/managing_experts.md)
    - [Extending the CLI](../examples/extending_the_cli.md)

## Basic Expert Creation

### Creating a Simple Expert

To create a new expert project:

```bash
metaexpert new my-simple-expert --exchange binance --strategy ema
```

This creates a new expert project named `my-simple-expert` for Binance exchange using an EMA strategy.

### Project Structure

The created project will have the following structure:

```
my-simple-expert/
├── main.py          # Main expert script
├── .env             # Environment configuration
├── .env.example     # Example environment configuration
├── pyproject.toml   # Project dependencies
├── README.md        # Project documentation
└── logs/            # Log directory
```

## Running an Expert

### Running in Foreground

To run an expert in the foreground (attached to the terminal):

```bash
cd my-simple-expert
metaexpert run --no-detach
```

### Running in Background

To run an expert in the background (detached):

```bash
metaexpert run
```

### Specifying a Script

To run a specific script:

```bash
metaexpert run --script custom_strategy.py
```

## Backtesting a Strategy

### Basic Backtest

To backtest a strategy:

```bash
metaexpert backtest main.py --start-date 2024-01-01 --end-date 2024-12-31
```

### Backtest with Optimization

To backtest with parameter optimization:

```bash
metaexpert backtest main.py --optimize --optimize-params "period,threshold"
```

### Backtest Comparison

To compare different strategies:

```bash
metaexpert backtest main.py --compare
```

### Backtest Report Formats

To generate a backtest report in a specific format:

```bash
# Generate HTML report
metaexpert backtest main.py --report-format html

# Generate JSON report
metaexpert backtest main.py --report-format json

# Generate CSV report
metaexpert backtest main.py --report-format csv
```

## Using Different Exchanges

### Binance

To create an expert for Binance:

```bash
metaexpert new my-binance-expert --exchange binance --strategy rsi
```

### Bybit

To create an expert for Bybit:

```bash
metaexpert new my-bybit-expert --exchange bybit --strategy macd
```

### OKX

To create an expert for OKX:

```bash
metaexpert new my-okx-expert --exchange okx --strategy ema
```

## Advanced Configuration

### Using Environment Files

To use a specific environment file:

```bash
metaexpert run --env-file .env.production
```

### Configuration Profiles

To use a specific configuration profile:

```bash
export METAEXPERT_PROFILE=production
metaexpert run
```

### Custom Configuration

To set a custom configuration value:

```bash
metaexpert config default_exchange --set binance
```

## Monitoring and Managing Experts

### Listing Running Experts

To list all running experts:

```bash
metaexpert list
```

### Viewing Expert Status

To view the status of a specific expert:

```bash
metaexpert status /path/to/my-expert
```

### Viewing Expert Logs

To view the logs of a specific expert:

```bash
# View last 50 lines of logs
metaexpert logs my-expert

# Follow log output
metaexpert logs my-expert --follow

# View logs with ERROR level or higher
metaexpert logs my-expert --level ERROR
```

### Stopping an Expert

To stop a running expert:

```bash
metaexpert stop my-expert
```

### Force Stopping an Expert

To force stop an expert:

```bash
metaexpert stop my-expert --force
```

## Additional Examples

### Initializing the CLI Environment

```bash
metaexpert init --interactive
```

### Diagnosing the CLI Environment

```bash
metaexpert doctor
```

### Cleaning Project Files

To clean log and cache files:

```bash
metaexpert clean /path/to/my-expert
```

To clean all files including outputs:

```bash
metaexpert clean /path/to/my-expert --all
```

### Exporting Project Data

To export project data in JSON format:

```bash
metaexpert export /path/to/my-expert
```

To export project data in CSV format:

```bash
metaexpert export /path/to/my-expert --format csv
```

### Importing Project Data

To import project data:

```bash
metaexpert import data.json
```

To import project data to a specific directory:

```bash
metaexpert import data.json --project-path /path/to/my-expert
```

To import project data with overwrite:

```bash
metaexpert import data.json --overwrite
```

### Showing CLI Version

To show full version information:

```bash
metaexpert version
```

To show only version number:

```bash
metaexpert version --short