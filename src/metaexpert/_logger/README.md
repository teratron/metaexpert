# MetaExpert Logging Module

This module provides a robust and flexible logging system for the MetaExpert trading framework, built upon `structlog` for structured logging. It offers advanced features such as asynchronous logging, specialized handlers for different log types (main, trade, error), and flexible configuration.

## Key Features

* **Structured Logging with `structlog`**: Leverages `structlog` to provide human-readable or JSON-formatted logs, making it easier to parse and analyze log data.
* **Asynchronous Logging**: Utilizes [`AsyncHandler`](src/metaexpert/logger/async_handler.py:9) to offload logging operations to a separate thread, ensuring non-blocking log writes and improving application performance.
* **Configurable Logger**: The [`MetaLogger`](src/metaexpert/logger/__init__.py:31) class allows for extensive customization of logging behavior, including log levels, file paths, console output, and structured logging preferences, all managed through a [`LoggerConfig`](src/metaexpert/logger/config.py:30) object.
* **Specialized Loggers**: Provides dedicated loggers for main application events, trade-specific activities, and error reporting, allowing for granular control and easier filtering of log messages.
* **Centralized Configuration**: The initialization of `MetaLogger` streamlines the setup of `structlog` processors and logging handlers by centralizing their creation and setup logic, promoting consistent and efficient logging across the application.

## Usage

The `MetaLogger` class is designed to be easily configurable and integrated into your MetaExpert applications.

### Basic Initialization

```python
from metaexpert.logger import MetaLogger

# Initialize the logger with default settings
logger = MetaLogger.create(
    log_level="INFO",
    log_file="application.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    console_logging=True,
    structured_logging=False,
    async_logging=True,
)

# Get specific loggers
main_logger = logger.get_main_logger()
trade_logger = logger.get_trade_logger()
error_logger = logger.get_error_logger()

# Log messages
main_logger.info("Application started.")
trade_logger.info("Trade executed successfully", symbol="BTC/USDT", price=60000, quantity=0.01)
try:
    raise ValueError("Something went wrong!")
except ValueError as e:
    error_logger.error("An error occurred", exception=e)
```

### Configuration with `LoggerConfig`

The logging behavior is dictated by the [`LoggerConfig`](src/metaexpert/logger/config.py:30) object, which can be customized to your needs.

```python
from metaexpert.logger.config import LoggerConfig
from metaexpert.logger import MetaLogger

# Custom configuration
custom_config = LoggerConfig(
    log_level="DEBUG",
    log_file="my_app.log",
    console_logging=False,
    structured_logging=True,
    async_logging=False,
    log_directory="./custom_logs",
)

# Initialize MetaLogger using the custom config
# Note: The MetaLogger.create method directly accepts the configuration parameters
# and internally constructs a LoggerConfig object.
logger = MetaLogger.create(
    log_level=custom_config.log_level,
    log_file=custom_config.log_file,
    trade_log_file=custom_config.trade_log_file,
    error_log_file=custom_config.error_log_file,
    console_logging=custom_config.console_logging,
    structured_logging=custom_config.structured_logging,
    async_logging=custom_config.async_logging,
)

main_logger = logger.get_main_logger()
main_logger.debug("Debug message from custom config.")
```

## Asynchronous Logging

The module supports asynchronous logging via [`AsyncHandler`](src/metaexpert/logger/async_handler.py:9), which wraps standard logging handlers. When `async_logging` is set to `True` during `MetaLogger` initialization, all file handlers will use `AsyncHandler` to write logs in a non-blocking manner.
