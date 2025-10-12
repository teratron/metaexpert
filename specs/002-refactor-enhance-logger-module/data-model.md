# Data Model: Structured Log Record

This document defines the data structure for the JSON log entries that will be produced by the enhanced logger.

## Log Record Schema

Each log entry will be a JSON object containing a standard set of fields, with the ability to include arbitrary additional context.

| Field | Type | Description |
|---|---|---|
| `event` | `str` | The main log message. |
| `level` | `str` | The log level (e.g., `info`, `warning`, `error`). |
| `timestamp` | `str` | An ISO 8601 formatted timestamp (e.g., `2025-10-12T10:00:00.123Z`). |
| `logger_name` | `str` | The name of the logger instance. |
| `source_path` | `str` | The file path of the code that generated the log entry. |
| `line_number` | `int` | The line number in the source file. |
| `function_name` | `str` | The name of the function or method that generated the log entry. |

## Bound and Contextual Fields

In addition to the standard schema, the logger will support adding arbitrary key-value pairs to the log entry. This is the primary mechanism for providing context.

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
