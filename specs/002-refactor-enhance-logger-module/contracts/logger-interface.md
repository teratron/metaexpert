# Logger Public API Contract

This document defines the public interface for the logger module that MUST be preserved after the refactoring to ensure backward compatibility.

## Obtaining a Logger Instance

A logger instance is obtained via the `get_logger` function with the same signature and behavior as the original implementation.

```python
from metaexpert.logger import get_logger

log = get_logger(__name__)
```

## Standard Logging Methods

The logger instance MUST support the standard logging methods with the exact same signatures:

- `log.debug(message, *args, **kwargs)`
- `log.info(message, *args, **kwargs)`
- `log.warning(message, *args, **kwargs)`
- `log.error(message, *args, **kwargs)`
- `log.critical(message, *args, **kwargs)`
- `log.exception(message, *args, **kwargs)`

## Contextualization

While the new implementation will use `structlog`'s `bind()` internally and for new use cases, the existing method of passing an `extra` dictionary MUST continue to work for backward compatibility. The data from the `extra` dictionary should be merged into the structured log record.

### Example (Legacy Support)

```python
# This style must continue to work.
log.info("User logged in", extra={"user_id": 123, "ip_address": "192.168.1.1"})
```

This would produce a log entry containing `"user_id": 123` and `"ip_address": "192.168.1.1"`.

## New Structured Logging Interface

The logger MUST also support direct keyword arguments for structured logging:

```python
# This new style should be supported.
log.info("Order placed", order_id="12345", symbol="BTC/USDT", amount=0.1)
```

This would produce a structured log entry with the provided key-value pairs.

## Context Binding

The logger MUST support context binding to persist contextual information across multiple log calls:

```python
# Context binding should be supported.
strategy_log = log.bind(strategy_name="ema_cross_strategy", version="1.2")

strategy_log.info("Strategy starting...", timestamp="2025-01-01T10:00:00Z")
strategy_log.info("Signal detected.", signal_strength=0.85)
strategy_log.error("Failed to execute trade.", error_code="E1001")
```

All messages from `strategy_log` will automatically contain the `strategy_name` and `version` fields.
