# Managing Experts

This guide explains how to manage running experts using the MetaExpert CLI.

## Prerequisites

- MetaExpert CLI installed
- One or more experts running

## Listing Running Experts

To list all running experts:

```bash
metaexpert list
```

This command will display a table of all running experts:

```
┌────────────────────┬───────────┬──────────┬──────────┬──────────────┬─────────────────────┐
│ Name               │ PID       │ Status   │ CPU %    │ Memory (MB)   │ Started             │
├────────────────────┼───────────┼──────────┼──────────┼──────────────┼─────────────────────┤
│ my-trading-expert  │ 12345     │ running  │ 2.5      │ 45.6         │ 2024-10-27 10:00:00 │
│ another-expert     │ 12346     │ running  │ 1.8      │ 32.1         │ 2024-10-27 10:05:00 │
└────────────────────┴───────────┴──────────┴──────────┴──────────────┴─────────────────────┘
```

### Filtering by Directory

To list experts in a specific directory:

```bash
metaexpert list --path /path/to/projects
```

### Output Formats

To output the list in different formats:

```bash
# JSON format
metaexpert list --format json

# YAML format
metaexpert list --format yaml
```

## Checking Expert Status

To check the status of a specific expert:

```bash
metaexpert status /path/to/my-trading-expert
```

This command will display detailed information about the expert:

```
Expert Status:
  PID: 12345
  Name: my-trading-expert
  Status: running
  CPU %: 2.5
  Memory (MB): 45.6
  Started: 2024-10-27 10:00:00
  Working Directory: /path/to/my-trading-expert
  Command: python main.py
```

## Viewing Expert Logs

To view the logs of a specific expert:

```bash
# View last 50 lines of logs
metaexpert logs my-trading-expert

# Follow log output
metaexpert logs my-trading-expert --follow

# View logs with ERROR level or higher
metaexpert logs my-trading-expert --level ERROR

# View last 100 lines of logs
metaexpert logs my-trading-expert --lines 100
```

### Log Levels

MetaExpert supports the following log levels:

- `DEBUG`: Detailed information for diagnosing problems.
- `INFO`: General information about the expert's operation.
- `WARNING`: Indicates that something unexpected happened.
- `ERROR`: Indicates that a serious problem occurred.
- `CRITICAL`: Indicates that the expert cannot continue running.

## Stopping Experts

To stop a running expert:

```bash
metaexpert stop my-trading-expert
```

### Force Stopping

To force stop an expert:

```bash
metaexpert stop my-trading-expert --force
```

### Specifying Timeout

To specify a timeout for graceful shutdown:

```bash
metaexpert stop my-trading-expert --timeout 60
```

## Restarting Experts

To restart an expert, you need to stop it and then start it again:

```bash
# Stop the expert
metaexpert stop my-trading-expert

# Start the expert
metaexpert run /path/to/my-trading-expert
```

Alternatively, if the expert was started with `--restart-on-error`, it will automatically restart if it crashes.

## Advanced Management

### Setting Resource Limits

To limit the resources used by an expert:

```bash
# This feature is planned for future releases
metaexpert run --max-memory 1024 --max-cpu 50
```

### Scheduling Experts

To schedule an expert to start or stop at a specific time:

```bash
# This feature is planned for future releases
metaexpert schedule start my-trading-expert --at "09:00"
metaexpert schedule stop my-trading-expert --at "17:00"
```

### Monitoring Experts

To continuously monitor experts:

```bash
# This feature is planned for future releases
metaexpert monitor
```

This command will display a live dashboard of all running experts, showing CPU, memory, and other metrics.

## Best Practices

### 1. Regular Monitoring

Regularly check the status and logs of your experts to ensure they are running correctly.

### 2. Resource Management

Monitor the CPU and memory usage of your experts to ensure they are not consuming excessive resources.

### 3. Log Rotation

Configure log rotation to prevent log files from growing too large.

### 4. Backup Configurations

Regularly backup your expert configurations and data.

### 5. Use Descriptive Names

Use descriptive names for your experts to make them easier to identify and manage.

## Conclusion

Managing experts is an essential part of using MetaExpert CLI. By regularly monitoring, logging, and controlling your experts, you can ensure they are running smoothly and efficiently.

For more information on available management commands and options, see the [Command Reference](../COMMAND_REFERENCE.md).