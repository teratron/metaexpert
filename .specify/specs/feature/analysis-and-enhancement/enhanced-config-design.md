# Enhanced Configuration System Design

## Current Issues

1. **Incomplete Exchange Support**: The config.py file only supports Binance and Bybit, while template.py supports Binance, Bybit, OKX, Bitget, and Kucoin.

2. **Configuration Mismatch**: The configuration system doesn't fully align with the parameters available in template.py, leading to potential confusion for users.

3. **Environment Variable Organization**: The .env.example file has a basic structure but could be better organized to match the template parameters.

4. **Missing Configuration Options**: Several important configuration options from template.py are not exposed through environment variables or command-line arguments.

## Proposed Improvements

### 1. Enhanced Environment Variable System

Update .env.example to include all supported exchanges and their relevant configuration options:

```env
# MetaExpert Configuration

# Logging Configuration
LOG_LEVEL="INFO"
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE="expert.log"
TRADE_LOG_FILE="trades.log"
ERROR_LOG_FILE="errors.log"
LOG_TO_CONSOLE=true
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# Binance
BINANCE_API_KEY=""
BINANCE_API_SECRET=""
BINANCE_API_PASSPHRASE=""  # For exchanges that require it
BINANCE_BASE_URL=""
BINANCE_SUBACCOUNT=""
BINANCE_TESTNET=false

# Bybit
BYBIT_API_KEY=""
BYBIT_API_SECRET=""
BYBIT_API_PASSPHRASE=""
BYBIT_BASE_URL=""
BYBIT_SUBACCOUNT=""
BYBIT_TESTNET=false

# OKX
OKX_API_KEY=""
OKX_API_SECRET=""
OKX_API_PASSPHRASE=""
OKX_BASE_URL=""
OKX_TESTNET=false

# Bitget
BITGET_API_KEY=""
BITGET_API_SECRET=""
BITGET_API_PASSPHRASE=""
BITGET_BASE_URL=""
BITGET_TESTNET=false

# Kucoin
KUCOIN_API_KEY=""
KUCOIN_API_SECRET=""
KUCOIN_API_PASSPHRASE=""
KUCOIN_BASE_URL=""
KUCOIN_TESTNET=false

# Default Configuration
DEFAULT_EXCHANGE="binance"
DEFAULT_MARKET_TYPE="futures"
DEFAULT_CONTRACT_TYPE="linear"
DEFAULT_MARGIN_MODE="isolated"
DEFAULT_POSITION_MODE="hedge"
DEFAULT_TIMEFRAME="1h"

# Risk Management
DEFAULT_LEVERAGE=10
DEFAULT_MAX_DRAWDOWN_PCT=0.2
DEFAULT_DAILY_LOSS_LIMIT=1000.0
DEFAULT_SIZE_TYPE="risk_based"
DEFAULT_SIZE_VALUE=1.5
DEFAULT_MAX_POSITION_SIZE_QUOTE=50000.0

# Trade Parameters
DEFAULT_STOP_LOSS_PCT=2.0
DEFAULT_TAKE_PROFIT_PCT=4.0
DEFAULT_TRAILING_STOP_PCT=1.0
DEFAULT_TRAILING_ACTIVATION_PCT=2.0
DEFAULT_BREAKEVEN_PCT=1.5
DEFAULT_SLIPPAGE_PCT=0.1
DEFAULT_MAX_SPREAD_PCT=0.1

# Advanced Settings
RATE_LIMIT=1200
ENABLE_METRICS=true
PERSIST_STATE=true
STATE_FILE="state.json"
```

### 2. Enhanced Configuration Module

Update config.py to include all supported exchanges and better align with template.py:

