# Quickstart Guide: MetaExpert Crypto Trading Library

## Overview

This guide will help you get started with the MetaExpert cryptocurrency trading library. The library provides a unified interface for trading across multiple exchanges with support for various trading types and risk management features.

## Prerequisites

- Python 3.12 or higher
- API keys for the exchanges you want to connect to
- Understanding of cryptocurrency trading concepts

## Installation

```bash
# Activate your virtual environment
.venv/Scripts/activate

# Install the MetaExpert library using uv
uv add metaexpert
```

Or add it to your project:

```bash
uv add metaexpert
```

## Basic Usage

### 1. Import the Library

```python
from metaexpert.core.trading_service import TradingService
from metaexpert.exchanges.binance import BinanceExchange
from metaexpert.exchanges.bybit import BybitExchange
```

### 2. Initialize the Trading Service

```python
# Initialize the trading service
trading_service = TradingService()

# Add exchange connections with your API keys
binance = BinanceExchange(
    api_key="your_binance_api_key",
    api_secret="your_binance_api_secret"
)
bybit = BybitExchange(
    api_key="your_bybit_api_key",
    api_secret="your_bybit_api_secret"
)

# Register exchanges with the trading service
trading_service.register_exchange(binance)
trading_service.register_exchange(bybit)
```

### 3. View Available Instruments

```python
# Get all available trading instruments
instruments = trading_service.get_instruments()

# Get instruments for a specific exchange
binance_instruments = trading_service.get_instruments(exchange_id="binance")

# Get instruments for specific trading type
spot_instruments = trading_service.get_instruments(trading_type="spot")
```

### 4. Place an Order

```python
# Place a market order
order = trading_service.place_market_order(
    symbol="BTCUSDT",
    side="buy",
    quantity=0.001,
    trading_account_id="my_account_1"
)

# Place a limit order
order = trading_service.place_limit_order(
    symbol="BTCUSDT",
    side="buy",
    quantity=0.001,
    price=45000.00,
    trading_account_id="my_account_1"
)

# Place an order with risk management
order = trading_service.place_limit_order(
    symbol="BTCUSDT",
    side="buy",
    quantity=0.001,
    price=45000.00,
    stop_loss_price=43000.00,
    take_profit_price=48000.00,
    trailing_stop_callback_rate=0.02,  # 2% trailing stop
    trading_account_id="my_account_1"
)
```

### 5. Check Positions

```python
# Get all open positions
positions = trading_service.get_positions()

# Get positions for a specific account
account_positions = trading_service.get_positions(account_id="my_account_1")
```

### 6. Cancel Orders

```python
# Cancel a specific order
trading_service.cancel_order(order_id="order_12345")
```

## Advanced Features

### Multi-Exchange Trading

```python
# Execute the same strategy across multiple exchanges
for exchange_id in ["binance", "bybit"]:
    trading_service.place_market_order(
        symbol="BTCUSDT",
        side="buy",
        quantity=0.001,
        trading_account_id=f"{exchange_id}_account"
    )
```

### Switching Trading Modes

```python
# The library supports backtesting, paper trading, and live trading
# with minimal code changes:

# For live trading
trading_service.set_mode("live")

# For paper trading
trading_service.set_mode("paper")

# For backtesting
trading_service.set_mode("backtest")
```

### Risk Management

```python
# Set up risk management parameters
risk_manager = trading_service.get_risk_manager()

# Set maximum position size
risk_manager.set_max_position_size("BTCUSDT", 0.1)

# Set maximum drawdown
risk_manager.set_max_drawdown(0.1)  # 10%

# Enable automatic stop-loss for all positions
risk_manager.set_auto_stop_loss(True)
```

## Handling Market Data

```python
# Get current market data for a symbol
ticker = trading_service.get_ticker("BTCUSDT")

# Get historical market data
klines = trading_service.get_klines(
    symbol="BTCUSDT",
    interval="1h",
    limit=100
)

# Subscribe to real-time market data
def on_market_data(data):
    print(f"Price update: {data['symbol']} = {data['price']}")

trading_service.subscribe_market_data("BTCUSDT", on_market_data)
```

## Error Handling

```python
from metaexpert.core.exceptions import TradingError, AuthenticationError, RateLimitError

try:
    order = trading_service.place_market_order(
        symbol="BTCUSDT",
        side="buy",
        quantity=0.001,
        trading_account_id="my_account_1"
    )
except AuthenticationError:
    print("Invalid API credentials")
except RateLimitError:
    print("Rate limit exceeded, retrying...")
except TradingError as e:
    print(f"Trading error: {e}")
```

## Cleanup

```python
# Properly close connections when done
trading_service.close()
```

## Configuration

You can configure the library using environment variables:

```bash
# Set API keys in environment variables
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_API_SECRET="your_binance_api_secret"
export BYBIT_API_KEY="your_bybit_api_key"
export BYBIT_API_SECRET="your_bybit_api_secret"

# Set data retention policy (minimum 3 years default)
export DATA_RETENTION_YEARS=5
```

## Performance Considerations

The library is designed to handle high-volume trading (1000+ trades per second). For optimal performance:

- Use the asynchronous API where available
- Implement proper connection pooling
- Monitor and handle rate limits appropriately
- Use the built-in observability features to track performance

## Next Steps

- Review the detailed API documentation
- Explore the examples directory for complete trading strategies
- Set up observability and monitoring for your trading activities