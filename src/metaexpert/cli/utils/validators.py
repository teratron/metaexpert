# src/metaexpert/cli/utils/validators.py
"""Input validation utilities."""

import re
from pathlib import Path
from typing import Any


def validate_project_name(name: str) -> None:
    """
    Validate project name.

    Rules:
    - Must start with letter or underscore
    - Can contain letters, numbers, hyphens, underscores
    - Length 3-50 characters
    - Cannot be Python keywords

    Args:
        name: Project name to validate

    Raises:
        ValueError: If name is invalid
    """
    # Check for Python keywords first
    import keyword

    if keyword.iskeyword(name):
        raise ValueError(f"'{name}' is a Python keyword and cannot be used")

    # Check length
    if len(name) < 3:
        raise ValueError("Project name must be at least 3 characters long")

    if len(name) > 50:
        raise ValueError("Project name must not exceed 50 characters")

    # Check pattern
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_-]*$"
    if not re.match(pattern, name):
        raise ValueError(
            "Project name must start with a letter or underscore "
            "and contain only letters, numbers, hyphens, and underscores"
        )

    # Check for common reserved names
    reserved = {"test", "tests", "src", "lib", "bin", "build", "dist"}
    if name.lower() in reserved:
        raise ValueError(f"'{name}' is a reserved name")


def validate_exchange(exchange: str) -> None:
    """Validate exchange name."""
    supported = {"binance", "bybit", "okx", "mexc", "kucoin", "bitget"}

    if exchange.lower() not in supported:
        raise ValueError(
            f"Unsupported exchange: {exchange}. "
            f"Supported: {', '.join(sorted(supported))}"
        )


def validate_strategy(strategy: str) -> None:
    """Validate strategy name."""
    supported = {"template", "ema", "rsi", "macd", "bollinger", "custom"}

    if strategy.lower() not in supported:
        raise ValueError(
            f"Unknown strategy: {strategy}. Available: {', '.join(sorted(supported))}"
        )


def validate_market_type(market_type: str) -> None:
    """Validate market type."""
    supported = {"spot", "futures", "options"}

    if market_type.lower() not in supported:
        raise ValueError(
            f"Invalid market type: {market_type}. "
            f"Supported: {', '.join(sorted(supported))}"
        )


def validate_date_format(date_str: str) -> None:
    """Validate date format (YYYY-MM-DD)."""
    pattern = r"^\d{4}-\d{2}-\d{2}$"

    if not re.match(pattern, date_str):
        raise ValueError(f"Invalid date format: {date_str}. Expected: YYYY-MM-DD")

    # Additional validation with datetime
    from datetime import datetime

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date: {date_str}. {e}")


def validate_path_exists(path: Path, file_type: str = "path") -> None:
    """Validate that path exists."""
    if not path.exists():
        # Use forward slashes to ensure consistent output across platforms for testing
        path_str = str(path).replace("\\", "/")
        raise ValueError(f"{file_type.capitalize()} not found: {path_str}")


def validate_positive_number(value: Any, name: str = "value") -> None:
    """Validate that number is positive."""
    # First try to convert to float to check if it's a valid number
    try:
        num = float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid {name}: {value}")
    
    # Check for special float values (inf, nan)
    import math
    if math.isnan(num) or math.isinf(num):
        raise ValueError(f"Invalid {name}: {value}")
    
    # Then check if the number is positive
    if num <= 0:
        raise ValueError(f"{name} must be positive, got {num}")
