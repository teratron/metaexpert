# MetaExpert CLI Guide

Welcome to the MetaExpert CLI guide! This document will help you get started with using the MetaExpert command-line interface.

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Commands](#commands)
4. [Configuration](#configuration)
5. [Advanced Usage](#advanced-usage)

## Installation

To install MetaExpert CLI, you can use pip:

```bash
pip install metaexpert[cli]
```

Or if you're using uv:

```bash
uv pip install metaexpert[cli]
```

## Quick Start

1. Initialize the CLI environment:

```bash
metaexpert init
```

2. Create a new expert project:

```bash
metaexpert new my-first-expert --exchange binance --strategy ema
```

3. Navigate to your project directory:

```bash
cd my-first-expert
```

4. Run your expert:

```bash
metaexpert run
```

5. Check the status of your expert:

```bash
metaexpert status
```

6. Stop your expert:

```bash
metaexpert stop
```

## Commands

MetaExpert CLI provides a variety of commands to manage your trading experts. Here are some of the most commonly used commands:

- `new`: Create a new expert project.
- `run`: Run an expert.
- `stop`: Stop a running expert.
- `status`: Show the status of a running expert.
- `list`: List all running experts.
- `logs`: View logs of a running expert.
- `backtest`: Backtest a strategy.
- `config`: Manage CLI configuration.
- `doctor`: Diagnose CLI environment.
- `version`: Show CLI version.
- `clean`: Clean project files.
- `export`: Export project data.
- `import`: Import project data.

For detailed information about each command, see the [Command Reference](COMMAND_REFERENCE.md).

## Configuration

MetaExpert CLI can be configured using a configuration file or environment variables. The default configuration file is located at `~/.metaexpert/config`.

You can also use the `config` command to manage your configuration:

```bash
metaexpert config --set default_exchange binance
```

## Advanced Usage

### Profiles

MetaExpert CLI supports profiles, allowing you to have different configurations for different environments (e.g., development, production).

To use a specific profile, set the `METAEXPERT_PROFILE` environment variable:

```bash
export METAEXPERT_PROFILE=production
metaexpert run
```

### Environment Files

You can specify an environment file to use with the `--env-file` option:

```bash
metaexpert run --env-file .env.production
```

### Docker

MetaExpert CLI supports running experts in Docker containers (this feature is planned for future releases).

### Notifications

You can enable notifications for certain events using the `--notify` option (this feature is planned for future releases).

### Restart on Error

To automatically restart an expert if it crashes, use the `--restart-on-error` option:

```bash
metaexpert run --restart-on-error
```

### Maximum Restarts

You can specify the maximum number of restart attempts using the `--max-restarts` option:

```bash
metaexpert run --restart-on-error --max-restarts 3
