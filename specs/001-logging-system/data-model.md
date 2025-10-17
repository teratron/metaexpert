# Data Model: Comprehensive Logging System

## Entities

### MetaLogger
**Description**: The main logger factory and configuration handler that sets up structlog with appropriate processors, formatters, and handlers.

**Fields**:
- `logger`: The configured structlog logger instance
- `config`: Reference to the configuration model
- `handlers`: Collection of active handlers (console, file, async file)

**Relationships**:
- Uses `LogConfiguration` for initialization parameters
- Creates multiple handlers based on configuration

### LogConfiguration
**Description**: A Pydantic model that defines all configurable logging parameters with environment variable aliases and default values.

**Fields**:
- `log_level`: str - The minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_file`: str - Path for the main log file (default: "expert.log")
- `trade_log_file`: str - Path for the trade log file (default: "trades.log")
- `error_log_file`: str - Path for the error log file (default: "errors.log")
- `log_to_console`: bool - Whether to output to console (default: True)
- `structured_logging`: bool - Whether to use JSON format (default: False)
- `async_logging`: bool - Whether to use async logging (default: False)
- `log_max_file_size`: int - Max size in bytes before rotation (default: 10485760)
- `log_backup_count`: int - Number of backup files to keep (default: 5)

**Validation Rules**:
- `log_level` must be one of the standard log levels
- `log_max_file_size` must be positive
- `log_backup_count` must be non-negative

### LogProcessors
**Description**: A chain of structlog processors that enrich, format, and route log entries appropriately.

**Fields**:
- `processor_chain`: List of processor functions
- `context_processors`: Processors that add contextual information
- `format_processors`: Processors that format the log entry

### LogHandlers
**Description**: Specialized handlers for console output, file output, and asynchronous file output with rotation capabilities.

**Fields**:
- `console_handler`: Handler for console output
- `file_handler`: Handler for file output with rotation
- `async_handler`: Async handler for non-blocking logging
- `error_handler`: Specialized handler for error logs
- `trade_handler`: Specialized handler for trade logs

### LogContext
**Description**: Domain-specific contextual information (expert_name, symbol, trade_id, etc.) that gets automatically added to log entries.

**Fields**:
- `expert_name`: str - Name of the trading expert
- `symbol`: str - Trading symbol (e.g., BTCUSDT)
- `trade_id`: str - Unique identifier for the trade
- `order_id`: str - Unique identifier for the order
- `strategy_id`: str - Identifier for the trading strategy
- `account_id`: str - Identifier for the trading account

**State Transitions**:
- Context information is bound to loggers when creating specialized loggers for different operations

## Relationships

- `MetaLogger` uses `LogConfiguration` to initialize the logging system
- `MetaLogger` creates and manages multiple `LogHandlers`
- `LogProcessors` are configured based on `LogConfiguration` settings
- `LogContext` information is used by `LogProcessors` to enrich log entries
- `LogHandlers` use `LogConfiguration` settings for file paths and rotation rules