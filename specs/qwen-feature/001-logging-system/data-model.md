# Data Model for Comprehensive Logging System

## Overview
This document defines the entities, their attributes, relationships, and validation rules for the MetaExpert logging system.

## Entities

### 1. LogConfiguration (Pydantic Model)

**Description**: Configuration model for the logging system that supports multiple configuration methods with priority ordering.

**Fields**:
- `log_level` (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) - Default: "INFO"
- `log_directory` (str): Directory path for log files - Default: "./logs"
- `expert_log_file` (str): Filename for expert logs - Default: "expert.log"
- `trades_log_file` (str): Filename for trades logs - Default: "trades.log" 
- `errors_log_file` (str): Filename for errors logs - Default: "errors.log"
- `enable_async` (bool): Enable asynchronous logging - Default: False
- `max_file_size_mb` (int): Maximum file size before rotation - Default: 10
- `backup_count` (int): Number of backup files to keep - Default: 5
- `enable_structured_logging` (bool): Enable RFC 5424 structured JSON format - Default: False
- `enable_contextual_logging` (bool): Enable contextual field inclusion - Default: True
- `mask_sensitive_data` (bool): Enable masking of sensitive information - Default: True
- `console_log_format` (str): Format for console logs ("text" or "json") - Default: "text"
- `file_log_format` (str): Format for file logs ("text" or "json") - Default: "json"
- `context_fields` (List[str]): List of contextual fields to include - Default: ["expert_name", "symbol", "trade_id", "order_id", "strategy_id", "account_id"]

**Validation Rules**:
- `log_level` must be one of ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
- `log_directory` must be a valid, writable directory path
- `max_file_size_mb` must be between 1 and 1000
- `backup_count` must be between 1 and 100
- `context_fields` must contain only valid field names from the pre-defined list

**Environment Variable Aliases**:
- `LOG_LEVEL` -> `log_level`
- `LOG_DIRECTORY` -> `log_directory`
- `EXPERT_LOG_FILE` -> `expert_log_file`
- `TRADES_LOG_FILE` -> `trades_log_file`
- `ERRORS_LOG_FILE` -> `errors_log_file`
- `ENABLE_ASYNC` -> `enable_async`
- `MAX_FILE_SIZE_MB` -> `max_file_size_mb`
- `BACKUP_COUNT` -> `backup_count`
- `ENABLE_STRUCTURED_LOGGING` -> `enable_structured_logging`
- `ENABLE_CONTEXTUAL_LOGGING` -> `enable_contextual_logging`
- `MASK_SENSITIVE_DATA` -> `mask_sensitive_data`

### 2. LogEntry

**Description**: Represents a single log entry with all required fields for RFC 5424 compliance.

**Fields**:
- `timestamp` (datetime): ISO 8601 timestamp of the log entry
- `severity` (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `message` (str): Main log message content
- `expert_name` (str): Name of the trading expert generating the log
- `symbol` (str): Trading symbol if applicable
- `trade_id` (str): Unique identifier for the trade if applicable
- `order_id` (str): Order ID if applicable
- `strategy_id` (str): Strategy identifier if applicable
- `account_id` (str): Account identifier if applicable
- `function` (Optional[str]): Function name where log was generated
- `file` (Optional[str]): Source file where log was generated
- `line` (Optional[int]): Line number in source file
- `exception_details` (Optional[dict]): Exception information if logging an error

**Validation Rules**:
- `timestamp` must be in ISO 8601 format
- `severity` must be one of ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
- `message` must not be empty
- `expert_name` must be provided for all entries
- At least one of `symbol`, `trade_id`, `order_id`, `strategy_id`, `account_id` should be present

### 3. LogContext

**Description**: Contextual information manager that can bind fields to log entries.

**Fields**:
- `expert_name` (str): Name of the trading expert
- `symbol` (str): Trading symbol
- `trade_id` (str): Trade identifier
- `order_id` (str): Order identifier
- `strategy_id` (str): Strategy identifier
- `account_id` (str): Account identifier
- `custom_fields` (Dict[str, Any]): Additional custom contextual fields

**Validation Rules**:
- At least one of the core context fields must be present
- Field values must be JSON serializable
- Context can be nested, with inner context taking precedence over outer context

### 4. LogHandler

**Description**: Abstract handler for different types of log outputs.

**Fields**:
- `name` (str): Name of the handler
- `level` (str): Minimum level to handle
- `formatter` (LogFormatter): Formatter to use for this handler
- `enabled` (bool): Whether this handler is active

**Validation Rules**:
- Name must be unique across all handlers
- Level must be a valid log level
- Formatter must be provided

### 5. LogFormatter

**Description**: Defines how log entries should be formatted.

**Fields**:
- `format_type` (str): Type of format ("text", "json", "rfc5424")
- `template` (str): Format template when using text format
- `include_context` (bool): Whether to include contextual fields
- `include_timestamp` (bool): Whether to include timestamp
- `timestamp_format` (str): Format for timestamps

**Validation Rules**:
- `format_type` must be one of ["text", "json", "rfc5424"]
- When `format_type` is "rfc5424", `include_context` must be True

## State Transitions

### LogConfiguration State Transitions
1. **Configuration Creation**: LogConfiguration object is created with defaults
2. **Parameter Binding**: Parameters from CLI, environment, or code are bound
3. **Validation**: Configuration is validated against rules
4. **Activation**: Configuration is applied to the logger
5. **Runtime Change**: Configuration can be changed at runtime (with appropriate locks)

### Log Handler State Transitions
1. **Initialization**: Handler is created with configuration
2. **Activation**: Handler is enabled and starts processing logs
3. **Error State**: Handler fails and enters error recovery
4. **Fallback Mode**: Handler switches to fallback (console only) when needed
5. **Shutdown**: Handler is properly closed during application shutdown

## Relationships

### LogConfiguration → LogHandler
- One-to-many relationship: One configuration can be applied to multiple handlers
- Configuration parameters determine handler creation and behavior

### LogEntry → LogHandler
- One-to-many relationship: One log entry can be sent to multiple handlers if they match the filtering criteria

### LogContext → LogEntry
- One-to-many relationship: Context can be applied to multiple log entries within its scope

### LogHandler → LogFormatter
- One-to-one relationship: Each handler uses one formatter