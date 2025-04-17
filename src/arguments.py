"""

"""
import argparse

from src.config import (
    DEFAULT_MODE,
    DEFAULT_TIMEFRAME,
    LOG_LEVEL,
    MODE_BACKTEST,
    MODE_LIVE,
    MODE_PAPER,
    TRADING_PAIRS
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
        type=str,
        default=DEFAULT_TIMEFRAME,
        help="Trading timeframe",
    )
    # lots=0.0001, stop_loss=0.0001, take_profit=0.0001, trailing_stop=0.0001
    # MAX_POSITION_SIZE = 0.01  # Maximum position size as a fraction of available balance
    # STOP_LOSS_PERCENT = 0.02  # Stop loss percentage
    # TAKE_PROFIT_PERCENT = 0.04  # Take profit percentage

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=LOG_LEVEL,
        help="Logging level",
    )
    return parser.parse_args()
