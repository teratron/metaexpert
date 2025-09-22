# MetaExpert Configuration System

## Overview

The MetaExpert configuration system provides a comprehensive and flexible way to configure your trading strategies. The system ensures alignment between environment variables, command-line arguments, and template parameters.

## Configuration Sources

The configuration system supports multiple sources with the following priority (highest to lowest):

1. **Command-Line Arguments** - Highest priority
2. **Environment Variables** - Medium priority
3. **Template Parameters** - Lowest priority (default values)

## Core Configuration Parameters

### Exchange Configuration

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| exchange | DEFAULT_EXCHANGE | --exchange | binance | Supported exchange |
| api_key | API_KEY | --api-key | "" | API key for authentication |
| api_secret | API_SECRET | --api-secret | "" | API secret for authentication |
| api_passphrase | API_PASSPHRASE | --api-passphrase | "" | API passphrase (OKX/KuCoin) |

### Exchange-Specific Configuration

#### Binance

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| binance_api_key | BINANCE_API_KEY | --binance-api-key | "" | Binance API key |
| binance_api_secret | BINANCE_API_SECRET | --binance-api-secret | "" | Binance API secret |

#### Bybit

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| bybit_api_key | BYBIT_API_KEY | --bybit-api-key | "" | Bybit API key |
| bybit_api_secret | BYBIT_API_SECRET | --bybit-api-secret | "" | Bybit API secret |

#### OKX

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| okx_api_key | OKX_API_KEY | --okx-api-key | "" | OKX API key |
| okx_api_secret | OKX_API_SECRET | --okx-api-secret | "" | OKX API secret |
| okx_api_passphrase | OKX_API_PASSPHRASE | --okx-api-passphrase | "" | OKX API passphrase |

#### Bitget

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| bitget_api_key | BITGET_API_KEY | --bitget-api-key | "" | Bitget API key |
| bitget_api_secret | BITGET_API_SECRET | --bitget-api-secret | "" | Bitget API secret |

#### KuCoin

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| kucoin_api_key | KUCOIN_API_KEY | --kucoin-api-key | "" | KuCoin API key |
| kucoin_api_secret | KUCOIN_API_SECRET | --kucoin-api-secret | "" | KuCoin API secret |
| kucoin_api_passphrase | KUCOIN_API_PASSPHRASE | --kucoin-api-passphrase | "" | KuCoin API passphrase |

### Market Configuration

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| market_type | MARKET_TYPE | --market-type | futures | Market type (spot, futures, options) |
| contract_type | CONTRACT_TYPE | --contract-type | linear | Contract type (linear, inverse) |
| margin_mode | MARGIN_MODE | --margin-mode | isolated | Margin mode (isolated, cross) |
| position_mode | POSITION_MODE | --position-mode | hedge | Position mode (hedge, oneway) |

### Trading Configuration

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| symbol | DEFAULT_SYMBOL | --symbol | BTCUSDT | Trading pair symbol |
| timeframe | DEFAULT_TIMEFRAME | --timeframe | 1h | Trading timeframe |
| lookback_bars | LOOKBACK_BARS | --lookback-bars | 100 | Historical bars for analysis |
| warmup_bars | WARMUP_BARS | --warmup-bars | 0 | Warmup bars for indicators |

### Strategy Metadata

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| strategy_id | STRATEGY_ID | --strategy-id | 1001 | Unique strategy ID |
| strategy_name | STRATEGY_NAME | --strategy-name | "My Strategy" | Strategy name |
| comment | COMMENT | --comment | "my_strategy" | Order comment |

