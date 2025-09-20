# Quickstart: MetaExpert Logging System Enhancement

## Purpose
This document provides a quickstart guide for developers who want to use the enhanced logging system in the MetaExpert library. The logging system is located at `/src/metaexpert/logger`.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- Basic understanding of logging concepts

## Key Features of the Enhanced Logging System

### Structured Logging
Logs are now formatted as structured JSON data, making them easier to parse and analyze.

### Asynchronous Logging
Logging operations are performed asynchronously to minimize performance impact.

### Centralized Configuration
All logging configuration is centralized for easier management and consistency.

### Multiple Output Destinations
Logs can be output to console, files, or network destinations.

## Configuration

### Default Configuration
The logging system is automatically configured with sensible defaults when the MetaExpert library is initialized.

### Custom Configuration
To customize the logging configuration, modify the logging settings in your template.py file:

```python
expert = MetaExpert(
    # ... other configuration options
    log_level="INFO",               # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    log_file="expert.log",          # Main log file
    trade_log_file="trades.log",    # Trade execution log
    error_log_file="errors.log",    # Error-specific log
    log_to_console=True,            # Print logs to console
    # ... other configuration options
)
```

### Existing Logger Module
The existing logger module is located at `/src/metaexpert/logger` and provides the following functions:
- `setup_logger()`: Configures and returns a logger instance
- `get_logger()`: Returns a logger instance by name

You can use the existing logger directly:
```python
from src.metaexpert.logger import setup_logger, get_logger

# Set up a logger
logger = setup_logger("my_module")

# Or get an existing logger
logger = get_logger("my_module")

# Use the logger
logger.info("This is a log message")
```

### Log Levels
The logging system supports the following log levels:
- **DEBUG**: Detailed information, typically of interest only when diagnosing problems
- **INFO**: Confirmation that things are working as expected
- **WARNING**: An indication that something unexpected happened
- **ERROR**: Due to a more serious problem, the software has not been able to perform some function
- **CRITICAL**: A serious error, indicating that the program itself may be unable to continue running

## Usage Examples

### Basic Logging
```python
import logging

# Get a logger for your module
logger = logging.getLogger(__name__)

# Log messages at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
```

### Structured Logging
```python
import logging

logger = logging.getLogger(__name__)

# Log structured data
logger.info("Trade executed", extra={
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 50000.0
})
```

### Performance Considerations
For performance-critical code paths, consider using lazy evaluation for expensive log messages:

```python
import logging

logger = logging.getLogger(__name__)

# Instead of this (always evaluates the message):
logger.debug("Expensive operation result: %s", expensive_operation())

# Use this (only evaluates when logging level allows):
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Expensive operation result: %s", expensive_operation())
```

## Troubleshooting

### Log Files Not Being Created
- Check that the log file path is writable
- Verify that there's sufficient disk space
- Ensure the log directory exists

### Missing Log Messages
- Check that the log level is set appropriately
- Verify that the logger is properly configured
- Ensure that log propagation is enabled if needed

### Performance Issues
- Consider using asynchronous logging for high-frequency operations
- Review log levels to avoid excessive logging
- Check file I/O performance if using file-based logging

## Best Practices

### Use Appropriate Log Levels
- Use DEBUG for detailed diagnostic information
- Use INFO for general operational messages
- Use WARNING for unexpected but recoverable events
- Use ERROR for serious problems that affect functionality
- Use CRITICAL for severe errors that may terminate the application

### Include Context Information
When logging, include relevant context information to help with debugging:

```python
logger.error("Failed to execute trade", extra={
    "symbol": symbol,
    "side": side,
    "quantity": quantity,
    "error": str(e)
})
```

### Avoid Logging Sensitive Information
Never log sensitive information such as API keys, passwords, or private data.

### Use Structured Logging for Complex Data
For complex data structures, use structured logging to make the data searchable and analyzable.