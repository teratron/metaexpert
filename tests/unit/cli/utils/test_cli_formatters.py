"""Tests for formatting functions in src/metaexpert/cli/utils/formatters.py"""

import datetime
from unittest.mock import MagicMock, patch

from metaexpert.cli.utils.formatters import (
    format_boolean,
    format_bytes,
    format_currency,
    format_datetime,
    format_duration,
    format_error,
    format_info,
    format_key_value_pairs,
    format_large_number,
    format_list,
    format_percentage,
    format_process_status,
    format_success,
    format_system_info,
    format_table,
    format_warning,
)


class TestFormatDatetime:
    """Test cases for format_datetime function."""

    def test_format_datetime_with_datetime_object(self):
        """Test formatting a specific datetime object."""
        dt = datetime.datetime(2023, 6, 15, 14, 30, 45)
        result = format_datetime(dt)
        assert result == "2023-06-15 14:30:45"

    def test_format_datetime_with_custom_format(self):
        """Test formatting with custom format string."""
        dt = datetime.datetime(2023, 6, 15, 14, 30, 45)
        result = format_datetime(dt, "%Y/%m/%d %H:%M")
        assert result == "2023/06/15 14:30"

    def test_format_datetime_with_none(self):
        """Test formatting with None (should use current time)."""
        # We can't predict the exact time, but we can check the format
        result = format_datetime(None)
        # Check that it matches the expected format (YYYY-MM-DD HH:MM:SS)
        assert len(result) == 19
        assert (
            result[4] == "-"
            and result[7] == "-"
            and result[10] == " "
            and result[13] == ":"
            and result[16] == ":"
        )

    def test_format_datetime_default(self):
        """Test formatting with default parameters."""
        # We can't predict the exact time, but we can check the format
        result = format_datetime()
        # Check that it matches the expected format (YYYY-MM-DD HH:MM:SS)
        assert len(result) == 19
        assert (
            result[4] == "-"
            and result[7] == "-"
            and result[10] == " "
            and result[13] == ":"
            and result[16] == ":"
        )


class TestFormatCurrency:
    """Test cases for format_currency function."""

    def test_format_currency_positive(self):
        """Test formatting positive currency values."""
        assert format_currency(1234.56) == "1,234.56 USD"
        assert format_currency(1000000) == "1,000,000.00 USD"
        assert format_currency(0.99) == "0.99 USD"

    def test_format_currency_negative(self):
        """Test formatting negative currency values."""
        assert format_currency(-1234.56) == "-1,234.56 USD"

    def test_format_currency_custom_currency(self):
        """Test formatting with custom currency code."""
        assert format_currency(1234.56, "EUR") == "1,234.56 EUR"

    def test_format_currency_custom_decimal_places(self):
        """Test formatting with custom decimal places."""
        assert format_currency(1234.567, decimal_places=3) == "1,234.567 USD"
        assert format_currency(1234, decimal_places=0) == "1,234 USD"

    def test_format_currency_integer(self):
        """Test formatting integer values."""
        assert format_currency(1234) == "1,234.00 USD"


class TestFormatPercentage:
    """Test cases for format_percentage function."""

    def test_format_percentage_decimal(self):
        """Test formatting decimal values as percentages."""
        assert format_percentage(0.05) == "5.00%"
        assert format_percentage(0.1234) == "12.34%"
        assert format_percentage(1.0) == "10.00%"

    def test_format_percentage_custom_decimal_places(self):
        """Test formatting with custom decimal places."""
        assert format_percentage(0.12345, decimal_places=4) == "12.3450%"
        assert format_percentage(0.12345, decimal_places=1) == "12.3%"

    def test_format_percentage_integer(self):
        """Test formatting integer values as percentages."""
        assert format_percentage(5) == "500.00%"
        assert format_percentage(100) == "10000.00%"

    def test_format_percentage_negative(self):
        """Test formatting negative values as percentages."""
        assert format_percentage(-0.05) == "-5.00%"


class TestFormatLargeNumber:
    """Test cases for format_large_number function."""

    def test_format_large_number_billions(self):
        """Test formatting numbers in billions."""
        assert format_large_number(1_500_000_000) == "1.50B"
        assert format_large_number(2_000_000_000) == "2.00B"

    def test_format_large_number_millions(self):
        """Test formatting numbers in millions."""
        assert format_large_number(1_500_000) == "1.50M"
        assert format_large_number(2_000_000) == "2.00M"

    def test_format_large_number_thousands(self):
        """Test formatting numbers in thousands."""
        assert format_large_number(1_500) == "1.50K"
        assert format_large_number(2_000) == "2.00K"

    def test_format_large_number_small_numbers(self):
        """Test formatting small numbers."""
        assert format_large_number(100) == "100"
        assert format_large_number(0) == "0"
        assert format_large_number(-500) == "-500"

    def test_format_large_number_negative(self):
        """Test formatting negative large numbers."""
        assert format_large_number(-1_500_000_000) == "-1.50B"
        assert format_large_number(-1_500_000) == "-1.50M"
        assert format_large_number(-1_500) == "-1.50K"


