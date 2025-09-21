# Updated Quickstart: MetaExpert Library Template Enhancement

## Purpose
This document provides a quickstart guide for developers who want to use the MetaExpert library template to create trading strategies with the enhanced configuration system.

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

### 2. Configure Environment Variables
Copy the `.env.example` file to `.env` and configure your exchange API credentials:

```bash
cp .env.example .env
```

Edit the `.env` file to set your exchange and API credentials:

```env
# Binance
BINANCE_API_KEY="your_api_key"
BINANCE_API_SECRET="your_api_secret"

# Bybit
BYBIT_API_KEY="your_api_key"
BYBIT_API_SECRET="your_api_secret"

# OKX
OKX_API_KEY="your_api_key"
OKX_API_SECRET="your_api_secret"
OKX_API_PASSPHRASE="your_api_passphrase"

# ... configure other exchanges as needed
```

### 3. Configure Exchange Settings
You can configure exchange settings through environment variables, command-line arguments, or by editing the template.py file directly.

Using environment variables (recommended):
```env
DEFAULT_EXCHANGE="binance"
DEFAULT_MARKET_TYPE="futures"
DEFAULT_CONTRACT_TYPE="linear"
```

Using command-line arguments:
```bash
metaexpert new my_trading_strategy --exchange binance --market-type futures --contract-type linear
```

Editing the template.py file:
```python
expert = MetaExpert(
    exchange="binance",             # Supported: 'binance', 'bybit', 'okx', 'bitget', 'kucoin'
    api_key=None,                   # User to provide API key
    api_secret=None,                # User to provide secret key
    api_passphrase=None,            # Required only for OKX/KuCoin
    # ... other configuration options
)
```

### 4. Configure Strategy Parameters
Modify the strategy-specific parameters in the on_init decorator:

```python
@expert.on_init(
    symbol="BTCUSDT",               # Trading symbols (str or set[str]: "BTCUSDT" or {"BTCUSDT", "ETHUSDT"})
    timeframe="1h",                 # Primary timeframe: '1m','5m','15m','1h','4h','1d',...
    lookback_bars=100,              # Number of historical bars to fetch for analysis
    strategy_id=1001,               # Unique ID for order tagging
    strategy_name="My Strategy",    # Display name
    leverage=10,                    # Leverage (verify per-symbol limits)
    # ... other strategy parameters
)
def init() -> None:
    """Called once at expert startup. Initialize indicators or load data here."""
    pass
```

### 5. Implement Trading Logic
Add your trading logic to the appropriate event handlers:

```python
@expert.on_bar
def bar(rates) -> None:
    """Called when a new bar closes. Implement core strategy logic here."""
    # Add your trading logic here
    pass
```

### 6. Run Your Strategy
```bash
python template.py
```

Or with command-line arguments:
```bash
python template.py --mode paper --symbol ETHUSDT --timeframe 5m
```

## Configuration Options

### Exchange Connection
- exchange: Supported exchanges (binance, bybit, okx, bitget, kucoin)
- api_key, api_secret, api_passphrase: Your exchange API credentials
- testnet: Set to True to use exchange testnet
- subaccount: For exchanges that support subaccounts

### Market Settings
- market_type: spot, futures, or options
- contract_type: linear (USDT-M) or inverse (COIN-M) for futures
- margin_mode: isolated or cross for futures
- position_mode: hedge (two-way) or oneway (one-way) for futures

### Risk Management
- leverage: Leverage to use for positions
- max_drawdown_pct: Maximum drawdown percentage
- size_type, size_value: Position sizing method and value
- stop_loss_pct, take_profit_pct: Risk management parameters

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

### Configuration Issues
If you're having trouble with configuration, check that:
1. Environment variables are properly set in your `.env` file
2. Command-line arguments are correctly formatted
3. Template parameters match the expected values