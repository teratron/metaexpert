# Data Model: Logger Module Improvement

## Core Entities

### LogEntry
Represents a single log record with timestamp, severity level, message content, and associated metadata.

**Fields**:
- timestamp: datetime - UTC timestamp when log entry was created
- level: str - Severity level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- logger_name: str - Name of the logger that created this entry
- message: str - Main log message content
- module: str - Module where log entry was created
- function: str - Function where log entry was created
- line_number: int - Line number where log entry was created
- thread_id: str - Identifier of thread that created log entry
- process_id: str - Identifier of process that created log entry
- exception_info: dict | None - Exception details if applicable
- stack_info: str | None - Stack trace information if applicable
- extra_fields: dict - Additional context data as key-value pairs
- log_type: str - Type of log entry (general, trade, error, performance)
- trade_data: dict | None - Trade-specific data if log_type is 'trade'
- error_context: dict | None - Error-specific context if log_type is 'error'

**Relationships**:
- Belongs to one LogConfiguration
- Can be associated with one LogDestination
- May reference one parent LogEntry (for nested operations)

### LogConfiguration
Represents logging configuration parameters including destinations, formats, levels, retention policies, and performance settings.

**Fields**:
- name: str - Unique identifier for this configuration
- log_level: str - Minimum severity level to log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- structured_logging: bool - Whether to use structured JSON logging
- async_logging: bool - Whether to use asynchronous logging
- log_to_console: bool - Whether to output logs to console
- console_log_level: str | None - Console-specific log level
- file_log_level: str | None - File-specific log level
- retention_days: int - Number of days to retain log files
- max_file_size: int - Maximum size of log files in bytes
- backup_count: int - Number of backup files to keep
- enable_compression: bool - Whether to compress rotated log files
- enable_encryption: bool - Whether to encrypt log files
- remote_destinations: list - List of remote log destinations with connection details
- buffer_size: int - Size of log buffer for I/O optimization
- async_queue_size: int - Maximum size of asynchronous logging queue
- overflow_strategy: str - Strategy for handling queue overflow (drop, block, increase)
- rate_limit_enabled: bool - Whether rate limiting is enabled
- max_logs_per_second: int | None - Maximum log entries per second if rate limiting enabled

**Relationships**:
- Contains multiple LogDestinations
- References multiple LogFormatters
- May be associated with multiple LogEntries

### LogDestination
Represents output targets for log entries including file systems, consoles, network endpoints, and cloud services with specific connection parameters.

**Fields**:
- name: str - Human-readable name for this destination
- type: str - Type of destination (file, console, syslog, http, tcp, udp)
- path: str | None - File path or network address
- port: int | None - Network port if applicable
- protocol: str | None - Network protocol (tcp, udp, tls)
- authentication: dict | None - Authentication details if required
- format_name: str - Name of formatter to use for this destination
- enabled: bool - Whether this destination is currently active
- tls_enabled: bool - Whether TLS encryption is enabled for network destinations
- tls_verify: bool - Whether to verify TLS certificates
- compression_enabled: bool - Whether to compress log data for this destination
- batch_size: int - Number of log entries to batch before sending
- batch_timeout: float - Maximum time to wait before sending batch

**Relationships**:
- Belongs to one LogConfiguration
- Uses one LogFormatter
- Receives multiple LogEntries

### LogFormatter
Represents formatting rules for converting log records into human-readable or machine-parseable formats including JSON, XML, and plain text variants.

**Fields**:
- name: str - Unique identifier for this formatter
- type: str - Type of formatting (json, xml, text, custom)
- include_timestamp: bool - Whether to include timestamp in output
- timestamp_format: str | None - Format string for timestamps
- include_level: bool - Whether to include log level in output
- include_logger_name: bool - Whether to include logger name in output
- include_module: bool - Whether to include module name in output
- include_function: bool - Whether to include function name in output
- include_line_number: bool - Whether to include line number in output
- include_thread_info: bool - Whether to include thread information
- include_process_info: bool - Whether to include process information
- include_exception_info: bool - Whether to include exception details
- include_stack_info: bool - Whether to include stack trace information
- custom_fields: dict - Custom field mappings and transformations
- field_separator: str | None - Separator for text format
- indent_json: bool | None - Whether to indent JSON output

**Relationships**:
- Used by multiple LogDestinations
- Processes multiple LogEntries

