# API Contract: MetaLogger

## Overview
This document specifies the API contract for the MetaLogger, which is the central component of the comprehensive logging system in MetaExpert.

## MetaLogger Class

### Constructor
```python
def __init__(
    self,
    log_level: str = "INFO",
    log_file: str = "expert.log",
    trade_log_file: str = "trades.log",
    error_log_file: str = "errors.log",
    log_to_console: bool = True,
    structured_logging: bool = False,
    async_logging: bool = False,
    log_max_file_size: int = 10485760,  # 10MB
    log_backup_count: int = 5
) -> None
```

**Parameters**:
- `log_level` (str): Minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file` (str): Path for the main log file
- `trade_log_file` (str): Path for the trade-specific log file
- `error_log_file` (str): Path for the error-specific log file
- `log_to_console` (bool): Whether to output to console
- `structured_logging` (bool): Whether to use JSON format
- `async_logging` (bool): Whether to use asynchronous logging
- `log_max_file_size` (int): Max size in bytes before rotation (default: 10MB)
- `log_backup_count` (int): Number of backup files to keep

**Returns**: A configured MetaLogger instance

### Methods

#### bind(context: dict) -> MetaLogger
Creates a new logger with additional context bound to it.

**Parameters**:
- `context` (dict): Key-value pairs to add as context

**Returns**: A new MetaLogger instance with the context bound

#### debug(event: str, **kwargs) -> None
Log a debug message.

**Parameters**:
- `event` (str): The event message to log
- `**kwargs`: Additional context fields to include

#### info(event: str, **kwargs) -> None
Log an info message.

**Parameters**:
- `event` (str): The event message to log
- `**kwargs`: Additional context fields to include

#### warning(event: str, **kwargs) -> None
Log a warning message.

**Parameters**:
- `event` (str): The event message to log
- `**kwargs`: Additional context fields to include

#### error(event: str, **kwargs) -> None
Log an error message.

**Parameters**:
- `event` (str): The event message to log
- `**kwargs`: Additional context fields to include

#### critical(event: str, **kwargs) -> None
Log a critical message.

**Parameters**:
- `event` (str): The event message to log
- `**kwargs`: Additional context fields to include

## Log Format

### Text Format
```
[timestamp] [LEVEL    ] event message key1=value1 key2=value2
```

### JSON Format (RFC 5424 compliant)
```json
{
  "timestamp": "2025-10-17T10:30:00.000000Z",
  "level": "info",
  "event": "event message",
  "expert_name": "MyEmaBot",
  "symbol": "BTCUSDT",
  "key1": "value1",
  "key2": "value2"
}
```

## Configuration Priority

Configuration parameters follow this priority order (highest to lowest):
1. Code parameters passed to constructor
2. Environment variables
3. Default values

## File Outputs

- **expert.log**: Contains all messages at INFO level and above
- **trades.log**: Contains messages with category="trade" context (JSON Lines format)
- **errors.log**: Contains ERROR and CRITICAL level messages with full stack traces