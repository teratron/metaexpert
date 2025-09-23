"""Argument validation utilities for CLI arguments."""

import re

from metaexpert.exceptions import ValidationError
from metaexpert.logger import get_logger

# Get the logger instance
logger = get_logger("metaexpert.cli.argument_validation")


class ArgumentValidationError(ValidationError):
    """Exception raised for argument validation errors."""

    pass


class ArgumentValidationUtils:
    """Utilities for validating command-line argument values."""

    @staticmethod
    def validate_exchange(exchange: str, valid_exchanges: list[str]) -> None:
        """Validate exchange value.

        Args:
            exchange: Exchange name to validate
            valid_exchanges: List of valid exchange names

        Raises:
            ArgumentValidationError: If exchange is not valid
        """
        if exchange not in valid_exchanges:
            raise ArgumentValidationError(
                f"Invalid exchange '{exchange}'. Valid exchanges are: {', '.join(valid_exchanges)}"
            )

    @staticmethod
    def validate_percentage(
        value: float, min_value: float = 0.0, max_value: float = 100.0
    ) -> None:
        """Validate percentage value.

        Args:
            value: Percentage value to validate
            min_value: Minimum allowed value
            max_value: Maximum allowed value

        Raises:
            ArgumentValidationError: If value is not within range
        """
        if not min_value <= value <= max_value:
            raise ArgumentValidationError(
                f"Percentage value {value} must be between {min_value} and {max_value}"
            )

    @staticmethod
    def validate_positive_float(value: float) -> None:
        """Validate that a float value is positive.

        Args:
            value: Float value to validate

        Raises:
            ArgumentValidationError: If value is not positive
        """
        if value <= 0:
            raise ArgumentValidationError(f"Value {value} must be positive")

    @staticmethod
    def validate_date_format(date_str: str) -> None:
        """Validate date format (YYYY-MM-DD).

        Args:
            date_str: Date string to validate

        Raises:
            ArgumentValidationError: If date format is invalid
        """
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            raise ArgumentValidationError(
                f"Invalid date format '{date_str}'. Expected format: YYYY-MM-DD"
            )

    @staticmethod
    def validate_trading_pair(pair: str) -> None:
        """Validate trading pair format.

        Args:
            pair: Trading pair to validate

        Raises:
            ArgumentValidationError: If pair format is invalid
        """
        if not re.match(r"^[A-Z0-9]{3,10}[A-Z0-9]{3,10}$", pair):
            raise ArgumentValidationError(
                f"Invalid trading pair '{pair}'. Expected format: BTCUSDT, ETHBTC, etc."
            )

    @staticmethod
    def validate_timeframe(timeframe: str) -> None:
        """Validate timeframe format.

        Args:
            timeframe: Timeframe to validate

        Raises:
            ArgumentValidationError: If timeframe format is invalid
        """
        valid_timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"]
        if timeframe not in valid_timeframes:
            raise ArgumentValidationError(
                f"Invalid timeframe '{timeframe}'. Valid timeframes are: {', '.join(valid_timeframes)}"
            )

    @staticmethod
    def validate_log_level(level: str) -> None:
        """Validate log level.

        Args:
            level: Log level to validate

        Raises:
            ArgumentValidationError: If log level is invalid
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level not in valid_levels:
            raise ArgumentValidationError(
                f"Invalid log level '{level}'. Valid levels are: {', '.join(valid_levels)}"
            )

    @staticmethod
    def validate_trade_mode(mode: str) -> None:
        """Validate trade mode.

        Args:
            mode: Trade mode to validate

        Raises:
            ArgumentValidationError: If trade mode is invalid
        """
        valid_modes = ["backtest", "paper", "live"]
        if mode not in valid_modes:
            raise ArgumentValidationError(
                f"Invalid trade mode '{mode}'. Valid modes are: {', '.join(valid_modes)}"
            )

    @staticmethod
    def validate_market_type(market_type: str) -> None:
        """Validate market type.

        Args:
            market_type: Market type to validate

        Raises:
            ArgumentValidationError: If market type is invalid
        """
        valid_types = ["spot", "futures", "options", "margin"]
        if market_type not in valid_types:
            raise ArgumentValidationError(
                f"Invalid market type '{market_type}'. Valid types are: {', '.join(valid_types)}"
            )