### AsyncLogQueue
Represents the asynchronous logging buffer system with configurable size limits, overflow handling strategies, and worker thread management.

**Fields**:
- name: str - Unique identifier for this queue
- max_size: int - Maximum number of log entries the queue can hold
- current_size: int - Current number of log entries in queue
- overflow_strategy: str - Strategy for handling overflow (drop_oldest, drop_newest, block, increase_temporarily)
- worker_thread_status: str - Current status of worker thread (running, stopped, error)
- dropped_entries_count: int - Number of log entries dropped due to overflow
- processed_entries_count: int - Number of log entries successfully processed
- error_count: int - Number of errors encountered during processing
- last_error: str | None - Description of last error if any occurred
- batch_size: int - Number of entries to process in each batch
- batch_timeout: float - Maximum time to wait for batch completion

**Relationships**:
- Associated with one LogConfiguration
- Processes LogEntries from multiple Loggers
- Feeds LogEntries to multiple LogHandlers

### LogMetrics
Represents performance and operational metrics for the logging system.

**Fields**:
- timestamp: datetime - Time when metrics were collected
- log_entries_created: int - Total number of log entries created
- log_entries_processed: int - Total number of log entries processed
- log_entries_dropped: int - Total number of log entries dropped
- async_queue_depth: int - Current depth of asynchronous logging queue
- memory_usage_bytes: int - Memory used by logging system
- cpu_time_seconds: float - CPU time consumed by logging operations
- io_operations_count: int - Number of I/O operations performed
- network_bytes_sent: int - Total bytes sent to remote destinations
- network_errors_count: int - Number of network errors encountered
- file_rotation_count: int - Number of file rotations performed
- compression_ratio: float | None - Average compression ratio achieved

**Relationships**:
- Collected from one LogConfiguration
- Aggregated from multiple LogDestinations

## Validation Rules

### LogEntry Validation
- timestamp must be a valid datetime
- level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- message must not be empty
- module name must conform to Python module naming conventions
- function name must conform to Python function naming conventions
- line_number must be a positive integer
- log_type must be one of general, trade, error, performance

### LogConfiguration Validation
- log_level must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL
- retention_days must be a positive integer
- max_file_size must be a positive integer
- backup_count must be a non-negative integer
- buffer_size must be a positive integer
- async_queue_size must be a positive integer
- overflow_strategy must be one of drop_oldest, drop_newest, block, increase_temporarily
- max_logs_per_second must be a positive integer if rate limiting is enabled

### LogDestination Validation
- type must be one of file, console, syslog, http, tcp, udp
- path must be a valid file path or network address
- port must be between 1 and 65535 if specified
- protocol must be one of tcp, udp, tls if specified
- format_name must reference an existing LogFormatter

### LogFormatter Validation
- type must be one of json, xml, text, custom
- timestamp_format must be a valid Python strftime format if specified
- field_separator must be a single character if specified
- indent_json must be a boolean if specified

### AsyncLogQueue Validation
- max_size must be a positive integer
- overflow_strategy must be one of drop_oldest, drop_newest, block, increase_temporarily
- batch_size must be a positive integer
- batch_timeout must be a positive number

## State Transitions

### LogEntry States
1. **Created** → **Queued** (when added to AsyncLogQueue)
2. **Queued** → **Processing** (when worker thread begins processing)
3. **Processing** → **Completed** (when successfully written to all destinations)
4. **Processing** → **Failed** (when error occurs during processing)
5. **Failed** → **Retrying** (when automatic retry is attempted)
6. **Failed** → **Abandoned** (when retries are exhausted)

### AsyncLogQueue States
1. **Initialized** → **Running** (when worker thread starts)
2. **Running** → **Paused** (when system requests pause)
3. **Paused** → **Running** (when system resumes operation)
4. **Running** → **Stopped** (when system shuts down)
5. **Stopped** → **Initialized** (when system restarts)

### LogDestination States
1. **Configured** → **Active** (when destination is enabled and available)
2. **Active** → **Degraded** (when errors occur but destination is still usable)
3. **Degraded** → **Failed** (when destination becomes unusable)
4. **Failed** → **Recovering** (when automatic recovery is attempted)
5. **Recovering** → **Active** (when recovery succeeds)
6. **Recovering** → **Inactive** (when recovery fails)