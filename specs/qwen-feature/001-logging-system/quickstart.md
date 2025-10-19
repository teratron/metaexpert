# Quickstart Guide: Comprehensive Logging System

## Overview

This guide provides a quick introduction to implementing and using the MetaExpert logging system. It covers basic setup and common usage patterns.

## Installation

The logging system is included as part of the MetaExpert library. No additional installation is required.

## Basic Setup

### 1. Initialize the Logger

```python
from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration

# Create a basic logger configuration
config = LogConfiguration(
    log_level="INFO",
    enable_async=True,
    enable_structured_logging=True,
    enable_contextual_logging=True
)

# Initialize the logger
logger = MetaLogger(config)
```

### 2. Configure via Environment Variables

```bash
export LOG_LEVEL="DEBUG"
export LOG_DIRECTORY="./custom_logs"
export ENABLE_ASYNC="true"
export ENABLE_STRUCTURED_LOGGING="true"
```

Then initialize with environment-based config:

```python
from metaexpert.logger.config import LogConfiguration

config = LogConfiguration()  # Will read from environment variables
logger = MetaLogger(config)
```

### 3. Configure via Code Parameters

```python
from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration

config = LogConfiguration(
    log_level="DEBUG",
    log_directory="./logs",
    expert_log_file="expert.log",
    trades_log_file="trades.log",
    errors_log_file="errors.log",
    enable_async=True,
    max_file_size_mb=25,
    backup_count=10,
    enable_structured_logging=True,
    enable_contextual_logging=True,
    mask_sensitive_data=True
)

logger = MetaLogger(config)
```

## Basic Usage

### 1. Create Different Log Types

```python
# General expert logs
logger.info("Expert initialized successfully", extra={
    "expert_name": "MyTradingExpert",
    "symbol": "BTCUSDT"
})

# Trade-specific logs
logger.trade("Order placed", extra={
    "trade_id": "trade_123",
    "order_id": "order_456",
    "symbol": "BTCUSDT",
    "strategy_id": "ema_strategy"
})

# Error logs
try:
    # some operation
    pass
except Exception as e:
    logger.error("Error occurred during trading operation", 
                 extra={"expert_name": "MyTradingExpert", "symbol": "BTCUSDT"},
                 exc_info=True)
```

### 2. Use Contextual Logging

```python
# Bind contextual information
with logger.context(
    expert_name="MyTradingExpert",
    symbol="BTCUSDT",
    account_id="account_789"
):
    logger.info("Processing trade")
    # All logs inside this context will include the contextual information
    logger.trade("Order executed", extra={"trade_id": "trade_123"})
```

### 3. Advanced Configuration

```python
from metaexpert.logger import MetaLogger
from metaexpert.logger.config import LogConfiguration

config = LogConfiguration(
    log_level="DEBUG",
    enable_async=True,
    max_file_size_mb=50,
    backup_count=20,
    enable_structured_logging=True,
    enable_contextual_logging=True,
    mask_sensitive_data=True,
    context_fields=["expert_name", "symbol", "trade_id", "order_id"]
)

logger = MetaLogger(config)
```

## Integration with MetaExpert

### 1. Using the Logger in Trading Experts

```python
from metaexpert import MetaExpert

# The logger is automatically available via the MetaExpert instance
expert = MetaExpert()
expert.logger.info("Expert initialized", extra={"symbol": "BTCUSDT"})

# You can also pass custom configuration
config = LogConfiguration(log_level="DEBUG")
expert_with_logging = MetaExpert(logger_config=config)
```

### 2. Adding Context to Trading Operations

```python
from metaexpert import MetaExpert

# Set context when creating expert
expert = MetaExpert(
    logger_config=LogConfiguration(
        log_level="INFO", 
        enable_contextual_logging=True
    )
)

# The logger in the expert automatically includes relevant context
expert.logger.trade("Placing buy order", extra={
    "symbol": "BTCUSDT",
    "strategy_id": "ema_strategy"
})
```

## Performance Considerations

### Async Logging Setup

For high-frequency trading, use asynchronous logging to avoid blocking:

```python
config = LogConfiguration(
    enable_async=True,  # Enable async logging
    log_level="INFO"    # Avoid DEBUG in production for performance
)
logger = MetaLogger(config)
```

### Batch Logging for Performance

When logging many events, consider the performance impact:

```python
# For many log entries, async mode will handle performance automatically
with logger.context(symbol="BTCUSDT", expert_name="HighFreqExpert"):
    for i in range(10000):
        logger.debug(f"Processing tick {i}")
```

## Error Handling and Fallbacks

The system is designed to continue operating even when logging fails:

```python
# The logger will continue operating even if:
# - Disk is full
# - Log file is locked
# - Write permissions fail

# In such cases, it falls back to console logging
logger.warn("Disk full - switching to console-only logging mode")
```

## Best Practices

1. **Use appropriate log levels**: DEBUG for detailed debugging, INFO for general info,
   WARNING for potential issues, ERROR for errors, CRITICAL for critical issues

2. **Include contextual information**: At minimum, include expert_name and symbol in logs

3. **Avoid logging sensitive data**: The system will mask sensitive info, but avoid logging
   sensitive data when possible

4. **Use structured logging**: Enable structured logging for better analysis capabilities

5. **Configure appropriate log retention**: Set max file size and backup count based on
   your storage constraints and analysis needs

## Configuration Priority Order

Configuration parameters follow this priority order (highest to lowest):
1. Code parameters (passed directly to LogConfiguration constructor)
2. Environment variables
3. Default values

Example:
```python
# Even if LOG_LEVEL is set to "INFO" in environment,
# this will use "DEBUG" because code parameters have higher priority
config = LogConfiguration(log_level="DEBUG")
```