### Risk Management

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| leverage | LEVERAGE | --leverage | 10 | Leverage |
| max_drawdown_pct | MAX_DRAWDOWN_PCT | --max-drawdown-pct | 0.2 | Max drawdown percentage |
| daily_loss_limit | DAILY_LOSS_LIMIT | --daily-loss-limit | 1000.0 | Daily loss limit |
| size_type | SIZE_TYPE | --size-type | "risk_based" | Position sizing method |
| size_value | SIZE_VALUE | --size-value | 1.5 | Position sizing value |
| max_position_size_quote | MAX_POSITION_SIZE_QUOTE | --max-position-size-quote | 50000.0 | Max position size |
| stop_loss_pct | STOP_LOSS_PCT | --stop-loss-pct | 2.0 | Stop loss percentage |
| take_profit_pct | TAKE_PROFIT_PCT | --take-profit-pct | 4.0 | Take profit percentage |
| trailing_stop_pct | TRAILING_STOP_PCT | --trailing-stop-pct | 1.0 | Trailing stop percentage |
| trailing_activation_pct | TRAILING_ACTIVATION_PCT | --trailing-activation-pct | 2.0 | Trailing activation percentage |
| breakeven_pct | BREAKEVEN_PCT | --breakeven-pct | 1.5 | Breakeven percentage |
| slippage_pct | SLIPPAGE_PCT | --slippage-pct | 0.1 | Slippage percentage |
| max_spread_pct | MAX_SPREAD_PCT | --max-spread-pct | 0.1 | Max spread percentage |

### Portfolio Management

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| max_open_positions | MAX_OPEN_POSITIONS | --max-open-positions | 3 | Max open positions |
| max_positions_per_symbol | MAX_POSITIONS_PER_SYMBOL | --max-positions-per-symbol | 1 | Max positions per symbol |

### Entry Filters

| Parameter | Environment Variable | CLI Argument | Default | Description |
|-----------|---------------------|--------------|---------|-------------|
| trade_hours | TRADE_HOURS | --trade-hours | {9, 10, 11, 15} | Trade hours (UTC) |
| allowed_days | ALLOWED_DAYS | --allowed-days | {1, 2, 3, 4, 5} | Allowed days (1=Mon, 7=Sun) |
| min_volume | MIN_VOLUME | --min-volume | 1000000 | Min volume |
| volatility_filter | VOLATILITY_FILTER | --volatility-filter | True | Enable volatility filter |
| trend_filter | TREND_FILTER | --trend-filter | True | Enable trend filter |

## Using Environment Variables

Environment variables provide a secure way to configure sensitive information like API credentials:

```bash
# Create a .env file
cat > .env << EOF
# Exchange API credentials
BINANCE_API_KEY="your_binance_api_key"
BINANCE_API_SECRET="your_binance_api_secret"
BYBIT_API_KEY="your_bybit_api_key"
BYBIT_API_SECRET="your_bybit_api_secret"
OKX_API_KEY="your_okx_api_key"
OKX_API_SECRET="your_okx_api_secret"
OKX_API_PASSPHRASE="your_okx_api_passphrase"

# Core configuration
DEFAULT_EXCHANGE="binance"
DEFAULT_SYMBOL="BTCUSDT"
DEFAULT_TIMEFRAME="1h"
EOF

# Load environment variables
source .env
```

## Using Command-Line Arguments

Command-line arguments provide a flexible way to configure your expert:

```bash
# Configure exchange settings
metaexpert --exchange binance --market-type futures --contract-type linear

# Configure trading parameters
metaexpert --symbol ETHUSDT --timeframe 5m --leverage 10

# Configure risk management
metaexpert --stop-loss 2.0 --take-profit 4.0 --max-drawdown 0.2

# Configure portfolio management
metaexpert --max-open-positions 5 --max-positions-per-symbol 2
```

## Configuration Validation

The configuration system includes built-in validation to ensure your parameters are correct:

```python
from metaexpert.services.config_service import ConfigurationManagementService

# Create a configuration service
config_service = ConfigurationManagementService()

# Validate configuration
config = {
    "exchange": "binance",
    "symbol": "BTCUSDT",
    "timeframe": "1h"
}

result = config_service.validate_configuration(config)
if result["valid"]:
    print("Configuration is valid")
else:
    print("Configuration errors:")
    for error in result["errors"]:
        print(f"  - {error['parameter']}: {error['error']}")
```

## Best Practices

1. **Use Environment Variables for Sensitive Data**: Store API keys and secrets in environment variables, not in code.

2. **Validate Configuration**: Always validate your configuration before running your strategy.

3. **Use Default Values**: Provide sensible default values for non-sensitive parameters.

4. **Document Parameters**: Document all configuration parameters in your strategy documentation.

5. **Test Different Configurations**: Test your strategy with different configuration values to ensure robustness.