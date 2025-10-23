# Logger Guide

This guide covers the usage of the new MetaExpert structured logging system (logger), built on structlog, offering structured logging, context management, and specialized handlers.

## Overview

The logger module provides a production-ready logging system with the following features:

- **Structured Logging with `structlog`**: Leverages `structlog` to provide human-readable or JSON-formatted logs, making it easier to parse and analyze log data.
- **Context Management**: Provides powerful context management capabilities with context managers and binding functionality.
- **Configurable Logger**: The `LoggerConfig` class allows for extensive customization of logging behavior, including log levels, file paths, console output, and structured logging preferences.
- **Specialized Loggers**: Provides dedicated loggers for different purposes, allowing for granular control and easier filtering of log messages.
- **Centralized Configuration**: The initialization of the logging system streamlines the setup of `structlog` processors and logging handlers by centralizing their creation and setup logic.

## Quick Start

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Initialize logging system
config = LoggerConfig(log_level="INFO")
setup_logging(config)

# Get logger
logger = get_logger(__name__)
logger.info("application started")

# With context
logger = logger.bind(symbol="BTCUSDT", exchange="binance")
logger.info("processing trade", price=50000)
```

## Configuration

The logging behavior is dictated by the `LoggerConfig` object, which can be customized to your needs.

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Create custom configuration
custom_config = LoggerConfig(
    log_level="DEBUG",
    log_to_console=True,
    log_to_file=True,
    log_dir="logs",
    log_file="custom.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    max_bytes=20 * 1024 * 1024,  # 20MB
    backup_count=10,
    use_colors=True,
    json_logs=False
)

# Initialize logging with custom configuration
setup_logging(custom_config)

# Get logger
logger = get_logger(__name__)
logger.debug("Debug message from custom config.")
```

## Context Management

```python
from metaexpert.logger import LogContext, get_logger

logger = get_logger(__name__)
with LogContext(strategy_id=101, symbol="ETHUSDT"):
    logger.info("executing strategy")
    # All logs in this block will include strategy_id and symbol
```

## Trade Logging

```python
from metaexpert.logger import get_trade_logger, trade_context

trade_logger = get_trade_logger(strategy_id=1001)
with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
    trade_logger.info("trade executed", price=50000)
```

## Advanced Usage

### Context Variables

The logger module provides several context variables that can be used to maintain state across async operations:

- `request_id_var`: For tracking request IDs
- `trade_session_var`: For tracking trade sessions
- `strategy_id_var`: For tracking strategy IDs

### Iteration with Context

```python
from metaexpert.logger import iterate_with_context

symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

for symbol in iterate_with_context(symbols, strategy_id=1001):
    logger.info("processing", symbol=symbol)
    # Each iteration has the strategy_id context
```

### Specialized Processors

The logger module includes several custom processors:

- `add_app_context`: Adds application-specific context to log entries
- `filter_by_log_level`: Filters events based on logger's effective level
- `add_process_info`: Adds process and thread information
- `rename_event_key`: Renames 'event' to 'message' for better readability
- `TradeEventFilter`: Filters to route trade events to specialized logger
- `ErrorEventEnricher`: Enriches error events with additional context

## Formatters

The logger module provides custom formatters:

- `MetaExpertConsoleRenderer`: Enhanced console renderer with custom styling
- `CompactJSONRenderer`: Compact JSON renderer for production logs

## Migration from Old Logger

If you're migrating from the old logger system, note these key differences:

- Import from `metaexpert.logger` instead of `metaexpert.logger`
- Use `setup_logging()` and `get_logger()` instead of `MetaLogger.create()`
- Context management is handled differently with `LogContext` and `bind_contextvars`
