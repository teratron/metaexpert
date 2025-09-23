# Logger Module

## Description

The logger module provides enhanced logging functionality for the trading bot, including structured logging, asynchronous logging, and centralized configuration.

## Module Structure

### [`__init__.py`](__init__.py)

The main interface of the logger module. Provides `setup_logger` and `get_logger` functions for setting up and getting logger instances.

#### Functions (`__init__.py`)

- `setup_logger(name, level, structured, async_enabled, buffered)` - Sets up and configures a logger with enhanced features
- `get_logger(name)` - Gets a logger instance from the centralized registry

### [`async_log_handler.py`](async_log_handler.py)

Asynchronous log handlers that don't block the main thread.

#### Classes

- `AsyncLogHandler` - Asynchronous log handler
- `BufferedAsyncLogHandler` - Buffered asynchronous log handler

### [`config.json`](config.json)

Logger configuration file in JSON format. Defines formatters, handlers, and loggers.

### [`config.py`](config.py)

Python logger configuration file. Provides programmatic access to configuration and integration with environment variables.

#### Functions (`config.py`)

- `get_logging_config()` - Gets the current logger configuration
- `update_logging_config(new_config)` - Updates the logger configuration
- `get_handler_config(handler_name)` - Gets the configuration of a specific handler
- `update_handler_config(handler_name, config)` - Updates the configuration of a specific handler

### [`logger_factory.py`](logger_factory.py)

Logger factory for creating and managing logger instances.

#### Classes (`logger_factory.py`)

- `LoggerFactory` - Factory for creating and managing loggers

#### Functions (`logger_factory.py`)

- `get_logger(name, level, structured, async_enabled, buffered)` - Gets a logger with the specified configuration
- `get_structured_logger(name, level)` - Gets a structured logger
- `get_async_logger(name, level, buffered)` - Gets an asynchronous logger
- `get_structured_async_logger(name, level, buffered)` - Gets a structured asynchronous logger

### [`logging_endpoint.py`](logging_endpoint.py)

Logging endpoint for configuring the logger via HTTP.

#### Functions (`logging_endpoint.py`)

- `configure_logging_endpoint(request)` - Handles requests to configure the logger

### [`performance_monitor.py`](performance_monitor.py)

Performance monitor for tracking and measuring logging operation performance.

#### Classes (`performance_monitor.py`)

- `PerformanceMonitor` - Performance monitor
- `PerformanceTimer` - Context manager for timing operations

#### Functions (`performance_monitor.py`)

- `get_performance_monitor()` - Gets the global performance monitor instance
- `start_operation(operation_name)` - Starts timing an operation
- `end_operation(operation_id, success)` - Ends timing an operation
- `record_metric(metric_name, value, tags)` - Records a custom metric
- `get_performance_report()` - Gets a performance report
- `time_operation(operation_name)` - Decorator for timing operations

### [`structured_log_formatter.py`](structured_log_formatter.py)

Structured log formatters for output in JSON and key-value formats.

#### Classes (`structured_log_formatter.py`)

- `StructuredLogFormatter` - JSON log formatter
- `KeyValueLogFormatter` - Key-value log formatter

## Logging Levels

- `NOTSET` < `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`

- `DEBUG` - the most detailed information, needed only by the developer and only for debugging, for example variable values, what data was received, etc.
- `INFO` - informational messages, as confirmation of work, for example launching a service.
- `WARNING` - not yet an error, but already worth looking at - low disk space, low memory, many created objects, etc.
- `ERROR` - the application is still running and can work, but something went wrong.
- `CRITICAL` - the application cannot work further.

## Usage

### Basic Usage

```python
from metaexpert.logger import setup_logger, get_logger

# Set up the logger
logger = setup_logger("my_app", level="INFO")

# Use the logger
logger.info("Application started")
logger.warning("Warning")
logger.error("Error")
```

### Structured Logging

```python
from metaexpert.logger import setup_logger

# Set up a structured logger
logger = setup_logger("my_app", level="INFO", structured=True)

# Use the logger
logger.info("Message with structured data", extra={"user_id": 123, "action": "login"})
```

### Asynchronous Logging

```python
from metaexpert.logger import setup_logger

# Set up an asynchronous logger
logger = setup_logger("my_app", level="INFO", async_enabled=True)

# Use the logger
logger.info("Asynchronous message")
```

### Buffered Asynchronous Logging

```python
from metaexpert.logger import setup_logger

# Set up a buffered asynchronous logger
logger = setup_logger("my_app", level="INFO", async_enabled=True, buffered=True)

# Use the logger
logger.info("Buffered asynchronous message")