class TestFormatTable:
    """Test cases for format_table function."""

    def test_format_table_with_data(self):
        """Test formatting a table with data."""
        data = [{"Name": "Alice", "Age": 30}, {"Name": "Bob", "Age": 25}]
        result = format_table(data)
        lines = result.split("\n")
        assert len(lines) == 4  # Header, separator, 2 data rows
        assert "| Name            | Age             |" in lines
        assert "| Alice           | 30              |" in lines
        assert "| Bob             | 25              |" in lines

    def test_format_table_with_custom_headers(self):
        """Test formatting a table with custom headers."""
        data = [
            {"Name": "Alice", "Age": 30, "City": "NYC"},
            {"Name": "Bob", "Age": 25, "City": "LA"},
        ]
        headers = ["Name", "City"]
        result = format_table(data, headers=headers)
        lines = result.split("\n")
        assert len(lines) == 4  # Header, separator, 2 data rows
        assert "| Name            | City            |" in lines
        assert "| Alice           | NYC             |" in lines

    def test_format_table_empty_data(self):
        """Test formatting an empty table."""
        result = format_table([])
        assert result == "No data to display"

    def test_format_table_with_different_width(self):
        """Test formatting a table with custom column width."""
        data = [{"Name": "Alice", "Age": 30}]
        result = format_table(data, column_width=10)
        lines = result.split("\n")
        assert "| Name        | Age         |" in lines


class TestFormatMessageFunctions:
    """Test cases for message formatting functions."""

    def test_format_error(self):
        """Test error message formatting."""
        assert format_error("Something went wrong") == "[ERROR] Something went wrong"

    def test_format_warning(self):
        """Test warning message formatting."""
        assert format_warning("This is a warning") == "[WARNING] This is a warning"

    def test_format_info(self):
        """Test info message formatting."""
        assert format_info("This is info") == "[INFO] This is info"

    def test_format_success(self):
        """Test success message formatting."""
        assert format_success("Operation completed") == "[SUCCESS] Operation completed"


class TestFormatSystemInfo:
    """Test cases for format_system_info function."""

    @patch("metaexpert.cli.utils.formatters.psutil.Process")
    @patch("metaexpert.cli.utils.formatters.os.getpid")
    def test_format_system_info(self, mock_getpid, mock_process_class):
        """Test system info formatting."""
        # Mock the process and its methods
        mock_process = MagicMock()
        mock_process.cpu_percent.return_value = 10.5
        mock_process.memory_percent.return_value = 25.75
        mock_process.memory_info().rss = 10485760  # 100 MB in bytes
        mock_process.num_threads.return_value = 4
        mock_process.status.return_value = "running"

        mock_process_class.return_value = mock_process
        mock_getpid.return_value = 1234

        result = format_system_info()

        # Check that the result is a dictionary with expected keys
        assert isinstance(result, dict)
        assert "pid" in result
        assert "cpu_percent" in result
        assert "memory_percent" in result
        assert "memory_mb" in result
        assert "num_threads" in result
        assert "status" in result

        # Check values
        assert result["pid"] == 1234
        assert result["cpu_percent"] == "10.50%"
        assert result["memory_percent"] == "25.75%"
        assert result["memory_mb"] == "100.00 MB"
        assert result["num_threads"] == 4
        assert result["status"] == "running"


class TestFormatProcessStatus:
    """Test cases for format_process_status function."""

    @patch("metaexpert.cli.utils.formatters.format_system_info")
    def test_format_process_status(self, mock_format_system_info):
        """Test process status formatting."""
        mock_format_system_info.return_value = {
            "pid": 1234,
            "cpu_percent": "10.50%",
            "memory_percent": "25.75%",
            "memory_mb": "100.00 MB",
            "num_threads": 4,
            "status": "running",
        }

        result = format_process_status()

        # Check that the result contains expected information
        assert "PID: 1234" in result
        assert "CPU: 10.50%" in result
        assert "Memory: 25.75% (100.00 MB)" in result
        assert "Threads: 4" in result
        assert "Status: running" in result


