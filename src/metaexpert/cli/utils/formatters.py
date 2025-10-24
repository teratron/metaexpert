"""Output formatting utilities."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}m"

    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f}h"

    days = hours / 24
    return f"{days:.1f}d"


def format_datetime(dt: datetime, include_time: bool = True) -> str:
    """Format datetime for display."""
    if include_time:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%m-%d")


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage for display."""
    return f"{value:.{decimals}f}%"


def format_money(value: float, currency: str = "USD", decimals: int = 2) -> str:
    """Format money for display."""
    return f"{value:,.{decimals}f} {currency}"


def format_json_pretty(data: Dict[str, Any]) -> str:
    """Format JSON with pretty printing."""
    return json.dumps(data, indent=2, sort_keys=True)


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate string to max length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def format_path_relative(path: Path, base: Path = Path.cwd()) -> str:
    """Format path relative to base."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)
