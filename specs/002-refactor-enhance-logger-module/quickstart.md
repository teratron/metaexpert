# Quickstart: Using the Enhanced Logger

This guide shows how to use the refactored logger, including the new structured logging capabilities.

## Basic Logging

For basic logging, the API remains unchanged. You can get a logger and call the standard methods.

```python
from metaexpert.logger import get_logger

log = get_logger(__name__)

log.info("This is an informational message.")
log.warning("This is a warning.")
```

## Structured Logging (Recommended)

The primary enhancement is the ability to add structured context to your logs. This is done by passing keyword arguments to the logging methods.

### Example: Logging Order Data

```python
log.info(
    "Placing new order",
    symbol="BTC/USDT",
    order_type="LIMIT",
    side="BUY",
    amount=0.1,
    price=50000.0
)
```

This will produce a single JSON log entry containing all the provided key-value pairs, making it easy to search and analyze your logs.

```json
{
  "event": "Placing new order",
  "level": "info",
  "timestamp": "...",
  "symbol": "BTC/USDT",
  "order_type": "LIMIT",
  "side": "BUY",
  "amount": 0.1,
  "price": 50000.0
}
```

## Binding Context

For context that persists across multiple log calls (like a strategy name or exchange), you can use `bind()` to create a new logger with that context baked in.

```python
strategy_log = log.bind(strategy_name="ema_cross_strategy", version="1.2")

strategy_log.info("Strategy starting...")
# ... later ...
strategy_log.info("Signal detected.")
# ... later ...
strategy_log.error("Failed to execute trade.")
```

All messages from `strategy_log` will automatically contain the `strategy_name` and `version` fields.
