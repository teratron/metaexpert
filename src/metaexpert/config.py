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

# Market types
MARKET_TYPE_SPOT: str = "spot"
MARKET_TYPE_FUTURES: str = "futures"
MARKET_TYPE_OPTIONS: str = "options"

# Default market type
DEFAULT_MARKET_TYPE: str = MARKET_TYPE_FUTURES

# Contract types for futures trading
CONTRACT_TYPE_LINEAR: str = "linear"    # USDT-M Futures /fapi/*
CONTRACT_TYPE_INVERSE: str = "inverse"  # COIN-M Delivery /dapi/*

# Default contract type for futures trading
DEFAULT_CONTRACT_TYPE: str = CONTRACT_TYPE_LINEAR

# Position modes for futures trading
MARGIN_MODE_ISOLATED: str = "isolated"
MARGIN_MODE_CROSS: str = "cross"

# Default position mode for futures trading
DEFAULT_MARGIN_MODE: str = MARGIN_MODE_ISOLATED

# Position modes for futures trading
POSITION_MODE_HEDGE: str = "hedge"
POSITION_MODE_ONEWAY: str = "oneway"

# Default position mode for futures trading
DEFAULT_POSITION_MODE: str = POSITION_MODE_HEDGE

# API request parameters
RATE_LIMIT: int = 1200                  # Max requests per minute (RPM). Varies by exchange and API tier.
REQUEST_TIMEOUT: int = 10               # Timeout for API requests in seconds

# Advanced System Settings
ENABLE_METRICS: bool = True             # Enable performance metrics
PERSIST_STATE: bool = True              # Persist state between runs
STATE_FILE: str = "state.json"          # State persistence file (relative to working directory)

# Trading bot operation modes
TRADE_MODE_BACKTEST: str = "backtest"  # Backtesting mode
TRADE_MODE_PAPER: str = "paper"  # Paper trading mode
TRADE_MODE_LIVE: str = "live"  # Live trading mode

# Default trading bot operation mode
DEFAULT_TRADE_MODE: str = TRADE_MODE_PAPER

# Backtesting parameters
BACKTEST_START_DATE: str | datetime = datetime.now().replace(year=datetime.now().year - 1).strftime("%Y-%m-%d")
BACKTEST_END_DATE: str | datetime = datetime.now().strftime("%Y-%m-%d")

# Initial capital for backtesting or paper trading
INITIAL_CAPITAL: float = 10000.0