```python
"""Enhanced configuration file for MetaExpert Trading Bot"""

import os
from typing import List, Set

from dotenv import load_dotenv  # type: ignore

_ = load_dotenv()

# Application configuration
APP_NAME = "MetaExpert"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "expert.log")
TRADE_LOG_FILE = os.getenv("TRADE_LOG_FILE", "trades.log")
ERROR_LOG_FILE = os.getenv("ERROR_LOG_FILE", "errors.log")
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# Exchange Configuration
EXCHANGE_BINANCE = "binance"
EXCHANGE_BYBIT = "bybit"
EXCHANGE_OKX = "okx"
EXCHANGE_BITGET = "bitget"
EXCHANGE_KUCOIN = "kucoin"

AVAILABLE_EXCHANGES = [
    EXCHANGE_BINANCE,
    EXCHANGE_BYBIT,
    EXCHANGE_OKX,
    EXCHANGE_BITGET,
    EXCHANGE_KUCOIN,
]

DEFAULT_EXCHANGE = os.getenv("DEFAULT_EXCHANGE", EXCHANGE_BINANCE)

# Exchange-specific API keys (fallback to defaults)
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET", "")
BINANCE_API_PASSPHRASE = os.getenv("BINANCE_API_PASSPHRASE", "")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL", "")
BINANCE_SUBACCOUNT = os.getenv("BINANCE_SUBACCOUNT", "")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "false").lower() == "true"

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")
BYBIT_API_PASSPHRASE = os.getenv("BYBIT_API_PASSPHRASE", "")
BYBIT_BASE_URL = os.getenv("BYBIT_BASE_URL", "")
BYBIT_SUBACCOUNT = os.getenv("BYBIT_SUBACCOUNT", "")
BYBIT_TESTNET = os.getenv("BYBIT_TESTNET", "false").lower() == "true"

OKX_API_KEY = os.getenv("OKX_API_KEY", "")
OKX_API_SECRET = os.getenv("OKX_API_SECRET", "")
OKX_API_PASSPHRASE = os.getenv("OKX_API_PASSPHRASE", "")
OKX_BASE_URL = os.getenv("OKX_BASE_URL", "")
OKX_TESTNET = os.getenv("OKX_TESTNET", "false").lower() == "true"

BITGET_API_KEY = os.getenv("BITGET_API_KEY", "")
BITGET_API_SECRET = os.getenv("BITGET_API_SECRET", "")
BITGET_API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE", "")
BITGET_BASE_URL = os.getenv("BITGET_BASE_URL", "")
BITGET_TESTNET = os.getenv("BITGET_TESTNET", "false").lower() == "true"

KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY", "")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET", "")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE", "")
KUCOIN_BASE_URL = os.getenv("KUCOIN_BASE_URL", "")
KUCOIN_TESTNET = os.getenv("KUCOIN_TESTNET", "false").lower() == "true"

# Market Configuration
MARKET_TYPE_SPOT = "spot"
MARKET_TYPE_FUTURES = "futures"
MARKET_TYPE_OPTIONS = "options"

AVAILABLE_MARKET_TYPES = [
    MARKET_TYPE_SPOT,
    MARKET_TYPE_FUTURES,
    MARKET_TYPE_OPTIONS,
]

DEFAULT_MARKET_TYPE = os.getenv("DEFAULT_MARKET_TYPE", MARKET_TYPE_FUTURES)

# Contract Configuration (for futures)
CONTRACT_TYPE_LINEAR = "linear"  # USDT-M
CONTRACT_TYPE_INVERSE = "inverse"  # COIN-M

AVAILABLE_CONTRACT_TYPES = [
    CONTRACT_TYPE_LINEAR,
    CONTRACT_TYPE_INVERSE,
]

DEFAULT_CONTRACT_TYPE = os.getenv("DEFAULT_CONTRACT_TYPE", CONTRACT_TYPE_LINEAR)

# Margin Configuration (for futures)
MARGIN_MODE_ISOLATED = "isolated"
MARGIN_MODE_CROSS = "cross"

AVAILABLE_MARGIN_MODES = [
    MARGIN_MODE_ISOLATED,
    MARGIN_MODE_CROSS,
]

DEFAULT_MARGIN_MODE = os.getenv("DEFAULT_MARGIN_MODE", MARGIN_MODE_ISOLATED)

# Position Configuration
POSITION_MODE_HEDGE = "hedge"  # Two-way
POSITION_MODE_ONEWAY = "oneway"  # One-way

AVAILABLE_POSITION_MODES = [
    POSITION_MODE_HEDGE,
    POSITION_MODE_ONEWAY,
]

DEFAULT_POSITION_MODE = os.getenv("DEFAULT_POSITION_MODE", POSITION_MODE_HEDGE)

# Trading Configuration
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "1h")
DEFAULT_LOOKBACK_BARS = int(os.getenv("DEFAULT_LOOKBACK_BARS", "100"))

# Risk Management Configuration
DEFAULT_LEVERAGE = int(os.getenv("DEFAULT_LEVERAGE", "10"))
DEFAULT_MAX_DRAWDOWN_PCT = float(os.getenv("DEFAULT_MAX_DRAWDOWN_PCT", "0.2"))
DEFAULT_DAILY_LOSS_LIMIT = float(os.getenv("DEFAULT_DAILY_LOSS_LIMIT", "1000.0"))
DEFAULT_SIZE_TYPE = os.getenv("DEFAULT_SIZE_TYPE", "risk_based")
DEFAULT_SIZE_VALUE = float(os.getenv("DEFAULT_SIZE_VALUE", "1.5"))
DEFAULT_MAX_POSITION_SIZE_QUOTE = float(os.getenv("DEFAULT_MAX_POSITION_SIZE_QUOTE", "50000.0"))

# Trade Parameters
DEFAULT_STOP_LOSS_PCT = float(os.getenv("DEFAULT_STOP_LOSS_PCT", "2.0"))
DEFAULT_TAKE_PROFIT_PCT = float(os.getenv("DEFAULT_TAKE_PROFIT_PCT", "4.0"))
DEFAULT_TRAILING_STOP_PCT = float(os.getenv("DEFAULT_TRAILING_STOP_PCT", "1.0"))
DEFAULT_TRAILING_ACTIVATION_PCT = float(os.getenv("DEFAULT_TRAILING_ACTIVATION_PCT", "2.0"))
DEFAULT_BREAKEVEN_PCT = float(os.getenv("DEFAULT_BREAKEVEN_PCT", "1.5"))
DEFAULT_SLIPPAGE_PCT = float(os.getenv("DEFAULT_SLIPPAGE_PCT", "0.1"))
DEFAULT_MAX_SPREAD_PCT = float(os.getenv("DEFAULT_MAX_SPREAD_PCT", "0.1"))

# Portfolio Management
DEFAULT_MAX_OPEN_POSITIONS = int(os.getenv("DEFAULT_MAX_OPEN_POSITIONS", "3"))
DEFAULT_MAX_POSITIONS_PER_SYMBOL = int(os.getenv("DEFAULT_MAX_POSITIONS_PER_SYMBOL", "1"))

# Entry Filters
DEFAULT_TRADE_HOURS: Set[int] = set(map(int, os.getenv("DEFAULT_TRADE_HOURS", "9,10,11,15").split(",")))
DEFAULT_ALLOWED_DAYS: Set[int] = set(map(int, os.getenv("DEFAULT_ALLOWED_DAYS", "1,2,3,4,5").split(",")))
DEFAULT_MIN_VOLUME = float(os.getenv("DEFAULT_MIN_VOLUME", "1000000"))
DEFAULT_VOLATILITY_FILTER = os.getenv("DEFAULT_VOLATILITY_FILTER", "true").lower() == "true"
DEFAULT_TREND_FILTER = os.getenv("DEFAULT_TREND_FILTER", "true").lower() == "true"

# Advanced Settings
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "1200"))
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
PERSIST_STATE = os.getenv("PERSIST_STATE", "true").lower() == "true"
STATE_FILE = os.getenv("STATE_FILE", "state.json")

# Strategy Metadata
DEFAULT_STRATEGY_ID = int(os.getenv("DEFAULT_STRATEGY_ID", "1001"))
DEFAULT_STRATEGY_NAME = os.getenv("DEFAULT_STRATEGY_NAME", "My Strategy")
DEFAULT_COMMENT = os.getenv("DEFAULT_COMMENT", "my_strategy")
```

