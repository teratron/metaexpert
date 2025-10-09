# Quickstart Guide: Logger Module Improvement

## Overview
This guide will help you quickly get started with the enhanced logging capabilities of the MetaExpert trading library. The improved logger module provides structured JSON logging, asynchronous processing, and support for multiple output destinations.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- Basic understanding of logging concepts

## Installation

The enhanced logger module is part of the core MetaExpert library. If you haven't installed MetaExpert yet:

```bash
# Using UV (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install metaexpert

# Using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install metaexpert
```

## Basic Usage

### 1. Import and Configure the Logger

```python
from metaexpert import MetaExpert
from metaexpert.logger import get_logger

# Create a MetaExpert instance with enhanced logging
expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    api_secret="your_api_secret",
    # Enhanced logging configuration
    log_level="INFO",
    log_file="trading.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    log_to_console=True,
    structured_logging=True,  # Enable JSON structured logging
    async_logging=True,        # Enable asynchronous logging
)
```

### 2. Basic Logging

```python
# Get the main logger
logger = get_logger(__name__)

# Simple log messages
logger.info("Strategy started")
logger.warning("High volatility detected")
logger.error("Order placement failed")

# Structured logging with context
logger.info("Trade executed", extra={
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 45000.0,
    "order_id": "123456789"
})
```

### 3. Trade-Specific Logging

```python
# Log trade events with specialized formatting
expert.logger.log_trade(
    "Order placed",
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.1,
    price=45000.0,
    order_id="123456789"
)

# Log errors with stack traces
try:
    # Some trading operation
    pass
except Exception as e:
    expert.logger.log_error(
        "Failed to place order",
        exception=e,
        symbol="BTCUSDT",
        side="BUY",
        quantity=0.1
    )
```

## Advanced Configuration

### 1. Multi-Destination Logging

```python
# Configure logging to multiple destinations
expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    api_secret="your_api_secret",
    # Configure multiple log destinations
    log_level="DEBUG",
    log_file="main.log",           # Main log file
    trade_log_file="trades.log",   # Trade-specific log file
    error_log_file="errors.log",   # Error-specific log file
    log_to_console=True,           # Also log to console
    structured_logging=True,        # Use structured JSON logging
    async_logging=True,            # Use asynchronous logging for performance
)
```

### 2. Performance Monitoring

```python
import time

# Measure performance of trading operations
start_time = time.time()

# Your trading logic here
# ...

end_time = time.time()
duration = end_time - start_time

# Log performance metrics
expert.logger.info(
    "Strategy execution completed",
    extra={
        "duration_ms": duration * 1000,
        "symbols_traded": ["BTCUSDT", "ETHUSDT"],
        "orders_placed": 5,
        "performance": "optimal"
    }
)
```

### 3. Custom Log Formatters

```python
# Configure custom JSON formatting
from metaexpert.logger.formatter import MainFormatter

# Create a custom formatter
class CustomFormatter(MainFormatter):
    def __init__(self):
        super().__init__(include_extra=True, timestamp_format="iso")
        
    def format(self, record):
        # Add custom fields to all log entries
        if not hasattr(record, 'application'):
            record.application = 'MetaExpert'
        if not hasattr(record, 'version'):
            record.version = '1.0.0'
        return super().format(record)

# Use the custom formatter
formatter = CustomFormatter()
```

## Asynchronous Logging

The enhanced logger supports asynchronous logging to prevent blocking of trading operations:

```python
# Asynchronous logging is enabled by default when async_logging=True
expert = MetaExpert(
    exchange="binance",
    # ... other parameters
    async_logging=True,  # Enable asynchronous logging
)

# High-frequency logging won't block trading operations
for i in range(1000):
    expert.logger.debug(f"Market data update {i}", extra={"price": 45000.0 + i})
```

## Error Handling and Exception Logging

```python
# Comprehensive error logging with context
try:
    # Trading operation that might fail
    order_result = expert.client.place_order(
        symbol="BTCUSDT",
        side="BUY",
        quantity=0.1,
        price=45000.0
    )
except Exception as e:
    # Log the error with full context
    expert.logger.log_error(
        "Order placement failed",
        exception=e,
        context={
            "symbol": "BTCUSDT",
            "side": "BUY",
            "quantity": 0.1,
            "price": 45000.0,
            "attempt": 1
        }
    )
```

