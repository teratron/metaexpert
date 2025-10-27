# MetaExpert CLI Command Reference

This document provides detailed information about all commands available in the MetaExpert CLI.

## Table of Contents

1. [new](#new)
2. [run](#run)
3. [stop](#stop)
4. [status](#status)
5. [list](#list)
6. [logs](#logs)
7. [backtest](#backtest)
8. [config](#config)
9. [doctor](#doctor)
10. [version](#version)
11. [clean](#clean)
12. [export](#export)
13. [import](#import)
14. [init](#init)

## new

Create a new expert project.

### Usage

```bash
metaexpert new PROJECT_NAME [OPTIONS]
```

### Arguments

- `PROJECT_NAME`: Name of the new expert project.

### Options

- `-e, --exchange TEXT`: Target exchange (default: binance).
- `-s, --strategy TEXT`: Strategy type (ema, rsi, macd, template) (default: template).
- `--market-type TEXT`: Market type (spot, futures, options) (default: futures).
- `-o, --output-dir PATH`: Output directory.
- `-f, --force`: Overwrite existing directory.
- `--help`: Show this message and exit.

### Examples

```bash
# Create a new expert project with default settings
metaexpert new my-bot

# Create a new expert project for Binance with EMA strategy
metaexpert new my-bot --exchange binance --strategy ema

# Create a new expert project in a specific directory
metaexpert new my-bot --output-dir /path/to/projects
```

## run

Run a trading expert.

### Usage

```bash
metaexpert run [PROJECT_PATH] [OPTIONS]
```

### Arguments

- `PROJECT_PATH`: Path to expert project (default: current directory).

### Options

- `-d, --detach`: Run in background (default: True).
- `--script TEXT`: Script to run (default: main.py).
- `-e, --env-file PATH`: Environment file to use.
- `--docker`: Run in Docker container.
- `-n, --notify`: Send notifications on events.
- `--restart-on-error`: Restart on error.
- `--max-restarts INTEGER`: Maximum restart attempts (default: 5).
- `--help`: Show this message and exit.

### Examples

```bash
# Run an expert in the current directory
metaexpert run

# Run an expert in a specific directory
metaexpert run /path/to/my-bot

# Run an expert in the foreground
metaexpert run --no-detach

# Run an expert with a specific environment file
metaexpert run --env-file .env.production

# Run an expert with restart on error
metaexpert run --restart-on-error
```

## stop

Stop a running expert.

### Usage

```bash
metaexpert stop PROJECT_NAME_OR_PATH [OPTIONS]
```

### Arguments

- `PROJECT_NAME_OR_PATH`: Name or path of the expert to stop.

### Options

- `--timeout INTEGER`: Timeout for graceful shutdown (default: 30).
- `--force`: Force kill the process.
- `--help`: Show this message and exit.

### Examples

```bash
# Stop an expert by name
metaexpert stop my-bot

# Stop an expert by path
metaexpert stop /path/to/my-bot

# Force stop an expert
metaexpert stop my-bot --force
```

## status

Show expert status.

### Usage

```bash
metaexpert status PROJECT_PATH [OPTIONS]
```

### Arguments

- `PROJECT_PATH`: Path to the project directory.

### Options

- `--help`: Show this message and exit.

### Examples

```bash
# Show status of an expert
metaexpert status /path/to/my-bot
```

## list

List all running experts.

### Usage

```bash
metaexpert list [OPTIONS]
```

### Options

- `-p, --path PATH`: Limit search to specific directory.
- `-f, --format [table|json|yaml]`: Output format (default: table).
- `--help`: Show this message and exit.

### Examples

```bash
# List all running experts
metaexpert list

# List experts in a specific directory
metaexpert list --path /path/to/projects

# List experts in JSON format
metaexpert list --format json
```

## logs

View expert logs.

### Usage

```bash
metaexpert logs PROJECT_NAME_OR_PATH [OPTIONS]
```

### Arguments

- `PROJECT_NAME_OR_PATH`: Name or path of the expert.

### Options

- `--lines INTEGER`: Number of lines to show (default: 50).
- `--follow, -f`: Follow log output.
- `--level [DEBUG|INFO|WARNING|ERROR|CRITICAL]`: Filter by log level.
- `--help`: Show this message and exit.

### Examples

```bash
# View last 50 lines of logs
metaexpert logs my-bot

# Follow log output
metaexpert logs my-bot --follow

# View logs with ERROR level or higher
metaexpert logs my-bot --level ERROR
```

## backtest

Backtest a trading strategy.

### Usage

```bash
metaexpert backtest EXPERT_PATH [OPTIONS]
```

### Arguments

- `EXPERT_PATH`: Path to expert file.

### Options

- `-s, --start-date TEXT`: Start date (YYYY-MM-DD).
- `-e, --end-date TEXT`: End date (YYYY-MM-DD).
- `-c, --capital FLOAT`: Initial capital (default: 10000.0).
- `-o, --optimize`: Optimize parameters.
- `--optimize-params TEXT`: Parameters to optimize (comma-separated).
- `--compare`: Compare strategies.
- `-f, --report-format [html|json|csv]`: Report format (default: html).
- `--help`: Show this message and exit.

### Examples

```bash
# Backtest a strategy
metaexpert backtest main.py --start-date 2024-01-01

# Backtest with optimization
metaexpert backtest main.py --optimize --optimize-params "period,threshold"

# Backtest and compare strategies
metaexpert backtest main.py --compare

# Backtest with JSON report
metaexpert backtest main.py --report-format json
```

## config

Manage CLI configuration.

### Usage

```bash
metaexpert config [KEY] [OPTIONS]
```

### Arguments

- `KEY`: Configuration key to get/set.

### Options

- `-s, --set TEXT`: Value to set for the key.
- `-p, --profile TEXT`: Profile to use.
- `--help`: Show this message and exit.

### Examples

```bash
# Display all configuration
metaexpert config

# Display specific configuration key
metaexpert config default_exchange

# Set configuration key
metaexpert config default_exchange --set binance
```

## doctor

Diagnose CLI environment.

### Usage

```bash
metaexpert doctor [OPTIONS]
```

### Options

- `--help`: Show this message and exit.

### Examples

```bash
# Diagnose CLI environment
metaexpert doctor
```

## version

Show CLI version.

### Usage

```bash
metaexpert version [OPTIONS]
```

### Options

- `-s, --short`: Show only version number.
- `--help`: Show this message and exit.

### Examples

```bash
# Show full version information
metaexpert version

# Show only version number
metaexpert version --short
```

## clean

Clean project files.

### Usage

```bash
metaexpert clean PROJECT_PATH [OPTIONS]
```

### Arguments

- `PROJECT_PATH`: Path to the project directory.

### Options

- `-l, --logs`: Clean log files (default: True).
- `-c, --cache`: Clean cache files (default: True).
- `-a, --all`: Clean all files including outputs.
- `--help`: Show this message and exit.

### Examples

```bash
# Clean log and cache files
metaexpert clean /path/to/my-bot

# Clean all files
metaexpert clean /path/to/my-bot --all
```

## export

Export project data.

### Usage

```bash
metaexpert export PROJECT_PATH [OPTIONS]
```

### Arguments

- `PROJECT_PATH`: Path to the project directory.

### Options

- `-o, --output PATH`: Output file path (default: project_name_export.<format>).
- `-f, --format [json|csv|yaml]`: Export format (default: json).
- `-l, --include-logs`: Include log files.
- `-c, --include-config`: Include config files (default: True).
- `--help`: Show this message and exit.

### Examples

```bash
# Export project data in JSON format
metaexpert export /path/to/my-bot

# Export project data in CSV format
metaexpert export /path/to/my-bot --format csv

# Export project data with logs
metaexpert export /path/to/my-bot --include-logs
```

## import

Import project data.

### Usage

```bash
metaexpert import INPUT_FILE [OPTIONS]
```

### Arguments

- `INPUT_FILE`: Path to the input file.

### Options

- `-p, --project-path PATH`: Path to the project directory (default: current directory).
- `-f, --format [auto|json|csv|yaml]`: Import format (default: auto).
- `-o, --overwrite`: Overwrite existing files.
- `--help`: Show this message and exit.

### Examples

```bash
# Import project data
metaexpert import data.json

# Import project data to a specific directory
metaexpert import data.json --project-path /path/to/my-bot

# Import project data with overwrite
metaexpert import data.json --overwrite
```

## init

Initialize MetaExpert CLI environment.

### Usage

```bash
metaexpert init [OPTIONS]
```

### Options

- `-i, --interactive`: Interactive setup.
- `--help`: Show this message and exit.

### Examples

```bash
# Initialize CLI environment
metaexpert init

# Initialize CLI environment interactively
metaexpert init --interactive