### 3. Enhanced Argument Parser

Update _argument.py to include all template parameters as command-line arguments:

```python
"""Enhanced arguments for the trading bot."""

from argparse import ArgumentParser, Namespace

from metaexpert.config import (
    AVAILABLE_EXCHANGES,
    DEFAULT_EXCHANGE,
    DEFAULT_MARKET_TYPE,
    AVAILABLE_MARKET_TYPES,
    DEFAULT_CONTRACT_TYPE,
    AVAILABLE_CONTRACT_TYPES,
    DEFAULT_MARGIN_MODE,
    AVAILABLE_MARGIN_MODES,
    DEFAULT_POSITION_MODE,
    AVAILABLE_POSITION_MODES,
    DEFAULT_TIMEFRAME,
    DEFAULT_LOOKBACK_BARS,
    DEFAULT_SYMBOL,
    DEFAULT_LEVERAGE,
    DEFAULT_MAX_DRAWDOWN_PCT,
    DEFAULT_DAILY_LOSS_LIMIT,
    DEFAULT_SIZE_TYPE,
    DEFAULT_SIZE_VALUE,
    DEFAULT_MAX_POSITION_SIZE_QUOTE,
    DEFAULT_STOP_LOSS_PCT,
    DEFAULT_TAKE_PROFIT_PCT,
    DEFAULT_TRAILING_STOP_PCT,
    DEFAULT_TRAILING_ACTIVATION_PCT,
    DEFAULT_BREAKEVEN_PCT,
    DEFAULT_SLIPPAGE_PCT,
    DEFAULT_MAX_SPREAD_PCT,
    DEFAULT_MAX_OPEN_POSITIONS,
    DEFAULT_MAX_POSITIONS_PER_SYMBOL,
    DEFAULT_TRADE_HOURS,
    DEFAULT_ALLOWED_DAYS,
    DEFAULT_MIN_VOLUME,
    DEFAULT_VOLATILITY_FILTER,
    DEFAULT_TREND_FILTER,
    RATE_LIMIT,
    ENABLE_METRICS,
    PERSIST_STATE,
    STATE_FILE,
    DEFAULT_STRATEGY_ID,
    DEFAULT_STRATEGY_NAME,
    DEFAULT_COMMENT,
)


def parse_arguments() -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="MetaExpert Trading System")

    # Template creation parameters
    parser.add_argument(
        "--new",
        type=str,
        help="Create a new expert file from template with the specified path (e.g., ./experts/my_expert)",
    )

    # Expert Core Configuration
    parser.add_argument(
        "--exchange",
        type=str,
        choices=AVAILABLE_EXCHANGES,
        default=DEFAULT_EXCHANGE,
        help="Supported exchange: binance, bybit, okx, bitget, kucoin",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for exchange authentication",
    )
    parser.add_argument(
        "--api-secret",
        type=str,
        help="API secret for exchange authentication",
    )
    parser.add_argument(
        "--api-passphrase",
        type=str,
        help="API passphrase (required for OKX/KuCoin)",
    )
    parser.add_argument(
        "--subaccount",
        type=str,
        help="Subaccount name (for exchanges that support it)",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        help="Custom API URL",
    )
    parser.add_argument(
        "--testnet",
        action="store_true",
        help="Use exchange testnet",
    )
    parser.add_argument(
        "--market-type",
        type=str,
        choices=AVAILABLE_MARKET_TYPES,
        default=DEFAULT_MARKET_TYPE,
        help="Market type: spot, futures, options",
    )
    parser.add_argument(
        "--contract-type",
        type=str,
        choices=AVAILABLE_CONTRACT_TYPES,
        default=DEFAULT_CONTRACT_TYPE,
        help="Contract type for futures: linear (USDT-M) or inverse (COIN-M)",
    )
    parser.add_argument(
        "--margin-mode",
        type=str,
        choices=AVAILABLE_MARGIN_MODES,
        default=DEFAULT_MARGIN_MODE,
        help="Margin mode for futures: isolated or cross",
    )
    parser.add_argument(
        "--position-mode",
        type=str,
        choices=AVAILABLE_POSITION_MODES,
        default=DEFAULT_POSITION_MODE,
        help="Position mode: hedge (two-way) or oneway (one-way)",
    )

    # Logging Configuration
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        help="Main log file",
    )
    parser.add_argument(
        "--trade-log-file",
        type=str,
        help="Trade execution log file",
    )
    parser.add_argument(
        "--error-log-file",
        type=str,
        help="Error-specific log file",
    )
    parser.add_argument(
        "--no-log-to-console",
        action="store_true",
        help="Disable logging to console",
    )

    # Strategy Initialization Parameters
    parser.add_argument(
        "--symbol",
        type=str,
        default=DEFAULT_SYMBOL,
        help="Trading symbol (e.g., BTCUSDT)",
    )
    parser.add_argument(
        "--timeframe",
        type=str,
        default=DEFAULT_TIMEFRAME,
        help="Primary timeframe: 1m, 5m, 15m, 1h, 4h, 1d, etc.",
    )
    parser.add_argument(
        "--lookback-bars",
        type=int,
        default=DEFAULT_LOOKBACK_BARS,
        help="Number of historical bars to fetch for analysis",
    )
    parser.add_argument(
        "--strategy-id",
        type=int,
        default=DEFAULT_STRATEGY_ID,
        help="Unique ID for order tagging",
    )
    parser.add_argument(
        "--strategy-name",
        type=str,
        default=DEFAULT_STRATEGY_NAME,
        help="Display name for strategy",
    )
    parser.add_argument(
        "--comment",
        type=str,
        default=DEFAULT_COMMENT,
        help="Order comment (max 32 chars Binance, 36 Bybit)",
    )

    # Risk & Position Sizing
    parser.add_argument(
        "--leverage",
        type=int,
        default=DEFAULT_LEVERAGE,
        help="Leverage (verify per-symbol limits)",
    )
    parser.add_argument(
        "--max-drawdown-pct",
        type=float,
        default=DEFAULT_MAX_DRAWDOWN_PCT,
        help="Max drawdown from peak equity (0.2 = 20%)",
    )
    parser.add_argument(
        "--daily-loss-limit",
        type=float,
        default=DEFAULT_DAILY_LOSS_LIMIT,
        help="Daily loss limit in settlement currency",
    )
    parser.add_argument(
        "--size-type",
        type=str,
        default=DEFAULT_SIZE_TYPE,
        help="Position sizing: fixed_base, fixed_quote, percent_equity, risk_based",
    )
    parser.add_argument(
        "--size-value",
        type=float,
        default=DEFAULT_SIZE_VALUE,
        help="Size value based on size-type",
    )
    parser.add_argument(
        "--max-position-size-quote",
        type=float,
        default=DEFAULT_MAX_POSITION_SIZE_QUOTE,
        help="Max position size in quote currency",
    )

    # Trade Parameters
    parser.add_argument(
        "--stop-loss-pct",
        type=float,
        default=DEFAULT_STOP_LOSS_PCT,
        help="Stop-Loss % from entry",
    )
    parser.add_argument(
        "--take-profit-pct",
        type=float,
        default=DEFAULT_TAKE_PROFIT_PCT,
        help="Take-Profit % from entry",
    )
    parser.add_argument(
        "--trailing-stop-pct",
        type=float,
        default=DEFAULT_TRAILING_STOP_PCT,
        help="Trailing stop distance %",
    )
    parser.add_argument(
        "--trailing-activation-pct",
        type=float,
        default=DEFAULT_TRAILING_ACTIVATION_PCT,
        help="Activate trailing stop after X% profit",
    )
    parser.add_argument(
        "--breakeven-pct",
        type=float,
        default=DEFAULT_BREAKEVEN_PCT,
        help="Move SL to breakeven after X% profit",
    )
    parser.add_argument(
        "--slippage-pct",
        type=float,
        default=DEFAULT_SLIPPAGE_PCT,
        help="Expected slippage %",
    )
    parser.add_argument(
        "--max-spread-pct",
        type=float,
        default=DEFAULT_MAX_SPREAD_PCT,
        help="Max allowed spread %",
    )

    # Portfolio Management
    parser.add_argument(
        "--max-open-positions",
        type=int,
        default=DEFAULT_MAX_OPEN_POSITIONS,
        help="Max total open positions",
    )
    parser.add_argument(
        "--max-positions-per-symbol",
        type=int,
        default=DEFAULT_MAX_POSITIONS_PER_SYMBOL,
        help="Max positions per symbol",
    )

    # Entry Filters
    parser.add_argument(
        "--trade-hours",
        type=int,
        nargs="+",
        default=list(DEFAULT_TRADE_HOURS),
        help="Trade only during these UTC hours (space-separated list)",
    )
    parser.add_argument(
        "--allowed-days",
        type=int,
        nargs="+",
        default=list(DEFAULT_ALLOWED_DAYS),
        help="Trade only these days (1=Mon, 7=Sun) (space-separated list)",
    )
    parser.add_argument(
        "--min-volume",
        type=float,
        default=DEFAULT_MIN_VOLUME,
        help="Min volume in settlement_currency",
    )
    parser.add_argument(
        "--no-volatility-filter",
        action="store_true",
        help="Disable volatility filter",
    )
    parser.add_argument(
        "--no-trend-filter",
        action="store_true",
        help="Disable trend filter",
    )

    # Advanced System Settings
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=RATE_LIMIT,
        help="Max requests per minute (RPM)",
    )
    parser.add_argument(
        "--no-enable-metrics",
        action="store_true",
        help="Disable performance metrics",
    )
    parser.add_argument(
        "--no-persist-state",
        action="store_true",
        help="Disable state persistence",
    )
    parser.add_argument(
        "--state-file",
        type=str,
        default=STATE_FILE,
        help="State persistence file",
    )

    # Mode and Run Parameters
    parser.add_argument(
        "--mode",
        type=str,
        choices=["paper", "live", "backtest"],
        default="paper",
        help="Trading mode: paper, live, or backtest",
    )
    parser.add_argument(
        "--backtest-start",
        type=str,
        help="Start date for backtesting (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--backtest-end",
        type=str,
        help="End date for backtesting (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--initial-capital",
        type=float,
        default=10000,
        help="Starting capital in settlement_currency",
    )

    return parser.parse_args()
```

