# MetaExpert Template System

## Overview

The MetaExpert template system provides a robust foundation for creating trading strategies. The template (`template.py`) serves as the starting point for all trading strategies, preserving all core functionality while allowing for strategy-specific customization.

## Template Structure

The template file is organized into several key sections:

### 1. Expert Core Configuration

This section defines the global behavior and connection of your expert:

```python
expert = MetaExpert(
    # Required Parameters
    exchange="binance",             # Supported: 'binance', 'bybit', 'okx', 'bitget', 'kucoin'
    
    # API Credentials
    api_key=None,                   # User to provide API key
    api_secret=None,                # User to provide secret key
    api_passphrase=None,            # Required only for OKX/KuCoin
    
    # Connection Settings
    subaccount=None,                # For Bybit multi-account
    base_url=None,                  # Custom API URL
    testnet=False,                  # True to use exchange testnet
    proxy=None,                     # Proxy settings
    
    # Market & Trading Mode
    market_type="futures",          # 'spot', 'futures', 'options'
    contract_type="linear",         # 'linear' (USDT-M) or 'inverse' (COIN-M)
    margin_mode="isolated",         # 'isolated' or 'cross'
    position_mode="hedge",          # 'hedge' or 'oneway'
    
    # Logging Configuration
    log_level="INFO",               # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    log_file="expert.log",          # Main log file
    trade_log_file="trades.log",    # Trade execution log
    error_log_file="errors.log",    # Error-specific log
    log_to_console=True,            # Print logs to console
    
    # Advanced System Settings
    rate_limit=1200,                # Max requests per minute
    enable_metrics=True,            # Enable performance metrics
    persist_state=True,             # Persist state between runs
    state_file="state.json"         # State persistence file
)
```

### 2. Strategy Initialization

This section defines the unique parameters of your trading strategy:

```python
@expert.on_init(
    # Core Trading Parameters
    symbol="BTCUSDT",               # Trading symbols
    timeframe="1h",                 # Primary timeframe
    lookback_bars=100,              # Historical bars for analysis
    warmup_bars=0,                  # Skip initial bars for indicator initialization
    
    # Strategy Metadata
    strategy_id=1001,               # Unique ID for order tagging
    strategy_name="My Strategy",    # Display name
    comment="my_strategy",          # Order comment
    
    # Risk & Position Sizing
    leverage=10,                    # Leverage
    max_drawdown_pct=0.2,           # Max drawdown from peak equity
    daily_loss_limit=1000.0,        # Daily loss limit
    size_type="risk_based",         # Position sizing method
    size_value=1.5,                 # Size value
    max_position_size_quote=50000.0,# Max position size
    
    # Trade Parameters
    stop_loss_pct=2.0,              # Stop-Loss %
    take_profit_pct=4.0,            # Take-Profit %
    trailing_stop_pct=1.0,          # Trailing stop distance %
    trailing_activation_pct=2.0,    # Activate after X% profit
    breakeven_pct=1.5,              # Move SL to breakeven after X% profit
    slippage_pct=0.1,               # Expected slippage %
    max_spread_pct=0.1,             # Max allowed spread %
    
    # Portfolio Management
    max_open_positions=3,           # Max total open positions
    max_positions_per_symbol=1,     # Max positions per symbol
    
    # Entry Filters
    trade_hours={9, 10, 11, 15},    # Trade only during these UTC hours
    allowed_days={1, 2, 3, 4, 5},   # Trade only these days
    min_volume=1000000,             # Min volume in settlement_currency
    volatility_filter=True,         # Enable volatility filter
    trend_filter=True,              # Enable trend filter
)
def init() -> None:
    """Called once at expert startup. Initialize indicators or load data here."""
    pass
```

### 3. Event Handlers

This section contains the core of your trading logic:

