"""Utility functions for formatting data for console output."""

import os
from datetime import datetime
from typing import Any

import psutil


def format_datetime(
    dt: datetime | None = None, format_str: str = "%Y-%m-%d %H:%M:%S"
) -> str:
    """
    Format a datetime object to a human-readable string.

    Args:
        dt: The datetime object to format. If None, uses current time.
        format_str: The format string to use. Defaults to "%Y-%m-%d %H:%M:%S".

    Returns:
        Formatted datetime string.
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_str)


def format_currency(
    value: float | int, currency: str = "USD", decimal_places: int = 2
) -> str:
    """
    Format a numeric value as currency.

    Args:
        value: The numeric value to format.
        currency: The currency code (e.g., "USD", "EUR"). Defaults to "USD".
        decimal_places: Number of decimal places. Defaults to 2.

    Returns:
        Formatted currency string.
    """
    return f"{value:,.{decimal_places}f} {currency}"


def format_percentage(value: float | int, decimal_places: int = 2) -> str:
    """
    Format a numeric value as a percentage.

    Args:
        value: The numeric value to format (e.g., 0.05 for 5%).
        decimal_places: Number of decimal places. Defaults to 2.

    Returns:
        Formatted percentage string.
    """
    return f"{value * 100:.{decimal_places}f}%"


def format_large_number(value: float | int) -> str:
    """
    Format large numbers with appropriate suffixes (K, M, B).

    Args:
        value: The numeric value to format.

    Returns:
        Formatted number string with suffix.
    """
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000:.2f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)


def format_table(
    data: list[dict[str, Any]],
    headers: list[str] | None = None,
    column_width: int = 15,
) -> str:
    """
    Format a list of dictionaries as a table for console output.

    Args:
        data: List of dictionaries to format as a table.
        headers: Optional list of headers. If None, uses keys from first dict.
        column_width: Width of each column. Defaults to 15.

    Returns:
        Formatted table string.
    """
    if not data:
        return "No data to display"

    if headers is None:
        headers = list(data[0].keys())

    # Create header row
    header_row = "|"
    separator_row = "|"
    for header in headers:
        header_row += f" {header:<{column_width}} |"
        separator_row += f" {'-' * column_width} |"

    # Create data rows
    rows = [header_row, separator_row]
    for row in data:
        row_str = "|"
        for header in headers:
            value = str(row.get(header, ""))
            row_str += f" {value:<{column_width}} |"
        rows.append(row_str)

    return "\n".join(rows)


def format_error(message: str) -> str:
    """
    Format an error message with styling.

    Args:
        message: The error message to format.

    Returns:
        Formatted error message string.
    """
    return f"[ERROR] {message}"


def format_warning(message: str) -> str:
    """
    Format a warning message with styling.

    Args:
        message: The warning message to format.

    Returns:
        Formatted warning message string.
    """
    return f"[WARNING] {message}"


def format_info(message: str) -> str:
    """
    Format an info message with styling.

    Args:
        message: The info message to format.

    Returns:
        Formatted info message string.
    """
    return f"[INFO] {message}"


def format_success(message: str) -> str:
    """
    Format a success message with styling.

    Args:
        message: The success message to format.

    Returns:
        Formatted success message string.
    """
    return f"[SUCCESS] {message}"


def format_system_info() -> dict[str, str | float | int]:
    """
    Format system information like CPU usage, memory, and PID.

    Returns:
        Dictionary containing formatted system information.
    """
    process = psutil.Process(os.getpid())

    info = {
        "pid": os.getpid(),
        "cpu_percent": process.cpu_percent(interval=1),
        "memory_percent": process.memory_percent(),
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "num_threads": process.num_threads(),
        "status": process.status(),
    }

    # Convert numeric values to strings with appropriate formatting
    formatted_info = {
        "pid": info["pid"],
        "cpu_percent": f"{info['cpu_percent']:.2f}%",
        "memory_percent": f"{info['memory_percent']:.2f}%",
        "memory_mb": f"{info['memory_mb']:.2f} MB",
        "num_threads": info["num_threads"],
        "status": info["status"],
    }

    return formatted_info


def format_process_status() -> str:
    """
    Format current process status information for display.

    Returns:
        Formatted process status string.
    """
    info = format_system_info()

    status_lines = [
        f"PID: {info['pid']}",
        f"CPU: {info['cpu_percent']}",
        f"Memory: {info['memory_percent']} ({info['memory_mb']})",
        f"Threads: {info['num_threads']}",
        f"Status: {info['status']}",
    ]

    return "\n".join(status_lines)


def format_duration(seconds: float) -> str:
    """
    Format a duration in seconds to a human-readable format.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string (e.g., "1h 2m 3s").
    """
    if seconds < 0:
        return "Invalid duration"

    units = [("d", 24 * 60 * 60), ("h", 60 * 60), ("m", 60), ("s", 1)]

    parts = []
    for unit, divisor in units:
        if seconds >= divisor:
            value = int(seconds // divisor)
            parts.append(f"{value}{unit}")
            seconds %= divisor

    if not parts:
        return "0s"

    return " ".join(parts)


def format_bytes(bytes_value: int | float) -> str:
    """
    Format bytes to human-readable format.

    Args:
        bytes_value: Number of bytes.

    Returns:
        Formatted bytes string (e.g., "1.23 KB", "4.56 MB").
    """
    value = float(bytes_value)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024.0:
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{value:.2f} PB"


def format_boolean(value: bool) -> str:
    """
    Format a boolean value as 'Yes'/'No' or 'True'/'False'.

    Args:
        value: Boolean value to format.

    Returns:
        Formatted boolean string.
    """
    return "Yes" if value else "No"


def format_list(items: list[Any], separator: str = ", ") -> str:
    """
    Format a list of items as a string.

    Args:
        items: List of items to format.
        separator: Separator to use between items. Defaults to ", ".

    Returns:
        Formatted list string.
    """
    return separator.join(str(item) for item in items)


def format_key_value_pairs(data: dict[str, Any], indent: int = 0) -> str:
    """
    Format a dictionary as indented key-value pairs.

    Args:
        data: Dictionary to format.
        indent: Number of spaces to indent. Defaults to 0.

    Returns:
        Formatted key-value pairs string.
    """
    indent_str = " " * indent
    lines = []
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}:")
            lines.append(format_key_value_pairs(value, indent + 2))
        else:
            lines.append(f"{indent_str}{key}: {value}")
    return "\n".join(lines)
