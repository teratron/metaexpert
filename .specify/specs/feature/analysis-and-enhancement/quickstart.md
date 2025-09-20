# Quickstart: MetaExpert Library Template Enhancement

## Purpose
This document provides a quickstart guide for developers who want to use the MetaExpert library template to create trading strategies.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- API credentials for at least one supported exchange

## Steps

### 1. Create a New Trading Strategy
```bash
metaexpert new my_trading_strategy
```

This command creates a new directory with the template.py file copied into it.

### 2. Configure Exchange Settings
Edit the template.py file to set your exchange and API credentials:

```python
expert = MetaExpert(
    exchange="binance",             # Change to your preferred exchange
    api_key="your_api_key",         # Add your API key
    api_secret="your_api_secret",   # Add your API secret
    # ... other configuration options
)
```

### 3. Configure Strategy Parameters
Modify the strategy-specific parameters in the on_init decorator:

```python
@expert.on_init(
    symbol="BTCUSDT",               # Trading pair
    timeframe="1h",                 # Timeframe for analysis
    # ... other strategy parameters
)
def init() -> None:
    """Initialize your strategy here."""
    pass
```

### 4. Implement Trading Logic
Add your trading logic to the appropriate event handlers:

```python
@expert.on_bar
def bar(rates) -> None:
    """Called when a new bar closes. Implement core strategy logic here."""
    # Add your trading logic here
    pass
```

### 5. Run Your Strategy
```bash
python template.py
```

## Testing Your Strategy
You can test your strategy in paper trading mode or backtest mode before going live:

```python
def main() -> None:
    expert.run(
        mode="paper",               # or "backtest" for backtesting
        # ... other options
    )
```

## Key Configuration Options

### Exchange Connection
- exchange: Supported exchanges (binance, bybit, okx, bitget, kucoin)
- api_key, api_secret: Your exchange API credentials
- testnet: Set to True to use exchange testnet

### Market Settings
- market_type: spot, futures, or options
- contract_type: linear (USDT-M) or inverse (COIN-M) for futures
- margin_mode: isolated or cross for futures

### Risk Management
- leverage: Leverage to use for positions
- max_drawdown_pct: Maximum drawdown percentage
- size_type, size_value: Position sizing method and value

### Event Handlers
Implement the event handlers you need for your strategy:
- on_tick: For real-time price updates
- on_bar: For completed bar notifications
- on_order: For order status changes
- on_position: For position changes
- etc.

## Common Customizations

### Adding Indicators
Initialize your indicators in the init() function:

```python
def init() -> None:
    # Initialize indicators here
    pass
```

### Strategy Logic
Implement your strategy logic in the bar() function:

```python
@expert.on_bar
def bar(rates) -> None:
    # Your strategy logic here
    pass
```

## Troubleshooting

### Template Structure
Do not modify the core structure of the template file. Only add your strategy-specific code in the designated areas.

### API Credentials
Never commit your API credentials to version control. Use environment variables or a separate configuration file.

### Error Handling
Implement proper error handling in your event handlers to prevent the strategy from crashing.