### 4. Updated Template Creator

Enhance template_creator.py to use the improved configuration system:

```python
"""Enhanced module for creating new expert files from template."""

import os
import shutil
from typing import Optional

from metaexpert.config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    OKX_API_KEY,
    OKX_API_SECRET,
    OKX_API_PASSPHRASE,
    BITGET_API_KEY,
    BITGET_API_SECRET,
    KUCOIN_API_KEY,
    KUCOIN_API_SECRET,
    KUCOIN_API_PASSPHRASE,
    DEFAULT_EXCHANGE,
    DEFAULT_MARKET_TYPE,
    DEFAULT_CONTRACT_TYPE,
    DEFAULT_MARGIN_MODE,
    DEFAULT_POSITION_MODE,
    DEFAULT_TIMEFRAME,
    DEFAULT_SYMBOL,
    DEFAULT_LEVERAGE,
    DEFAULT_MAX_DRAWDOWN_PCT,
    DEFAULT_DAILY_LOSS_LIMIT,
    DEFAULT_SIZE_TYPE,
    DEFAULT_SIZE_VALUE,
    DEFAULT_MAX_POSITION_SIZE_QUOTE,
    DEFAULT_STOP_LOSS_PCT,
    DEFAULT_TAKE_PROFIT_PCT,
    DEFAULT_TRAILING_STOP_PCT,
    DEFAULT_TRAILING_ACTIVATION_PCT,
    DEFAULT_BREAKEVEN_PCT,
    DEFAULT_SLIPPAGE_PCT,
    DEFAULT_MAX_SPREAD_PCT,
    DEFAULT_MAX_OPEN_POSITIONS,
    DEFAULT_MAX_POSITIONS_PER_SYMBOL,
    DEFAULT_TRADE_HOURS,
    DEFAULT_ALLOWED_DAYS,
    DEFAULT_MIN_VOLUME,
    DEFAULT_VOLATILITY_FILTER,
    DEFAULT_TREND_FILTER,
    RATE_LIMIT,
    ENABLE_METRICS,
    PERSIST_STATE,
    STATE_FILE,
    DEFAULT_STRATEGY_ID,
    DEFAULT_STRATEGY_NAME,
    DEFAULT_COMMENT,
    LOG_LEVEL,
    LOG_FILE,
    TRADE_LOG_FILE,
    ERROR_LOG_FILE,
    LOG_TO_CONSOLE,
)


def create_expert_from_template(
    file_path: str,
    exchange: Optional[str] = None,
    symbol: Optional[str] = None,
    timeframe: Optional[str] = None,
) -> str:
    """
    Create a new expert file from template with optional configuration.

    Args:
        file_path: Path to the new expert file (with or without extension)
        exchange: Exchange to configure (overrides default)
        symbol: Trading symbol to configure (overrides default)
        timeframe: Timeframe to configure (overrides default)

    Returns:
        Path to the created file
    """
    # Get the absolute path to the template file
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "template.py"
    )

    # Split the path into directory and filename
    output_dir, filename = os.path.split(file_path)

    # If no directory specified, use current directory
    if not output_dir:
        output_dir = "."

    # Make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Add .py extension if not provided
    if not filename.endswith(".py"):
        filename = f"{filename}.py"

    # Create the output file path
    output_path = os.path.join(output_dir, filename)

    # Copy the template file to the output path
    shutil.copy2(template_path, output_path)

    # If specific parameters are provided, update the template
    if exchange or symbol or timeframe:
        _update_template_with_config(output_path, exchange, symbol, timeframe)

    print(f"Created new expert file: {output_path}")
    return output_path


def _update_template_with_config(
    file_path: str,
    exchange: Optional[str] = None,
    symbol: Optional[str] = None,
    timeframe: Optional[str] = None,
) -> None:
    """
    Update the template file with specific configuration.

    Args:
        file_path: Path to the template file
        exchange: Exchange to configure
        symbol: Trading symbol to configure
        timeframe: Timeframe to configure
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update exchange if provided
    if exchange:
        content = _replace_config_value(content, "exchange", f'"{exchange}"')

    # Update symbol if provided
    if symbol:
        content = _replace_init_param(content, "symbol", f'"{symbol}"')

    # Update timeframe if provided
    if timeframe:
        content = _replace_init_param(content, "timeframe", f'"{timeframe}"')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def _replace_config_value(content: str, param: str, value: str) -> str:
    """Replace a configuration value in the expert initialization."""
    import re

    pattern = rf'(\s+{param}=)[^,]+(,?)'
    replacement = rf'\1{value}\2'
    return re.sub(pattern, replacement, content)


def _replace_init_param(content: str, param: str, value: str) -> str:
    """Replace a parameter in the on_init decorator."""
    import re

    pattern = rf'(\s+{param}=)[^,]+(,?)'
    replacement = rf'\1{value}\2'
    return re.sub(pattern, replacement, content)
```

## Benefits of This Approach

1. **Complete Exchange Support**: All exchanges supported by template.py are now properly configured.

2. **Consistent Configuration**: Environment variables, command-line arguments, and template parameters are all aligned.

3. **Improved User Experience**: Users can configure all template parameters through environment variables or command-line arguments.

4. **Better Organization**: Configuration options are logically grouped and clearly documented.

5. **Enhanced Flexibility**: Users can easily customize any aspect of their trading strategy through configuration.

6. **Constitutional Compliance**: The enhanced system follows the Library-First Development and CLI Interface Standard principles from the constitution.