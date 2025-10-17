# Quickstart Guide: Comprehensive Logging System

## Overview
This guide will help you quickly set up and use the comprehensive logging system in MetaExpert.

## Basic Setup

### 1. Initialize the Logger
The logger is automatically initialized when you create a MetaExpert instance:

```python
from metaexpert import MetaExpert

expert = MetaExpert(
    exchange="binance",
    log_level="INFO",
    log_file="expert.log",
    trade_log_file="trades.log",
    error_log_file="errors.log",
    log_to_console=True,
    structured_logging=False,
    async_logging=True,
)
```

### 2. Using the Logger in Your Strategy
Access the logger through the expert instance:

```python
@expert.on_bar
def my_strategy(rates):
    expert.logger.info("New bar received", open=rates.open, close=rates.close)
    
    if some_condition:
        expert.logger.warning("High volatility detected", volatility=0.5)

# Log a trade-specific event
trade_logger = expert.logger.bind(category="trade")
trade_logger.info("Position opened", side="BUY", size=0.1, price=70000.0)
```

## Configuration Options

### Log Levels
- `DEBUG`: Detailed information for debugging
- `INFO`: Key lifecycle events
- `WARNING`: Non-critical issues
- `ERROR`: Operational errors
- `CRITICAL`: System-critical errors

### File Configuration
By default, three log files are created:
- `expert.log` - General events
- `trades.log` - Trade-specific events (in JSON Lines format)
- `errors.log` - Errors only

### Contextual Information
The system automatically adds contextual information to log entries, including:
- expert_name
- symbol
- trade_id
- order_id
- strategy_id
- account_id

## Advanced Usage

### Contextual Logging
Add custom context to your log entries:

```python
# Add context to all subsequent log entries
log = expert.logger.bind(strategy="ema_strategy", symbol="BTCUSDT")

# All logs from 'log' will now include this context
log.info("Executing trade", trade_id="12345")
```

### Structured Logging
Enable structured (JSON) logging for external log analysis:

```python
expert = MetaExpert(
    exchange="binance",
    structured_logging=True,  # Enables JSON format
)
```

## Asynchronous Logging
Enable async logging to ensure logging operations don't block trading:

```python
expert = MetaExpert(
    exchange="binance",
    async_logging=True,  # Enables non-blocking logging
)
```