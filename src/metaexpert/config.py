"""Configuration file for Expert Trading Bot"""

from datetime import datetime
from typing import Literal

# -----------------------------------------------------------------------------
# APPLICATION CONFIGURATION
# -----------------------------------------------------------------------------

# Application metadata
APP_VERSION: str = "0.1.0"
APP_DESCRIPTION: str = "Expert trading system for algorithmic trading."
APP_NAME: str = "MetaExpert"
LIB_NAME: str = "metaexpert"

# -----------------------------------------------------------------------------
# LOGGING CONFIGURATION
# -----------------------------------------------------------------------------

#  Logging metadata
LOG_NAME: str = APP_NAME

# Log levels
LOG_LEVEL_TYPE = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Default log levels
LOG_LEVEL: LOG_LEVEL_TYPE = "DEBUG"
LOG_TRADE_LEVEL: LOG_LEVEL_TYPE = "INFO"
LOG_ERROR_LEVEL: LOG_LEVEL_TYPE = "ERROR"

# Directory configuration
LOG_DIRECTORY: str = "logs"

# Default file names
LOG_FILE: str = "expert.log"
LOG_TRADE_FILE: str = "trades.log"
LOG_ERROR_FILE: str = "errors.log"

# File rotation settings
LOG_MAX_FILE_SIZE: int = 10485760  # 10 * 1024 * 1024 (10MB)
LOG_BACKUP_COUNT: int = 5

# Format settings
LOG_FORMAT: str = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
LOG_DETAILED_FORMAT: str = (
    "[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s"
)
LOG_FALLBACK_FORMAT: str = "[%(asctime)s] %(levelname)s: (LOGGING-FALLBACK) %(message)s"

# Enhanced configuration flags
LOG_CONSOLE_LOGGING: bool = True
LOG_FILE_LOGGING: bool = True
LOG_STRUCTURED_LOGGING: bool = False
LOG_ASYNC_LOGGING: bool = False

# -----------------------------------------------------------------------------
# EXCHANGE-SPECIFIC CONFIGURATION
# -----------------------------------------------------------------------------

# Market types
MARKET_TYPE_SPOT: str = "spot"
MARKET_TYPE_FUTURES: str = "futures"
MARKET_TYPE_OPTIONS: str = "options"

# Default market type
DEFAULT_MARKET_TYPE: str = MARKET_TYPE_FUTURES

# Contract types for futures trading
CONTRACT_TYPE_LINEAR: str = "linear"  # USDT-M Futures /fapi/*
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

# -----------------------------------------------------------------------------
# TRADING STRATEGY CONFIGURATION
# -----------------------------------------------------------------------------

# Core trading parameters
DEFAULT_SYMBOL: str = "BTCUSDT"
DEFAULT_TIMEFRAME: str = "1h"
LOOKBACK_BARS: int = 100
LOOKBACK_TIME: str = "7d"
WARMUP_BARS: int = 0

# Strategy Metadata
STRATEGY_ID: int = 1001
STRATEGY_NAME: str = "My Strategy"
COMMENT: str = "my_strategy"

# Risk & position sizing
LEVERAGE: int = 10
MAX_DRAWDOWN_PCT: float = 0.2
DAILY_LOSS_LIMIT: float = 1000.0
SIZE_VALUE: float = 1.5
MAX_POSITION_SIZE_QUOTE: float = 50000.0

# Size types
SIZE_TYPE_FIXED_BASE: str = "fixed_base"
SIZE_TYPE_FIXED_QUOTE: str = "fixed_quote"
SIZE_TYPE_PERCENT_EQUITY: str = "percent_equity"
SIZE_TYPE_RISK_BASED: str = "risk_based"

# Default size type
DEFAULT_SIZE_TYPE: str = SIZE_TYPE_RISK_BASED

# Trade parameters
STOP_LOSS_PCT: float = 2.0
TAKE_PROFIT_PCT: float = 4.0
TRAILING_STOP_PCT: float = 1.0
TRAILING_ACTIVATION_PCT: float = 2.0
BREAKEVEN_PCT: float = 1.5
SLIPPAGE_PCT: float = 0.1
MAX_SPREAD_PCT: float = 0.1

# Portfolio management
MAX_OPEN_POSITIONS: int = 3
MAX_POSITIONS_PER_SYMBOL: int = 1

# Entry filters
TRADE_HOURS: set[int] = {
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
}
ALLOWED_DAYS: set[int] = {1, 2, 3, 4, 5, 6, 7}
MIN_VOLUME: int = 1000000
VOLATILITY_FILTER: bool = True
TREND_FILTER: bool = True

# -----------------------------------------------------------------------------
# TRADING BOT OPERATION MODES
# -----------------------------------------------------------------------------

# Trading modes
TRADE_MODE_BACKTEST: str = "backtest"  # Backtesting mode
TRADE_MODE_PAPER: str = "paper"  # Paper trading mode
TRADE_MODE_LIVE: str = "live"  # Live trading mode

# Default trading mode
DEFAULT_TRADE_MODE: str = TRADE_MODE_PAPER

# Backtesting parameters
BACKTEST_START_DATE: str = (
    datetime.now().replace(year=datetime.now().year - 1).strftime("%Y-%m-%d")
)
BACKTEST_END_DATE: str = datetime.now().strftime("%Y-%m-%d")

# Initial capital for backtesting or paper trading
INITIAL_CAPITAL: float = 10000.0
