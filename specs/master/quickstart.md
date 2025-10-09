# Quickstart Guide: MetaExpert Trading Library

## Overview
This guide will help you get started with the MetaExpert Trading Library, a unified interface for cryptocurrency trading across multiple exchanges with support for various trading types and comprehensive risk management.

## Prerequisites
- Python 3.12 or higher
- pip or uv package manager
- API credentials for your target exchange (Binance, Bybit, OKX, etc.)

## Installation

### Using UV (Recommended)
```bash
# Install UV if you don't have it
pip install uv

# Create and activate virtual environment
uv venv
source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate

# Install MetaExpert
uv pip install -e .
```

### Using pip
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate

# Install MetaExpert
pip install -e .
```

## Basic Usage

### 1. Creating Your First Trading Expert

```python
from metaexpert import MetaExpert

# Create a MetaExpert instance
expert = MetaExpert(
    exchange="binance",           # Supported: 'binance', 'bybit', 'okx', 'bitget', 'kucoin',...
    api_key="your_api_key",      # Your API key
    api_secret="your_secret",    # Your secret key
    api_passphrase="pass",       # Required only for OKX/KuCoin
    market_type="futures",       # 'spot', 'futures', 'options'
    contract_type="linear",      # Only for futures: 'linear' (USDT-M) or 'inverse' (COIN-M)
    margin_mode="isolated",      # Only for futures: 'isolated' or 'cross'
    position_mode="hedge",       # 'hedge' (two-way) or 'oneway' (one-way)
    log_level="INFO",            # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    log_file="expert.log",       # Main log file
    trade_log_file="trades.log", # Trade execution log
    error_log_file="errors.log", # Error-specific log
    log_to_console=True,         # Print logs to console
    structured_logging=False,    # Use structured JSON logging
    async_logging=True,          # Use asynchronous logging
)
```

### 2. Configuring Your Strategy

```python
@expert.on_init(
    symbol="BTCUSDT",              # Trading symbol
    timeframe="1h",                # Primary timeframe
    lookback_bars=100,             # Number of historical bars to fetch
    strategy_id=1001,              # Unique ID for order tagging
    strategy_name="My Strategy",   # Display name
    leverage=10,                   # Leverage to use
    max_drawdown_pct=0.2,          # Max drawdown from peak equity (20%)
    size_type="risk_based",        # Position sizing: 'fixed_base', 'fixed_quote', 'percent_equity', 'risk_based'
    size_value=1.5,                # Size value: 1.5% risk per trade
    stop_loss_pct=2.0,             # Stop-Loss % from entry
    take_profit_pct=4.0,           # Take-Profit % from entry
    trailing_stop_pct=1.0,         # Trailing stop distance %
)
def init() -> None:
    """Called once at expert startup. Initialize indicators or load data here."""
    print(f"Strategy {expert.strategy_name} initialized on {expert.symbol}")
```

### 3. Implementing Trading Logic

```python
@expert.on_bar(timeframe="1h")
def bar(rates) -> None:
    """Called when a new bar closes. Implement core strategy logic here."""
    # Example: Simple moving average crossover strategy
    current_price = rates['close'][-1]
    # Add your trading logic here
    print(f"New bar for {expert.symbol} at {current_price}")

@expert.on_order
def order(ord) -> None:
    """Called when order status changes."""
    print(f"Order status changed: {ord}")

@expert.on_position
def position(pos) -> None:
    """Called when position state changes."""
    print(f"Position changed: {pos}")
```

### 4. Running Your Expert

```python
def main() -> None:
    """Main entry point. Starts the trading expert."""
    expert.run(
        trade_mode="paper",         # 'paper', 'live' or 'backtest'
        backtest_start="2024-01-01",# 'YYYY-MM-DD' - for backtesting
        backtest_end="2024-12-31",  # 'YYYY-MM-DD' - for backtesting
        initial_capital=10000,      # Starting capital in settlement_currency
    )

if __name__ == "__main__":
    main()
