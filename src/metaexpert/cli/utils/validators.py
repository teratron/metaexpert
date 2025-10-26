"""Validator functions for CLI input validation.

This module contains a collection of validation functions for various types of
CLI inputs including project names, exchange names, strategy names, dates,
numeric values, and file paths.
"""

import os
import re
from datetime import datetime
from pathlib import Path

from src.metaexpert.cli.core.exceptions import ValidationError


def validate_project_name(name: str, max_length: int = 50) -> bool:
    """Validate project name format and constraints.

    Args:
        name: Project name to validate
        max_length: Maximum allowed length for the project name

    Returns:
        True if valid

    Raises:
        ValidationError: If the project name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationError("Project name must be a non-empty string")

    if len(name) > max_length:
        raise ValidationError(
            f"Project name exceeds maximum length of {max_length} characters"
        )

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        raise ValidationError(
            "Project name must start with a letter and contain only letters, numbers, underscores, and hyphens"
        )

    if name.startswith("_") or name.startswith("-"):
        raise ValidationError("Project name cannot start with underscore or hyphen")

    if name.endswith("_") or name.endswith("-"):
        raise ValidationError("Project name cannot end with underscore or hyphen")

    return True


def validate_exchange_name(name: str) -> bool:
    """Validate exchange name format.

    Args:
        name: Exchange name to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If the exchange name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationError("Exchange name must be a non-empty string")

    # Common exchange names used in the project
    valid_exchanges = {"binance", "bybit", "okx", "kucoin", "mexc", "bitget"}

    if name.lower() not in valid_exchanges:
        raise ValidationError(
            f"Invalid exchange name: '{name}'. Valid options are: {', '.join(valid_exchanges)}"
        )

    return True


def validate_strategy_name(name: str) -> bool:
    """Validate strategy name format.

    Args:
        name: Strategy name to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If the strategy name is invalid
    """
    if not name or not isinstance(name, str):
        raise ValidationError("Strategy name must be a non-empty string")

    if len(name) < 3:
        raise ValidationError("Strategy name must be at least 3 characters long")

    if len(name) > 50:
        raise ValidationError("Strategy name cannot exceed 50 characters")

    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name):
        raise ValidationError(
            "Strategy name must start with a letter and contain only letters, numbers, underscores, and hyphens"
        )

    return True


def validate_datetime_format(
    date_string: str, date_format: str = "%Y-%m-%d %H:%M:%S"
) -> bool:
    """Validate date and time format.

    Args:
        date_string: Date string to validate
        date_format: Expected date format (default: "%Y-%m-%d %H:%M:%S")

    Returns:
        True if valid

    Raises:
        ValidationError: If the date format is invalid
    """
    if not date_string or not isinstance(date_string, str):
        raise ValidationError("Date must be a non-empty string")

    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        raise ValidationError(
            f"Date format invalid. Expected format: {date_format}. Received: {date_string}"
        ) from None


def validate_date_format(date_string: str, date_format: str = "%Y-%m-%d") -> bool:
    """Validate date format.

    Args:
        date_string: Date string to validate
        date_format: Expected date format (default: "%Y-%m-%d")

    Returns:
        True if valid

    Raises:
        ValidationError: If the date format is invalid
    """
    if not date_string or not isinstance(date_string, str):
        raise ValidationError("Date must be a non-empty string")

    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        raise ValidationError(
            f"Date format invalid. Expected format: {date_format}. Received: {date_string}"
        ) from None


def validate_positive_number(value: int | float | str) -> bool:
    """Validate that a value is a positive number.

    Args:
        value: Value to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If the value is not a positive number
    """
    try:
        num_value = float(value)
        if num_value <= 0:
            raise ValidationError(f"Value must be a positive number, got: {value}")
        return True
    except (ValueError, TypeError):
        raise ValidationError(f"Value must be a number, got: {type(value).__name__}") from None


def validate_numeric_range(
    value: int | float | str,
    min_val: int | float | None = None,
    max_val: int | float | None = None,
) -> bool:
    """Validate that a numeric value is within a specified range.


    Args:
        value: Value to validate
        min_val: Minimum allowed value (optional)
        max_val: Maximum allowed value (optional)

    Returns:
        True if valid

    Raises:
        ValidationError: If the value is outside the specified range
    """
    try:
        num_value = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"Value must be a number, got: {type(value).__name__}") from None

    if min_val is not None and num_value < min_val:
        raise ValidationError(
            f"Value {num_value} is less than minimum allowed value {min_val}"
        )

    if max_val is not None and num_value > max_val:
        raise ValidationError(
            f"Value {num_value} is greater than maximum allowed value {max_val}"
        )

    return True


