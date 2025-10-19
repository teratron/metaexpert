# Public API Contract: Logging Module

**Date**: 2025-10-17

This document defines the public API contract for the `metaexpert.logger` module. This is the set of functions, classes, and parameters that the library guarantees for external users and their strategies.

## 1. `MetaLogger` Factory

This is the primary entry point for initializing the logging system.

```python
from metaexpert.logger import MetaLogger

logger = MetaLogger(
    log_level="INFO",
    log_file="expert.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    log_to_console=True,
    structured_logging=False,
    async_logging=True,
    webhook_url=None,
    # ... other config ...
)
```

### Parameters

- `log_level` (str): Minimum log level. Default: `"INFO"`.
- `log_file` (str): Path for the main log file. Default: `"expert.log"`.
- `trade_log_file` (str): Path for the trade-specific log. Default: `"trades.log"`.
- `error_log_file` (str): Path for the error-specific log. Default: `"errors.log"`.
- `log_to_console` (bool): Toggles console output. Default: `True`.
- `structured_logging` (bool): Toggles JSON format for files/webhooks. Default: `False`.
- `async_logging` (bool): Toggles non-blocking file I/O. Default: `False`.
- `webhook_url` (str | None): URL for `CRITICAL` alert notifications. Default: `None`.

**Returns**: A fully configured `structlog` logger instance.

## 2. Logger Instance API

The logger instance returned by `MetaLogger` (and available via `expert.logger`) conforms to the standard `structlog` API.

### Logging Methods

These methods create a log entry.

```python
# Basic logging
expert.logger.info("Expert has started")
expert.logger.warning("Slippage is high", slippage=0.5)

# Logging with exception info
try:
    1 / 0
except ZeroDivisionError:
    expert.logger.error("Calculation failed")
```

- `debug(event: str, **context)`
- `info(event: str, **context)`
- `warning(event: str, **context)`
- `error(event: str, **context)`
- `critical(event: str, **context)`

### Context Management

This method allows for creating a new logger instance with additional, permanent context.

```python
# Create a logger specifically for a trading pair
symbol_logger = expert.logger.bind(symbol="BTCUSDT", strategy="EMA_Cross")

# All logs from symbol_logger will now include {"symbol": "BTCUSDT", "strategy": "EMA_Cross"}
symbol_logger.info("Signal detected")
```

- `bind(**new_context) -> Logger`: Returns a new logger with `new_context` merged into its existing bound context.
- `unbind(*keys_to_remove) -> Logger`: Returns a new logger with specified keys removed from its bound context.

## 3. Integration with `MetaExpert` Class

The logging system is automatically initialized within the `MetaExpert` class. Users can override the default logging configuration by passing parameters to the constructor.

```python
from metaexpert import MetaExpert

expert = MetaExpert(
    exchange="binance",
    # ... other core params

    # Override logging config
    log_level="DEBUG",
    structured_logging=True,
    webhook_url="https://my-alerts.com/xyz"
)

# Use the pre-configured logger
expert.logger.info("This will be a structured log entry.")
```

This contract ensures that users have a consistent and powerful interface for logging, while the implementation details (processors, handlers) remain encapsulated within the `metaexpert.logger` module.
