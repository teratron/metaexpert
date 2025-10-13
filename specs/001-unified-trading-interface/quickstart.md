# Quickstart Guide: Unified Trading Interface

**Feature**: MetaExpert Unified Trading Interface
**Date**: 2025-10-13

## Overview

This guide provides a quick introduction to using the MetaExpert Unified Trading Interface for cryptocurrency trading across multiple exchanges.

## Prerequisites

1. Python 3.12+
2. Install MetaExpert: `pip install metaexpert`
3. API credentials for desired exchanges (Binance, Bybit, OKX)
4. Environment variables for API keys (recommended)

## Setting Up the Environment

```bash
# Clone the repository
git clone https://github.com/teratron/metaexpert.git

# Navigate to the project directory
cd metaexpert

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

## Basic Usage Examples

### Connecting to an Exchange

```python
from metaexpert import MetaExpert
from metaexpert.core.events import BarEvent, TickEvent

# Initialize the trading system with Binance
expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    secret_key="your_secret_key",
    testnet=True  # Use testnet for development
)

@expert.on_init
def init():
    # Configure trading parameters
    expert.symbol = "BTCUSDT"
    expert.timeframe = "1m"
    expert.risk_params = {
        "max_position_size": 0.01,
        "stop_loss_pct": 0.02,  # 2%
        "take_profit_pct": 0.04, # 4%
    }

@expert.on_bar
def on_bar(bar):
    # Handle bar events
    print(f"Bar: {bar.timestamp} - O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close}")
    
    # Place a buy order if conditions are met
    if should_buy(bar):
        expert.buy(quantity=0.001, symbol="BTCUSDT")

@expert.on_tick
def on_tick(tick):
    # Handle tick events for high-frequency strategies
    print(f"Tick: {tick.symbol} - B:{tick.best_bid} A:{tick.best_ask}")

def should_buy(bar):
    # Example condition: price above 20-period moving average
    return bar.close > calculate_sma(bar, 20)

def calculate_sma(bar, period):
    # Placeholder for SMA calculation
    return bar.close  # Simplified

# Start the trading system
expert.run()
```

### Multi-Exchange Trading

```python
from metaexpert import MetaExpert

# Initialize experts for different exchanges
binance_expert = MetaExpert(
    exchange="binance",
    api_key="binance_api_key",
    secret_key="binance_secret_key",
    testnet=True
)

bybit_expert = MetaExpert(
    exchange="bybit",
    api_key="bybit_api_key",
    secret_key="bybit_secret_key",
    testnet=True
)

@binance_expert.on_init
@bybit_expert.on_init
def init():
    binance_expert.symbol = "BTCUSDT"
    bybit_expert.symbol = "BTCUSDT"
    
# Implement cross-exchange arbitrage strategy
@binance_expert.on_tick
@bybit_expert.on_tick
def on_tick(tick):
    # Compare prices across exchanges to find arbitrage opportunities
    if hasattr(binance_expert, 'last_tick') and hasattr(bybit_expert, 'last_tick'):
        binance_price = (binance_expert.last_tick.best_bid + binance_expert.last_tick.best_ask) / 2
        bybit_price = (bybit_expert.last_tick.best_bid + bybit_expert.last_tick.best_ask) / 2
        
        # If Binance price is significantly lower, consider buying on Binance and selling on Bybit
        if binance_price < bybit_price * 0.995:  # 0.5% spread + fees
            # Execute arbitrage trade (simplified example)
            binance_expert.buy(quantity=0.001, symbol="BTCUSDT")
            bybit_expert.sell(quantity=0.001, symbol="BTCUSDT")
    
    # Store tick for next comparison
    if tick.exchange_id == "binance":
        binance_expert.last_tick = tick
    elif tick.exchange_id == "bybit":
        bybit_expert.last_tick = tick
```

### Using Risk Management Features

```python
from metaexpert import MetaExpert

expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    secret_key="your_secret_key",
    testnet=True
)

@expert.on_init
def init():
    # Configure comprehensive risk management
    expert.risk_params = {
        "stop_loss_pct": 0.02,      # 2% stop loss
        "take_profit_pct": 0.04,    # 4% take profit
        "trailing_stop_pct": 0.015, # 1.5% trailing stop
        "max_position_size": 0.01,  # Max 0.01 BTC per position
        "max_daily_loss": 100.0,    # Max $100 daily loss
        "max_drawdown": 0.1,        # Max 10% drawdown
    }

@expert.on_bar
def on_bar(bar):
    # Implement strategy with risk management
    if should_enter_position(bar):
        # The risk management will automatically apply stop losses, etc.
        expert.buy(quantity=0.005, symbol="BTCUSDT")
```

### Paper Trading vs Live Trading

```python
from metaexpert import MetaExpert

# For paper trading/testing
paper_expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    secret_key="your_secret_key",
    mode="paper"  # Use paper trading mode
)

# For live trading
live_expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    secret_key="your_secret_key",
    mode="live"  # Use live trading mode (default)
)
```

## Data Models and Validation

All data entities in the system use Pydantic for validation and serialization:

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Example of a validated data model
class Order(BaseModel):
    order_id: str
    symbol: str
    side: str  # "buy" or "sell"
    quantity: float
    price: Optional[float] = None
    timestamp: datetime
    
    def validate(self):
        assert self.quantity > 0, "Quantity must be positive"
        if self.price is not None:
            assert self.price > 0, "Price must be positive"
```

## Error Handling

```python
from metaexpert import MetaExpert

expert = MetaExpert(
    exchange="binance",
    api_key="your_api_key",
    secret_key="your_secret_key",
    testnet=True
)

@expert.on_init
def init():
    expert.symbol = "BTCUSDT"

@expert.on_error
def on_error(error):
    print(f"Error occurred: {error}")
    # Implement error handling logic
    # e.g., send notifications, pause strategy, retry connection
```

## Running the System

```bash
# Run the trading system
python main.py

# For debugging
python -m debug main.py
```

## Configuration

Create a `.env` file in your project root:

```
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key
BYBIT_API_KEY=your_bybit_api_key
BYBIT_SECRET_KEY=your_bybit_secret_key
OKX_API_KEY=your_okx_api_key
OKX_SECRET_KEY=your_okx_secret_key
```

Then load the configuration in your code:

```python
import os
from dotenv import load_dotenv

load_dotenv()

expert = MetaExpert(
    exchange="binance",
    api_key=os.getenv("BINANCE_API_KEY"),
    secret_key=os.getenv("BINANCE_SECRET_KEY"),
    testnet=True
)
```

## Next Steps

1. Explore the examples directory for complete trading strategies
2. Review API documentation for detailed method references
3. Set up monitoring and alerting for your trading systems
4. Implement comprehensive testing for your strategies before going live