## Log Rotation and Retention

```python
# Configure log rotation and retention
expert = MetaExpert(
    exchange="binance",
    # ... other parameters
    log_max_file_size=10485760,  # 10MB per log file
    log_backup_count=5,          # Keep 5 backup files
    log_retention_days=90,      # Keep logs for 90 days
)
```

## Performance Optimization

### 1. Buffering Configuration

```python
# Optimize logging for high-performance scenarios
expert = MetaExpert(
    exchange="binance",
    # ... other parameters
    log_buffer_size=1000,       # Buffer up to 1000 log entries
    log_async_queue_size=10000,  # Queue up to 10000 async log entries
    log_batch_size=100,         # Process logs in batches of 100
)
```

### 2. Log Level Filtering

```python
# Configure different log levels for different destinations
expert = MetaExpert(
    exchange="binance",
    # ... other parameters
    log_level="INFO",           # Overall log level
    console_log_level="WARNING", # Only warnings/errors to console
    file_log_level="DEBUG",     # All messages to file
)
```

## Remote Log Transmission

```python
# Configure remote log destinations
expert = MetaExpert(
    exchange="binance",
    # ... other parameters
    remote_log_destinations=[
        {
            "url": "https://logs.example.com/api/logs",
            "auth_token": "your_auth_token",
            "format": "json",
            "tls_enabled": True,
            "compression_enabled": True
        }
    ]
)
```

## Best Practices

### 1. Use Structured Logging

Always use structured logging for better searchability and analysis:

```python
# Good: Structured logging with context
logger.info("Order executed", extra={
    "order_id": "12345",
    "symbol": "BTCUSDT",
    "side": "BUY",
    "quantity": 0.1,
    "price": 45000.0,
    "commission": 4.5
})

# Avoid: Unstructured logging
logger.info("Order 12345 for BTCUSDT BUY 0.1 at 45000.0 executed with 4.5 commission")
```

### 2. Log at Appropriate Levels

```python
# DEBUG: Detailed diagnostic information
logger.debug("Entering strategy calculation", extra={"indicators": ["RSI", "MACD"]})

# INFO: General operational information
logger.info("Strategy started", extra={"strategy": "MovingAverageCross"})

# WARNING: Potentially harmful situations
logger.warning("High volatility detected", extra={"volatility": 0.05})

# ERROR: Error events that might still allow the application to continue
logger.error("Order placement failed", extra={"reason": "Insufficient funds"})

# CRITICAL: Critical events that might cause the application to stop
logger.critical("Exchange connection lost", extra={"exchange": "Binance"})
```

### 3. Protect Sensitive Information

```python
# Avoid logging sensitive information
# DON'T DO THIS:
logger.info("API credentials", extra={
    "api_key": "actual_api_key_here",  # DON'T DO THIS
    "api_secret": "actual_api_secret_here"  # DON'T DO THIS
})

# DO THIS instead:
logger.info("API connection established", extra={
    "exchange": "Binance",
    "connection_id": "conn_12345"  # Safe identifier
})
```

## Troubleshooting

### Common Issues

1. **Logs not appearing**: Check log level configuration and ensure the logger is properly configured
2. **Performance issues**: Consider disabling async_logging for debugging or reducing log volume
3. **Disk space issues**: Configure appropriate log rotation and retention policies
4. **Network errors**: Check remote destination configuration and network connectivity

### Diagnostic Steps

```python
# Enable debug logging to diagnose issues
import logging
logging.basicConfig(level=logging.DEBUG)

# Check logger configuration
logger = get_logger(__name__)
logger.debug("Logger configuration check")
```

## Next Steps

1. Explore the full API documentation
2. Review advanced configuration options
3. Implement custom log processors for specialized requirements
4. Set up log aggregation and analysis tools for production monitoring

Refer to the complete MetaExpert documentation for detailed API references and advanced usage examples.