# Quickstart: Using the Logging System

**Date**: 2025-10-17

This guide provides a brief, practical example of how to use the new logging system within a MetaExpert strategy.

## Basic Usage

The logger is automatically initialized and available as `expert.logger`. You can use it directly in your event handlers.

```python
from metaexpert import MetaExpert

# 1. Initialize the expert
# The logger is configured automatically here.
expert = MetaExpert(exchange="binance", log_level="INFO")

@expert.on_init
def init():
    """Initialize the strategy."""
    expert.logger.info("Strategy is initializing...")

@expert.on_bar
def bar(rates):
    """Handle new bar data."""
    expert.logger.info(
        "Processing new bar", 
        open=rates.open,
        close=rates.close,
        volume=rates.volume
    )

    if rates.close > 100000:
        expert.logger.warning("Price exceeded high threshold!", threshold=100000)

# This will start the expert and its logger
if __name__ == "__main__":
    expert.run()
```

## Structured Logging (JSON)

To enable structured logging for better machine readability (e.g., for Logstash, Datadog), set `structured_logging=True`.

```python
expert = MetaExpert(
    exchange="binance",
    structured_logging=True
)
```

An `INFO` log from the example above would now be written to `expert.log` as a single JSON line:

```json
{"event": "Processing new bar", "open": 68000.5, "close": 68500.1, "volume": 1234.56, "level": "info", "timestamp": "2025-10-17T12:00:00Z"}
```

## Using Bound Context

Use `bind()` to add persistent context to your log messages. This is highly recommended for distinguishing logs from different sources.

```python
@expert.on_init
def init():
    # Create a logger specifically for this strategy instance
    # This is better than using expert.logger directly
    strategy_logger = expert.logger.bind(
        strategy_name="EMA_Cross_Strategy",
        symbol="BTCUSDT"
    )
    
    strategy_logger.info("Strategy logger initialized.")

# Later, in another function...
@expert.on_order
def on_order(order):
    strategy_logger.info("Order status updated", order_id=order.id, status=order.status)
```

Now, all logs from `strategy_logger` will automatically include `{"strategy_name": "EMA_Cross_Strategy", "symbol": "BTCUSDT"}`.

## Real-Time Critical Alerts

To receive alerts on critical failures, provide a webhook URL.

```python
expert = MetaExpert(
    exchange="binance",
    webhook_url="https://hooks.slack.com/services/YOUR-TEAM-ID/YOUR-CHANNEL-ID/YOUR-WEBHOOK-TOKEN"
)

# This will be logged to errors.log AND sent to the webhook
expert.logger.critical("FATAL: Could not connect to exchange API.")

# This will only be logged to errors.log
expert.logger.error("Order placement failed: insufficient funds.")
```
