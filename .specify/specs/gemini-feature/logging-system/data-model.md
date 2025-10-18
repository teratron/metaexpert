# Data Model: Logging System

**Date**: 2025-10-17

This document outlines the conceptual data models and key entities for the Comprehensive Logging System feature. These are not database schemas but rather descriptions of the primary objects and their roles within the system.

## Core Entities

### 1. `LogRecord`

A structured, immutable data object representing a single log event.

- **Attributes**:
  - `timestamp` (datetime): The UTC time when the event occurred. Added by a processor.
  - `level` (str): The severity of the event (e.g., `INFO`, `CRITICAL`). Added by a processor.
  - `event` (str): The core, human-readable message for the log entry.
  - `context` (dict): A dictionary of key-value pairs providing situational context (e.g., `expert_name`, `symbol`, `order_id`). This is an aggregation of all bound data.
  - `exception_info` (str, optional): Formatted stack trace if the log was triggered by an exception.

- **Relationships**:
  - A `LogRecord` is created by a `Logger` instance and passed through a chain of `Processor`s before being sent to one or more `Handler`s.

### 2. `Logger`

The primary user-facing interface for creating log entries. In this architecture, it is a `structlog` logger instance.

- **Attributes**:
  - `bound_context` (dict): Key-value pairs that are permanently attached to this logger instance and included with every `LogRecord` it generates.

- **Methods**:
  - `info(event, **kwargs)`: Creates a `LogRecord` with level `INFO`.
  - `warning(event, **kwargs)`: Creates a `LogRecord` with level `WARNING`.
  - `error(event, **kwargs)`: Creates a `LogRecord` with level `ERROR`.
  - `critical(event, **kwargs)`: Creates a `LogRecord` with level `CRITICAL`.
  - `bind(**kwargs)`: Returns a *new* `Logger` instance with additional context bound to it.

### 3. `Handler`

A component responsible for dispatching a finalized `LogRecord` to a specific destination.

- **Key Implementations**:
  - `FileHandler`: Writes log records to a specified file (e.g., `expert.log`). Manages file rotation.
  - `ConsoleHandler`: Formats and prints log records to the standard output (console).
  - `WebhookHandler`: Serializes the log record to JSON and sends it to a configured HTTP endpoint via a POST request. This handler will only be triggered for `CRITICAL` level events.

- **Relationships**:
  - A `Logger` is configured with one or more `Handler`s. A single `LogRecord` can be sent to multiple handlers based on filtering rules (e.g., log level).

### 4. `Processor`

A function that receives a `LogRecord` (or a nascent version of it), modifies it, and passes it to the next processor in a chain. Processors are the core mechanism for enrichment and formatting.

- **Key Responsibilities**:
  - `add_timestamp`: Adds the current UTC timestamp to the log.
  - `add_log_level`: Adds the log level name (e.g., "INFO").
  - `merge_contextvars`: Merges context from `contextvars` into the log's context.
  - `format_exception`: Renders a stack trace into a string.
  - `JSONRenderer`: The final processor in a file-logging chain; serializes the entire log record into a JSON string.
  - `ConsoleRenderer`: The final processor in a console-logging chain; formats the log record into a human-readable, colored string.

## Configuration Models

### `LoggerConfig` (Pydantic Model)

A Pydantic model that declaratively defines the entire logging setup. An instance of this model is used by the `MetaLogger` factory.

- **Attributes**:
  - `log_level` (str): The minimum log level to process (e.g., `"INFO"`).
  - `log_to_console` (bool): Enable or disable console output.
  - `structured_logging` (bool): If `True`, file and webhook logs are JSON; otherwise, plain text.
  - `async_logging` (bool): If `True`, file I/O is performed in a separate thread/task to avoid blocking.
  - `log_file` (str): Path to the main log file.
  - `trade_log_file` (str): Path to the trades-only log file.
  - `error_log_file` (str): Path to the errors-only log file.
  - `webhook_url` (str, optional): The URL for critical alert notifications.
  - `rotation_size_mb` (int): Max file size in megabytes before rotation.
  - `rotation_backup_count` (int): Number of backup log files to keep.