```python
# Expert Lifecycle Events
@expert.on_deinit
def deinit(reason) -> None:
    """Called when expert stops. Clean up resources if needed."""
    pass

# Market Data Events
@expert.on_tick
def tick(rates) -> None:
    """Called on every price tick. Use for HFT, real-time adjustments."""
    pass

@expert.on_bar(timeframe="1h")
def bar(rates) -> None:
    """Called when a new bar closes. Implement core strategy logic here."""
    pass

# Timer Events
@expert.on_timer(interval=60)
def timer() -> None:
    """Called periodically. Useful for monitoring, heartbeat, non-market logic."""
    pass

# Trading Events
@expert.on_order
def order(order) -> None:
    """Called when order status changes."""
    pass

@expert.on_position
def position(pos) -> None:
    """Called when position state changes. Ideal for dynamic risk management."""
    pass

@expert.on_transaction
def transaction(request, result) -> None:
    """Called when a transaction completes (e.g., order fill)."""
    pass

# Market Depth Events
@expert.on_book
def book(orderbook) -> None:
    """Called when order book changes. Useful for market making or liquidity analysis."""
    pass

# System Events
@expert.on_error
def error(err) -> None:
    """Called on error (API, network, logic). Implement recovery or alerting here."""
    pass

@expert.on_account
def account(acc) -> None:
    """Called when account state updates (balance, equity, margin)."""
    pass

# Backtesting Events
@expert.on_backtest_init
def backtest_init() -> None:
    """Called once at the start of a backtest run."""
    pass

@expert.on_backtest_deinit
def backtest_deinit() -> None:
    """Called once at the end of a backtest run."""
    pass

@expert.on_backtest
def backtest() -> float:
    """Called for each bar during a backtest."""
    ret: float = 0.0
    return ret

@expert.on_backtest_pass
def backtest_pass() -> None:
    """Called at the end of each pass in an optimization run."""
    pass
```

### 4. Entry Point

This section is responsible for launching the expert:

```python
def main() -> None:
    """Main entry point. Starts the trading expert."""
    expert.run(
        trade_mode="paper",         # 'paper' or 'live' or 'backtest'
        backtest_start="2024-01-01",# 'YYYY-MM-DD'
        backtest_end="2025-08-31",  # 'YYYY-MM-DD'
        initial_capital=10000,      # Starting capital
    )

if __name__ == "__main__":
    main()
```

## Creating New Templates

### Using the CLI

To create a new trading strategy template, use the `metaexpert` CLI:

```bash
# Create a new strategy template
metaexpert create my_strategy ./strategies

# Create a template with specific parameters
metaexpert create my_strategy ./strategies --exchange binance --symbol BTCUSDT --timeframe 1h

# List supported exchanges
metaexpert exchanges

# List configurable parameters
metaexpert parameters

# Validate configuration parameters
metaexpert validate exchange=binance symbol=BTCUSDT timeframe=1h
```

### Using the Python API

You can also create templates programmatically:

```python
from metaexpert.template.template_creator import create_expert_from_template

# Create a new expert file from template
create_expert_from_template("./strategies/my_strategy.py")

# Create a new expert with custom parameters
create_expert_from_template(
    "./strategies/my_strategy.py",
    parameters={
        "exchange": "binance",
        "symbol": "BTCUSDT",
        "timeframe": "1h"
    }
)
```

## Configuration System

The enhanced configuration system provides better alignment between environment variables, command-line arguments, and template parameters.

### Environment Variables

Environment variables provide a secure way to configure sensitive information:

```bash
# Exchange API credentials
BINANCE_API_KEY="your_api_key"
BINANCE_API_SECRET="your_api_secret"
BYBIT_API_KEY="your_api_key"
BYBIT_API_SECRET="your_api_secret"
OKX_API_KEY="your_api_key"
OKX_API_SECRET="your_api_secret"
OKX_API_PASSPHRASE="your_api_passphrase"

# Core configuration
DEFAULT_EXCHANGE="binance"
DEFAULT_SYMBOL="BTCUSDT"
DEFAULT_TIMEFRAME="1h"
```

### Command-Line Arguments

Command-line arguments provide a flexible way to configure your expert:

```bash
# Configure exchange settings
metaexpert --exchange binance --market-type futures --contract-type linear

# Configure trading parameters
metaexpert --symbol ETHUSDT --timeframe 5m --leverage 10

# Configure risk management
metaexpert --stop-loss 2.0 --take-profit 4.0 --max-drawdown 0.2
```

## Best Practices

1. **Preserve Core Structure**: Do not modify the core structure of the template file. Only add your strategy-specific code in the designated areas.

2. **Secure API Credentials**: Never commit your API credentials to version control. Use environment variables or a separate configuration file.

3. **Implement Error Handling**: Implement proper error handling in your event handlers to prevent the strategy from crashing.

4. **Test Thoroughly**: Test your strategy in paper trading mode before running it live.

5. **Monitor Performance**: Use the built-in metrics and logging to monitor your strategy's performance.