class TestFormatDuration:
    """Test cases for format_duration function."""

    def test_format_duration_seconds(self):
        """Test formatting duration in seconds."""
        assert format_duration(30) == "30s"
        assert format_duration(59) == "59s"

    def test_format_duration_minutes(self):
        """Test formatting duration in minutes."""
        assert format_duration(60) == "1m"
        assert format_duration(120) == "2m"
        assert format_duration(150) == "2m 30s"  # 2 minutes and 30 seconds

    def test_format_duration_hours(self):
        """Test formatting duration in hours."""
        assert format_duration(3600) == "1h"
        assert format_duration(720) == "2h"
        assert format_duration(3661) == "1h 1m 1s"  # 1 hour, 1 minute, 1 second

    def test_format_duration_days(self):
        """Test formatting duration in days."""
        assert format_duration(86400) == "1d"
        assert format_duration(172800) == "2d"
        assert (
            format_duration(90061) == "1d 1h 1m 1s"
        )  # 1 day, 1 hour, 1 minute, 1 second

    def test_format_duration_zero(self):
        """Test formatting zero duration."""
        assert format_duration(0) == "0s"

    def test_format_duration_negative(self):
        """Test formatting negative duration."""
        assert format_duration(-10) == "Invalid duration"

    def test_format_duration_fractions(self):
        """Test formatting duration with fractional seconds."""
        assert format_duration(30.5) == "30s"
        assert format_duration(90.7) == "1m 30s"


class TestFormatBytes:
    """Test cases for format_bytes function."""

    def test_format_bytes_bytes(self):
        """Test formatting bytes in bytes."""
        assert format_bytes(512) == "512.00 B"
        assert format_bytes(1023) == "1023.00 B"

    def test_format_bytes_kb(self):
        """Test formatting bytes in KB."""
        assert format_bytes(1024) == "1.00 KB"
        assert format_bytes(2048) == "2.00 KB"
        assert format_bytes(1536) == "1.50 KB"

    def test_format_bytes_mb(self):
        """Test formatting bytes in MB."""
        assert format_bytes(1024 * 1024) == "1.00 MB"
        assert format_bytes(2 * 1024 * 1024) == "2.00 MB"
        assert format_bytes(1.5 * 1024 * 1024) == "1.50 MB"

    def test_format_bytes_gb(self):
        """Test formatting bytes in GB."""
        assert format_bytes(1024 * 1024 * 1024) == "1.00 GB"
        assert format_bytes(2 * 1024 * 1024 * 1024) == "2.00 GB"

    def test_format_bytes_tb(self):
        """Test formatting bytes in TB."""
        assert format_bytes(1024 * 1024 * 1024 * 1024) == "1.00 TB"

    def test_format_bytes_large(self):
        """Test formatting very large bytes."""
        assert format_bytes(1024**5) == "1024.00 TB"

    def test_format_bytes_float(self):
        """Test formatting float bytes values."""
        assert format_bytes(1024.5) == "1.00 KB"


class TestFormatBoolean:
    """Test cases for format_boolean function."""

    def test_format_boolean_true(self):
        """Test formatting True value."""
        assert format_boolean(True) == "Yes"

    def test_format_boolean_false(self):
        """Test formatting False value."""
        assert format_boolean(False) == "No"


class TestFormatList:
    """Test cases for format_list function."""

    def test_format_list_default_separator(self):
        """Test formatting list with default separator."""
        assert format_list(["apple", "banana", "cherry"]) == "apple, banana, cherry"

    def test_format_list_custom_separator(self):
        """Test formatting list with custom separator."""
        assert (
            format_list(["apple", "banana", "cherry"], " | ")
            == "apple | banana | cherry"
        )
        assert format_list([1, 2, 3], "-") == "1-2-3"

    def test_format_list_empty(self):
        """Test formatting empty list."""
        assert format_list([]) == ""

    def test_format_list_single_item(self):
        """Test formatting list with single item."""
        assert format_list(["single"]) == "single"

    def test_format_list_mixed_types(self):
        """Test formatting list with mixed types."""
        assert format_list([1, "text", 3.14, True]) == "1, text, 3.14, True"


class TestFormatKeyValuePairs:
    """Test cases for format_key_value_pairs function."""

    def test_format_key_value_pairs_simple(self):
        """Test formatting simple key-value pairs."""
        data = {"name": "John", "age": 30}
        result = format_key_value_pairs(data)
        lines = result.split("\n")
        assert "name: John" in lines
        assert "age: 30" in lines

    def test_format_key_value_pairs_nested(self):
        """Test formatting nested key-value pairs."""
        data = {
            "user": {"name": "John", "details": {"age": 30, "city": "NYC"}},
            "active": True,
        }
        result = format_key_value_pairs(data)

        lines = result.split("\n")
        assert "user:" in lines
        assert " name: John" in result  # Indented
        assert "  details:" in result  # Indented
        assert "    age: 30" in result  # More indented
        assert "    city: NYC" in result  # More indented
        assert "active: True" in lines

    def test_format_key_value_pairs_with_indent(self):
        """Test formatting with custom indent."""
        data = {"name": "John", "age": 30}
        result = format_key_value_pairs(data, indent=4)
        lines = result.split("\n")
        assert "    name: John" in lines
        assert "    age: 30" in lines

    def test_format_key_value_pairs_empty(self):
        """Test formatting empty dictionary."""
        result = format_key_value_pairs({})
        assert result == ""
