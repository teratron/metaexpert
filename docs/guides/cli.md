# CLI Usage Guide

This guide provides detailed information on how to use the `metaexpert` command-line interface (CLI) to manage your trading experts.

## Commands

### `metaexpert new <PROJECT_NAME>`

Creates a new trading expert project from a template.

**Arguments:**

*   `<PROJECT_NAME>`: The name of the new expert project. This will be the name of the directory created for your project.

**Options:**

*   `--exchange`, `-e`: The target exchange for the expert (e.g., `binance`, `bybit`, `okx`). Defaults to `binance`.
*   `--force`, `-f`: Overwrite the existing directory if it already exists. Use with caution.

**Examples:**

```bash
# Create a new expert named 'my-first-bot' for Binance
metaexpert new my-first-bot

# Create a new expert for Bybit, overwriting if it exists
metaexpert new my-bybit-expert --exchange bybit --force
```

### `metaexpert run <PATH>`

Runs a trading expert in a detached background process. A PID file (`.metaexpert.pid`) will be created in the project directory to track the running process.

**Arguments:**

*   `<PATH>`: The path to the expert project directory (e.g., `./my-first-bot`).

**Examples:**

```bash
# Run the expert located in the 'my-first-bot' directory
metaexpert run ./my-first-bot
```

### `metaexpert backtest <PATH>`

Backtests a trading expert. This command will execute the expert's logic against historical data (implementation details for backtesting engine to follow).

**Arguments:**

*   `<PATH>`: The path to the expert project directory.

**Examples:**

```bash
# Backtest the expert in 'my-first-bot'
metaexpert backtest ./my-first-bot
```

### `metaexpert list`

Lists all detected trading experts in the current working directory and their running status.

**Output:**

The command will display a table with the following columns:

*   `Project Name`: The name of the expert project.
*   `Path`: The absolute path to the expert project directory.
*   `PID`: The Process ID of the running expert, or `N/A` if not running.
*   `Status`: The current status of the expert (e.g., `Running`, `Stopped`, `Stale PID`, `Malformed PID File`).

**Examples:**

```bash
# List all experts
metaexpert list
```

### `metaexpert stop <PATH>`

Stops a running trading expert by sending a termination signal to its process. The PID is read from the `.metaexpert.pid` file in the project directory.

**Arguments:**

*   `<PATH>`: The path to the expert project directory.

**Examples:**

```bash
# Stop the expert running in 'my-first-bot'
metaexpert stop ./my-first-bot
```

### `metaexpert logs <PATH>`

Views the log file for a trading expert. This command will tail the `expert.log` file located in the project directory.

**Arguments:**

*   `<PATH>`: The path to the expert project directory.

**Options:**

*   `--level`, `-l`: Filter logs by level (e.g., `INFO`, `WARNING`, `ERROR`, `DEBUG`). If not specified, all log levels are shown.

**Examples:**

```bash
# View all logs for 'my-first-bot'
metaexpert logs ./my-first-bot

# View only ERROR level logs for 'my-first-bot'
metaexpert logs ./my-first-bot --level ERROR
```
