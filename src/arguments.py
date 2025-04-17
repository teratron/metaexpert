"""Arguments for the trading bot."""

import argparse

from src.config import (
    DEFAULT_MODE,
    DEFAULT_TIMEFRAME,
    LOG_LEVEL,
    MAX_POSITION_SIZE,
    MODE_BACKTEST,
    MODE_LIVE,
    MODE_PAPER,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT,
    TRAILING_STOP_PERCENT,
    TRADING_PAIRS,
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Expert Trading Bot")

    parser.add_argument(
        "--mode",
        type=str,
        choices=[MODE_BACKTEST, MODE_PAPER, MODE_LIVE],
        default=DEFAULT_MODE,
        help="Trading mode: backtest, paper, or live",
    )
    parser.add_argument(
        "--pair",
        type=str,
        default=TRADING_PAIRS[0],
        help="Trading pair (e.g., BTCUSDT)",
    )
    parser.add_argument(
        "--timeframe",
        "--tf",
        type=str,
        default=DEFAULT_TIMEFRAME,
        help="Trading timeframe",
    )
    parser.add_argument(
        "--position-size",
        "--size",
        "--ps",
        "--lots",
        type=float,
        default=MAX_POSITION_SIZE,
        help="Maximum position size as a fraction of available balance",
    )
    parser.add_argument(
        "--stop-loss",
        "--sl",
        type=float,
        default=STOP_LOSS_PERCENT,
        help="Stop loss percentage",
    )
    parser.add_argument(
        "--take-profit",
        "--tp",
        type=float,
        default=TAKE_PROFIT_PERCENT,
        help="Take profit percentage",
    )
    parser.add_argument(
        "--trailing-stop",
        "--ts",
        type=float,
        default=TRAILING_STOP_PERCENT,
        help="Trailing stop percentage",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=LOG_LEVEL,
        help="Logging level",
    )
    # TODO: тип торговли: spot, futures, options, etc.
    # TODO: тип ордера: buy, sell, buy limit, sell limit, etc.
    return parser.parse_args()
