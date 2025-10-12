# Logger Public API Contract

This document defines the public interface for the logger module that MUST be preserved after the refactoring to ensure backward compatibility.

## Obtaining a Logger Instance

A logger instance is obtained via the `get_logger` function.

```python
from metaexpert.logger import get_logger

log = get_logger(__name__)
```

## Standard Logging Methods

The logger instance MUST support the standard logging methods.

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