def validate_percentage(value: int | float | str) -> bool:
    """Validate that a value is a valid percentage (0-100).

    Args:
        value: Percentage value to validate

    Returns:
        True if valid

    Raises:
        ValidationError: If the value is not a valid percentage
    """
    return validate_numeric_range(value, min_val=0, max_val=100)


def validate_file_path(
    path: str, must_exist: bool = True, must_be_file: bool = True
) -> bool:
    """Validate file path.

    Args:
        path: File path to validate
        must_exist: Whether the path must exist (default: True)
        must_be_file: Whether the path must be a file (vs directory) (default: True)

    Returns:
        True if valid

    Raises:
        ValidationError: If the path is invalid
    """
    if not path or not isinstance(path, str):
        raise ValidationError("Path must be a non-empty string")

    path_obj = Path(path)

    # Check if path contains invalid characters
    invalid_chars = '<>:"|?*'
    if any(char in invalid_chars for char in path):
        raise ValidationError(f"Path contains invalid characters: {invalid_chars}")

    # Check if path is absolute and potentially unsafe
    if os.path.isabs(path):
        # For security, we might want to restrict absolute paths depending on use case
        # For now, just warn if it's outside expected directories
        if not str(path_obj).startswith((".", os.getcwd(), os.path.expanduser("~"))):
            raise ValidationError("Path is outside allowed directories")

    if must_exist and not path_obj.exists():
        raise ValidationError(f"Path does not exist: {path}")

    if must_exist and must_be_file and path_obj.is_dir():
        raise ValidationError(f"Path exists but is a directory, expected file: {path}")

    if must_exist and not must_be_file and path_obj.is_file():
        raise ValidationError(f"Path exists but is a file, expected directory: {path}")

    # Check for path traversal attacks
    if ".." in path.split(os.sep) or ".." in path.split("/"):
        raise ValidationError(
            "Path contains directory traversal ('..') which is not allowed"
        )

    return True


def validate_directory_path(path: str, must_exist: bool = True) -> bool:
    """Validate directory path.

    Args:
        path: Directory path to validate
        must_exist: Whether the directory must exist (default: True)

    Returns:
        True if valid

    Raises:
        ValidationError: If the directory path is invalid
    """
    return validate_file_path(path, must_exist=must_exist, must_be_file=False)


def validate_timeframe(timeframe: str) -> bool:
    """Validate trading timeframe format.

    Args:
        timeframe: Timeframe to validate (e.g., '1m', '5m', '1h', '1d')

    Returns:
        True if valid

    Raises:
        ValidationError: If the timeframe is invalid
    """
    if not timeframe or not isinstance(timeframe, str):
        raise ValidationError("Timeframe must be a non-empty string")

    # Common timeframe patterns in trading
    valid_patterns = [
        r"^\d+s$",  # seconds
        r"^\d+m$",  # minutes
        r"^\d+h$",  # hours
        r"^\d+d$",  # days
        r"^\d+w$",  # weeks
        r"^\d+M$",  # months
    ]

    if not any(re.match(pattern, timeframe) for pattern in valid_patterns):
        raise ValidationError(
            f"Invalid timeframe format: {timeframe}. Valid formats include: 1m, 5m, 1h, 1d, 1w, 1M, etc."
        )

    # Extract numeric value and validate it's reasonable
    number_part = re.match(r"^(\d+)", timeframe)
    if number_part:
        num = int(number_part.group(1))
        if num <= 0:
            raise ValidationError(f"Timeframe value must be positive, got: {num}")

    return True


def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format.

    Args:
        symbol: Trading symbol to validate (e.g., 'BTCUSDT', 'ETH/USDT')

    Returns:
        True if valid

    Raises:
        ValidationError: If the symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")

    # Common symbol formats: BTCUSDT, ETH/USDT, BTC-USDT, etc.
    pattern = r"^[A-Z0-9]+[/\-]?[A-Z0-9]+$"
    if not re.match(pattern, symbol):
        raise ValidationError(
            f"Invalid symbol format: {symbol}. Valid format is base/quote currency pair (e.g., BTCUSDT, ETH/USDT)"
        )

    return True
