# Troubleshooting MetaExpert CLI

This document provides solutions to common issues you might encounter while using the MetaExpert CLI.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Command Execution Issues](#command-execution-issues)
3. [Configuration Issues](#configuration-issues)
4. [Expert Runtime Issues](#expert-runtime-issues)
5. [Backtesting Issues](#backtesting-issues)
6. [Performance Issues](#performance-issues)
7. [Network Issues](#network-issues)
8. [Docker Issues](#docker-issues)

## Installation Issues

### Problem: `pip install metaexpert[cli]` fails

**Solution:**

1. Ensure you have Python 3.12 or later installed:

```bash
python --version
```

2. Upgrade pip:

```bash
pip install --upgrade pip
```

3. Try installing with `--user` flag:

```bash
pip install --user metaexpert[cli]
```

4. If you're behind a proxy, configure pip:

```bash
pip install --proxy http://user:password@proxyserver:port metaexpert[cli]
```

### Problem: Command not found after installation

**Solution:**

1. Check if the installation path is in your `PATH`:

```bash
pip show -f metaexpert
```

2. Add the installation path to your `PATH` environment variable.

3. On Windows, you might need to add the Scripts directory to your `PATH`:

```bash
# Add to PATH (temporary)
set PATH=%PATH%;C:\Users\YourUsername\AppData\Local\Programs\Python\Python312\Scripts

# Or permanently via System Properties -> Environment Variables
```

### Problem: Permission denied during installation

**Solution:**

1. Use `--user` flag to install for the current user only:

```bash
pip install --user metaexpert[cli]
```

2. On Linux/macOS, use `sudo` (not recommended):

```bash
sudo pip install metaexpert[cli]
```

3. Use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install metaexpert[cli]
```

## Command Execution Issues

### Problem: Command fails with "ModuleNotFoundError"

**Solution:**

1. Ensure you're using the correct Python environment where MetaExpert is installed.

2. Check if all dependencies are installed:

```bash
metaexpert doctor
```

3. Reinstall MetaExpert:

```bash
pip uninstall metaexpert
pip install metaexpert[cli]
```

### Problem: Command hangs or takes too long

**Solution:**

1. Use `Ctrl+C` to interrupt the command and check for any error messages.

2. Increase verbosity to see what's happening:

```bash
metaexpert --verbose <command>
```

3. Check system resources (CPU, memory) to ensure there's no bottleneck.

### Problem: Command produces unexpected output

**Solution:**

1. Check the command's help for correct usage:

```bash
metaexpert <command> --help
```

2. Ensure you're using the latest version of MetaExpert:

```bash
metaexpert version
pip install --upgrade metaexpert[cli]
```

## Configuration Issues

### Problem: Configuration values are not respected

**Solution:**

1. Check the configuration file location:

```bash
metaexpert config --profile <profile-name>
```

2. Ensure the configuration file is correctly formatted.

3. Use environment variables to override configuration:

```bash
export METAEXPERT_CLI_DEFAULT_EXCHANGE=binance
metaexpert run
```

### Problem: Profile configuration is not loaded

**Solution:**

1. Ensure the profile name is correct:

```bash
metaexpert config --profile <profile-name>
```

2. Check if the profile file exists in `~/.metaexpert/<profile-name>.env`.

3. Set the profile using environment variable:

```bash
export METAEXPERT_PROFILE=<profile-name>
metaexpert run
```

## Expert Runtime Issues

### Problem: Expert fails to start

**Solution:**

1. Check the expert's log files:

```bash
metaexpert logs <expert-name>
```

2. Ensure all required dependencies for the expert are installed.

3. Validate the expert's configuration file (`.env`).

4. Check if the expert's script file exists and is executable.

### Problem: Expert crashes unexpectedly

**Solution:**

1. Enable restart on error:

```bash
metaexpert run --restart-on-error
```

2. Check the expert's log files for crash details:

```bash
metaexpert logs <expert-name>
```

3. Increase log level for more detailed information:

```bash
metaexpert logs <expert-name> --level DEBUG
```

### Problem: Expert is not responding to market changes

**Solution:**

1. Check if the expert is connected to the exchange API.

2. Verify the expert's configuration (API keys, symbols, timeframes).

3. Check the expert's strategy logic for potential deadlocks or infinite loops.

4. Monitor system resources to ensure the expert is not starved of CPU or memory.

## Backtesting Issues

### Problem: Backtest fails with data loading error

**Solution:**

1. Ensure the expert file exists and is accessible.

2. Check if the specified date range is valid and has available data.

3. Verify the expert's data loading logic.

### Problem: Backtest results are unexpected

**Solution:**

1. Check the expert's strategy logic for potential bugs.

2. Verify the initial capital and other backtest parameters.

3. Compare results with a known-good backtest.

### Problem: Backtest optimization fails

**Solution:**

1. Ensure the parameters specified for optimization exist in the expert.

2. Check if the parameter values are within valid ranges.

3. Increase the verbosity of the optimization process to see detailed logs.

## Performance Issues

### Problem: CLI commands are slow

**Solution:**

1. Check system resources (CPU, memory, disk I/O).

2. Disable unnecessary features like logging to file:

```bash
metaexpert --quiet <command>
```

3. Use profiling to identify bottlenecks:

```bash
metaexpert --profile <command>
```

### Problem: High memory usage

**Solution:**

1. Check for memory leaks in expert strategies.

2. Reduce the amount of historical data loaded into memory.

3. Use data streaming instead of batch loading where possible.

### Problem: High CPU usage

**Solution:**

1. Check for inefficient loops or calculations in expert strategies.

2. Reduce the frequency of strategy updates.

3. Use asynchronous processing where possible.

## Network Issues

### Problem: Connection timeouts

**Solution:**

1. Check your internet connection.

2. Increase the API timeout:

```bash
metaexpert config --set api_timeout 30
```

3. Use a proxy if required:

```bash
export HTTP_PROXY=http://proxy-server:port
export HTTPS_PROXY=http://proxy-server:port
```

### Problem: SSL certificate errors

**Solution:**

1. Update your system's CA certificates.

2. Disable SSL verification (not recommended for production):

```bash
export PYTHONHTTPSVERIFY=0
```

3. Use a custom CA bundle:

```bash
export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt
```

## Docker Issues

### Problem: Docker container fails to start

**Solution:**

1. Ensure Docker is installed and running.

2. Check Docker daemon logs for errors.

3. Verify the Docker image is correctly built.

### Problem: Expert inside Docker cannot access host network

**Solution:**

1. Use `--network host` flag when running the container:

```bash
docker run --network host <image-name>
```

2. Map the necessary ports explicitly:

```bash
docker run -p 8080:8080 <image-name>
```

### Problem: Volume mounting issues

**Solution:**

1. Ensure the host directory exists and has correct permissions.

2. Use absolute paths for volume mounts.

3. Check if SELinux or AppArmor is blocking access.