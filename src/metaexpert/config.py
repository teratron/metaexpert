"""Configuration file for Expert Trading Bot"""

from datetime import datetime

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

# API request parameters
API_RATE_LIMIT = 1200  # Maximum number of requests per minute
REQUEST_TIMEOUT = 10  # Timeout for API requests in seconds

# Trading bot operation modes
TRADE_MODE_BACKTEST = "backtest"  # Backtesting mode
TRADE_MODE_PAPER = "paper"  # Paper trading mode
TRADE_MODE_LIVE = "live"  # Live trading mode

# Default operation mode
DEFAULT_TRADE_MODE = TRADE_MODE_PAPER

# Backtesting parameters
BACKTEST_START_DATE: str | datetime = datetime.now().replace(year=datetime.now().year - 1).strftime("%Y-%m-%d")
BACKTEST_END_DATE: str | datetime = datetime.now().strftime("%Y-%m-%d")

# Initial capital for backtesting or paper trading
INITIAL_CAPITAL: float = 10000.0

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
