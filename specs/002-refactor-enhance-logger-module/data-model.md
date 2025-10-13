# Data Model: Structured Log Record

This document defines the data structure for the JSON log entries that will be produced by the enhanced logger.

## Log Record Schema

Each log entry will be a JSON object containing a standard set of fields, with the ability to include arbitrary additional context.

| Field | Type | Description | Required |
|---|---|---|---|
| `event` | `str` | The main log message. | Yes |
| `level` | `str` | The log level (e.g., `info`, `warning`, `error`). | Yes |
| `timestamp` | `str` | An ISO 8601 formatted timestamp (e.g., `2025-10-12T10:00:00.123Z`). | Yes |
| `logger_name` | `str` | The name of the logger instance. | Yes |
| `source_path` | `str` | The file path of the code that generated the log entry. | No |
| `line_number` | `int` | The line number in the source file. | No |
| `function_name` | `str` | The name of the function or method that generated the log entry. | No |

## Bound and Contextual Fields

In addition to the standard schema, the logger will support adding arbitrary key-value pairs to the log entry. This is the primary mechanism for providing context.

## Field Validation and Sanitization

The logger MUST validate and sanitize all fields before serializing to JSON:
- Non-serializable objects MUST be converted to string representation or omitted
- Circular references MUST be detected and handled gracefully
- Field names with special characters that are not valid JSON keys MUST be sanitized

### Example

A call like this:

```python
log = logger.bind(strategy_name="ema_cross", exchange="binance")
log.info("Order placed", order_id="12345", symbol="BTC/USDT")
```

Will produce a JSON log similar to this:

```json
{
  "event": "Order placed",
  "level": "info",
  "timestamp": "2025-10-12T10:00:05.456Z",
  "logger_name": "metaexpert.strategy",
  "source_path": "/path/to/your/strategy.py",
  "line_number": 42,
  "function_name": "execute_trade",
  "strategy_name": "ema_cross",
  "exchange": "binance",
  "order_id": "12345",
  "symbol": "BTC/USDT"
}
```

### Error Handling Example

When the logger handles non-serializable objects:

```python
import threading
lock = threading.Lock()
log.info("Debug info", resource_lock=lock, user_data={"id": 123})
```

Will produce a JSON log with sanitized representation:

```json
{
  "event": "Debug info",
  "level": "info",
  "timestamp": "2025-10-12T10:00:05.456Z",
  "logger_name": "metaexpert.logger",
  "resource_lock": "<thread.lock object at 0x...>",
  "user_data": {"id": 123}
}
```
