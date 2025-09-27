"""Configuration file for Expert Trading Bot"""

import os
from typing import Any

from dotenv import load_dotenv

_ = load_dotenv()

# Application configuration
APP_NAME: str = "MetaExpert"
LIB_NAME: str = "metaexpert"

# Trading parameters
TRADING_PAIRS: str = "BTCUSDT"  # Trading pairs to monitor
BASE_CURRENCY: str = "USDT"  # Base currency for trading
QUOTE_CURRENCIES = ["BTC", "ETH"]  # Quote currencies for trading

# Position sizing and risk management
MAX_POSITION_SIZE = 0.01  # Maximum position size as a fraction of available balance
STOP_LOSS_PERCENT = 0.02  # Stop loss percentage
TAKE_PROFIT_PERCENT = 0.04  # Take profit percentage
TRAILING_STOP_PERCENT = 0.01  # Trailing stop percentage

# Trading timeframes
TIMEFRAMES = {
    "1m": "1m",  # 1 minute
    "5m": "5m",  # 5 minutes
    "15m": "15m",  # 15 minutes
    "30m": "30m",  # 30 minutes
    "1h": "1h",  # 1 hour
    "4h": "4h",  # 4 hours
    "1d": "1d",  # 1 day
}

# Default timeframe for analysis
DEFAULT_TIMEFRAME = TIMEFRAMES["5m"]

# Backtesting parameters
BACKTEST_START_DATE = "2025-01-01"  # Start date for backtesting
BACKTEST_END_DATE = "2025-04-01"  # End date for backtesting

# API request parameters
API_RATE_LIMIT = 1200  # Maximum number of requests per minute
REQUEST_TIMEOUT = 10  # Timeout for API requests in seconds

# Trading bot operation modes
TRADE_MODE_BACKTEST = "backtest"  # Backtesting mode
TRADE_MODE_PAPER = "paper"  # Paper trading mode
TRADE_MODE_LIVE = "live"  # Live trading mode

# Default operation mode
DEFAULT_TRADE_MODE = TRADE_MODE_PAPER

# Trading types
TRADE_TYPE_SPOT = "spot"  # Spot trading
TRADE_TYPE_FUTURES = "futures"  # Futures trading
TRADE_TYPE_OPTIONS = "options"  # Options trading
TRADE_TYPE_MARGIN = "margin"  # Margin trading

# Default trade type
DEFAULT_TRADE_TYPE = TRADE_TYPE_SPOT

# Contract types for futures trading
CONTRACT_TYPE_USD_M = "usd_m"  # USDⓈ-M Futures (USDT/BUSD margined contracts)
CONTRACT_TYPE_COIN_M = "coin_m"  # COIN-M Futures (Coin margined contracts)

# Default contract type
DEFAULT_CONTRACT_TYPE = CONTRACT_TYPE_USD_M

# Available Exchanges
EXCHANGE_BINANCE = "binance"
EXCHANGE_BYBIT = "bybit"
EXCHANGE_OKX = "okx"
EXCHANGE_BITGET = "bitget"
EXCHANGE_KUCOIN = "kucoin"
AVAILABLE_EXCHANGES = [EXCHANGE_BINANCE, EXCHANGE_BYBIT, EXCHANGE_OKX, EXCHANGE_BITGET, EXCHANGE_KUCOIN]

# Default exchange
DEFAULT_EXCHANGE = EXCHANGE_BINANCE

# Trading strategy parameters
ALLOW_LONG_BUYING = True
ALLOW_SHORT_SELLING = True


def get_config_value(parameter_name: str, default_value: Any = None) -> Any:
    """Get a configuration value with proper priority handling.
    
    Args:
        parameter_name: Name of the parameter to get
        default_value: Default value if not found
        
    Returns:
        Configuration value
    """
    # This function would implement the priority logic:
    # 1. CLI arguments (highest priority)
    # 2. Environment variables (medium priority)
    # 3. Default values (lowest priority)
    
    # For now, we'll just check environment variables
    env_var_name = _get_env_var_name(parameter_name)
    if env_var_name and env_var_name in os.environ:
        return os.environ[env_var_name]
    
    return default_value


def _get_env_var_name(parameter_name: str) -> str:
    """Get the environment variable name for a parameter.
    
    Args:
        parameter_name: Name of the parameter
        
    Returns:
        Environment variable name
    """
    # Mapping of parameter names to environment variable names
    env_var_mapping = {
        "exchange": "DEFAULT_EXCHANGE",
        "symbol": "DEFAULT_SYMBOL",
        "timeframe": "DEFAULT_TIMEFRAME",
        "api_key": "API_KEY",
        "api_secret": "API_SECRET",
        "binance_api_key": "BINANCE_API_KEY",
        "binance_api_secret": "BINANCE_API_SECRET",
        "bybit_api_key": "BYBIT_API_KEY",
        "bybit_api_secret": "BYBIT_API_SECRET",
        "okx_api_key": "OKX_API_KEY",
        "okx_api_secret": "OKX_API_SECRET",
        "okx_api_passphrase": "OKX_API_PASSPHRASE",
        "bitget_api_key": "BITGET_API_KEY",
        "bitget_api_secret": "BITGET_API_SECRET",
        "kucoin_api_key": "KUCOIN_API_KEY",
        "kucoin_api_secret": "KUCOIN_API_SECRET",
        "kucoin_api_passphrase": "KUCOIN_API_PASSPHRASE",
    }
    
    return env_var_mapping.get(parameter_name, parameter_name.upper())