```

## Multiple Trading Modes

### Paper Trading (Simulated)
```python
expert.run(trade_mode="paper")  # Simulates trades without real money
```

### Live Trading
```python
expert.run(trade_mode="live")   # Executes real trades with real money
```

### Backtesting
```python
expert.run(
    trade_mode="backtest",
    backtest_start="2024-01-01",
    backtest_end="2024-12-31",
    initial_capital=10000
)
```

## Risk Management Features

MetaExpert includes comprehensive risk management:

- **Stop-Loss**: Automatically close positions at a specified loss level
- **Take-Profit**: Automatically close positions at a specified profit level
- **Trailing Stops**: Dynamic stop-loss that follows price in your favor
- **Position Sizing**: Various methods to determine position size
- **Drawdown Limits**: Prevent losses beyond specified percentage
- **Daily Loss Limits**: Stop trading for the day after specified loss

## Supported Exchanges

- Binance (spot, futures)
- Bybit (spot, futures)
- OKX (spot, futures, options)
- Bitget (spot, futures)
- KuCoin (spot, futures)

## Advanced Features

### Event Handlers
The library provides various event handlers for different market conditions:

- `on_tick`: Called on every price tick (for HFT)
- `on_bar`: Called when a new bar closes
- `on_timer`: Called periodically for monitoring
- `on_order`: Called when order status changes
- `on_position`: Called when position state changes
- `on_transaction`: Called when a transaction completes
- `on_book`: Called when order book changes
- `on_error`: Called on error conditions
- `on_account`: Called when account state updates

### Backtesting Handlers
- `on_backtest_init`: Called at the start of backtest
- `on_backtest_deinit`: Called at the end of backtest
- `on_backtest`: Called for each bar during backtest
- `on_backtest_pass`: Called at the end of each optimization pass

## Configuration Options

### Exchange Connection
- `exchange`: Target exchange (binance, bybit, okx, etc.)
- `api_key`: API key for authentication
- `api_secret`: API secret for authentication
- `api_passphrase`: Required for some exchanges
- `testnet`: Use testnet instead of live API

### Trading Parameters
- `market_type`: 'spot', 'futures', or 'options'
- `contract_type`: 'linear' or 'inverse' for futures
- `margin_mode`: 'isolated' or 'cross' for futures
- `position_mode`: 'hedge' or 'oneway' for futures

### Risk Management
- `leverage`: Trading leverage to use
- `max_drawdown_pct`: Maximum allowed drawdown percentage
- `daily_loss_limit`: Daily loss limit in quote currency
- `stop_loss_pct`: Stop-loss percentage from entry
- `take_profit_pct`: Take-profit percentage from entry

### Logging
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `structured_logging`: Enable JSON structured logging
- `async_logging`: Enable asynchronous logging for performance

## Best Practices

1. **Start with Paper Trading**: Always test your strategies with paper trading before going live.

2. **Implement Risk Management**: Use stop-losses and position sizing to protect your capital.

3. **Monitor Logs**: Regularly check logs to ensure your strategies are behaving as expected.

4. **Backtest Thoroughly**: Test your strategies on historical data before live deployment.

5. **Use Appropriate Timeframes**: Match your strategy to appropriate timeframes for your trading style.

6. **Secure Your API Keys**: Never share your API credentials and use appropriate API permissions.

## Troubleshooting

### Common Issues

- **API Rate Limits**: The system handles rate limiting automatically, but you can configure rate limits with the `rate_limit` parameter.
- **Connection Issues**: Check your API credentials and network connectivity.
- **Insufficient Balance**: Ensure your account has sufficient balance for the desired position size.
- **Exchange-Specific Limits**: Different exchanges may have different limits for leverage, position sizes, etc.

### Error Handling

The MetaExpert library provides comprehensive error handling:

- Network errors are automatically retried with exponential backoff
- Critical operations are queued when exchanges are unavailable
- Non-critical operations are dropped when rate limits are reached

## Next Steps

- Review the examples directory for more complete strategy implementations
- Check the API documentation for detailed parameter information
- Explore the configuration options for advanced features
- Consider compliance requirements in your jurisdiction