"""Arguments for the trading bot."""

from argparse import ArgumentParser, Namespace

from metaexpert.config import (
    AVAILABLE_EXCHANGES,
    BACKTEST_END_DATE,
    BACKTEST_START_DATE,
    CONTRACT_TYPE_COIN_M,
    CONTRACT_TYPE_USD_M,
    DEFAULT_CONTRACT_TYPE,
    DEFAULT_EXCHANGE,
    DEFAULT_MODE,
    DEFAULT_TIMEFRAME,
    DEFAULT_TRADE_TYPE,
    LOG_LEVEL,
    MAX_POSITION_SIZE,
    MODE_BACKTEST,
    MODE_LIVE,
    MODE_PAPER,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
    TRADE_TYPE_FUTURES,
    TRADE_TYPE_MARGIN,
    TRADE_TYPE_OPTIONS,
    TRADE_TYPE_SPOT,
    TRADING_PAIRS,
    TRAILING_STOP_PERCENT,
)


def parse_arguments() -> Namespace:
    """Parse command line arguments."""
    parser = ArgumentParser(description="Expert Trading System")

    # Core Configuration Group
    core_group = parser.add_argument_group('Core Configuration', 'Basic settings for the trading system')
    core_group.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=LOG_LEVEL,
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    # Trading Parameters Group
    trading_group = parser.add_argument_group('Trading Parameters', 'Market and trading configuration')
    trading_group.add_argument(
        "--exchange",
        type=str,
        choices=AVAILABLE_EXCHANGES,
        default=DEFAULT_EXCHANGE,
        help="Stock exchange to use (e.g., binance, bybit, okx, bitget, kucoin)",
    )
    trading_group.add_argument(
        "--trade-mode",
        type=str,
        choices=[MODE_BACKTEST, MODE_PAPER, MODE_LIVE],
        default=DEFAULT_MODE,
        help="Trading mode: backtest, paper, or live",
    )
    trading_group.add_argument(
        "--market-type",
        type=str,
        choices=[TRADE_TYPE_SPOT, TRADE_TYPE_FUTURES, TRADE_TYPE_OPTIONS, TRADE_TYPE_MARGIN],
        default=DEFAULT_TRADE_TYPE,
        help="Trading type: spot, futures, options, or margin",
    )
    trading_group.add_argument(
        "--contract-type",
        type=str,
        choices=[CONTRACT_TYPE_USD_M, CONTRACT_TYPE_COIN_M],
        default=DEFAULT_CONTRACT_TYPE,
        help="Contract type for futures trading: USDⓈ-M (usd_m) or COIN-M (coin_m)",
    )
    trading_group.add_argument(
        "--pair",
        "--symbol",
        type=str,
        default=TRADING_PAIRS[0],
        help="Trading pair (e.g., BTCUSDT)",
    )
    trading_group.add_argument(
        "-tf",
        "--timeframe",
        type=str,
        default=DEFAULT_TIMEFRAME,
        help="Trading timeframe",
    )

    # Risk Management Group
    risk_group = parser.add_argument_group('Risk Management', 'Position sizing and risk controls')
    risk_group.add_argument(
        "--size",
        "--lots",
        type=float,
        default=MAX_POSITION_SIZE,
        help="Maximum position size as a fraction of available balance",
    )
    risk_group.add_argument(
        "-sl",
        "--stop-loss",
        type=float,
        default=STOP_LOSS_PERCENT,
        help="Stop loss percentage",
    )
    risk_group.add_argument(
        "-tp",
        "--take-profit",
        type=float,
        default=TAKE_PROFIT_PERCENT,
        help="Take profit percentage",
    )
    risk_group.add_argument(
        "-ts",
        "--trailing-stop",
        type=float,
        default=TRAILING_STOP_PERCENT,
        help="Trailing stop percentage",
    )

    # Backtesting Group
    backtest_group = parser.add_argument_group('Backtesting', 'Parameters for backtesting strategies')
    backtest_group.add_argument(
        "--start-date",
        type=str,
        default=BACKTEST_START_DATE,
        help="Start date for backtesting (YYYY-MM-DD)",
    )
    backtest_group.add_argument(
        "--end-date",
        type=str,
        default=BACKTEST_END_DATE,
        help="End date for backtesting (YYYY-MM-DD)",
    )
    backtest_group.add_argument(
        "--balance",
        type=float,
        default=1000.0,
        help="Initial balance for backtesting",
    )
    backtest_group.add_argument(
        "--output",
        type=str,
        help="Output file for backtest results (JSON format)",
    )

    # Authentication Group
    auth_group = parser.add_argument_group('Authentication', 'API credentials and security settings')
    auth_group.add_argument(
        "--api-key",
        "--key",
        type=str,
        help="API key for exchange authentication",
    )
    auth_group.add_argument(
        "--api-secret",
        "--secret",
        type=str,
        help="API secret for exchange authentication",
    )
    auth_group.add_argument(
        "--base-url",
        "--url",
        type=str,
        help="Base URL for the exchange API",
    )

    # Template Management Group
    template_group = parser.add_argument_group('Template Management', 'Options for creating and managing expert templates')
    template_group.add_argument(
        "--new",
        type=str,
        help="Create a new expert file from template with the specified path (e.g., ./experts/my_expert)",
    )

    return parser.parse_args()
