"""Tests for validator functions in src/metaexpert/cli/utils/validators.py"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from metaexpert.cli.utils.validators import (
    validate_project_name,
    validate_exchange,
    validate_date_format,
    validate_path_exists,
    validate_positive_number,
    validate_strategy,
    validate_market_type
)


class TestValidateProjectName:
    """Test cases for validate_project_name function."""

    def test_valid_project_names(self):
        """Test valid project names."""
        valid_names = [
            "my_project",
            "project123",
            "test-project",
            "Test_Project_123",
            "a_b_c",
            "project_name_2023",
            "my-long-project-name-with-many-parts",
            "_" * 3 + "valid_name",  # Starts with underscore
            "valid_name" + "_" * 3,  # Ends with underscore
        ]
        
        for name in valid_names:
            if len(name) <= 50:  # Ensure it's within length limits
                validate_project_name(name)

    def test_invalid_project_names_empty(self):
        """Test empty project name."""
        with pytest.raises(ValueError, match="Project name must be at least 3 characters long"):
            validate_project_name("")

    def test_invalid_project_names_too_short(self):
        """Test project names that are too short."""
        with pytest.raises(ValueError, match="Project name must be at least 3 characters long"):
            validate_project_name("ab")
        
        with pytest.raises(ValueError, match="Project name must be at least 3 characters long"):
            validate_project_name("a")

    def test_invalid_project_names_too_long(self):
        """Test project names that are too long."""
        long_name = "a" * 51
        with pytest.raises(ValueError, match="Project name must not exceed 50 characters"):
            validate_project_name(long_name)

    def test_invalid_project_names_start_with_number(self):
        """Test project names starting with a number."""
        with pytest.raises(ValueError, match="Project name must start with a letter or underscore"):
            validate_project_name("123project")

    def test_invalid_project_names_with_invalid_chars(self):
        """Test project names with invalid characters."""
        invalid_names = [
            "project.name",
            "project@name",
            "project name",  # space
            "project$name",
            "project!name",
            "project#name",
            "project%name",
            "project&name",
            "project*name",
            "project=name",
            "project+name",
            "project[name]",
            "project{name}",
            "project|name",
            "project\\name",
            "project/name",
            "project:name",
            "project;name",
            "project,name",
            "project<name>",
            "project>name",
        ]
        
        for name in invalid_names:
            with pytest.raises(ValueError, match="Project name must start with a letter or underscore"):
                validate_project_name(name)

    def test_invalid_project_names_start_with_hyphen(self):
        """Test project names starting with a hyphen."""
        with pytest.raises(ValueError, match="Project name must start with a letter or underscore"):
            validate_project_name("-invalid")

    def test_python_keywords(self):
        """Test Python keywords as project names."""
        keywords = ["class", "def", "for", "while", "if", "else", "import", "from", "as", "try", "except", "finally", "with", "lambda", "yield", "async", "await"]
        
        for keyword in keywords:
            with pytest.raises(ValueError, match=f"'{keyword}' is a Python keyword and cannot be used"):
                validate_project_name(keyword)

    def test_reserved_names(self):
        """Test reserved names."""
        reserved = ["test", "tests", "src", "lib", "bin", "build", "dist"]
        
        for name in reserved:
            with pytest.raises(ValueError, match=f"'{name}' is a reserved name"):
                validate_project_name(name)


class TestValidateExchange:
    """Test cases for validate_exchange function."""

    def test_valid_exchanges(self):
        """Test valid exchange names."""
        valid_exchanges = ["binance", "bybit", "okx", "mexc", "kucoin", "bitget"]
        
        for exchange in valid_exchanges:
            validate_exchange(exchange)
            validate_exchange(exchange.upper())  # Test uppercase
            validate_exchange(exchange.capitalize())  # Test capitalized

    def test_invalid_exchanges(self):
        """Test invalid exchange names."""
        invalid_exchanges = ["nonexistent", "unknown", "invalid", "fake_exchange", "test_exchange"]
        
        for exchange in invalid_exchanges:
            with pytest.raises(ValueError, match=f"Unsupported exchange: {exchange}"):
                validate_exchange(exchange)


class TestValidateStrategy:
    """Test cases for validate_strategy function."""

    def test_valid_strategies(self):
        """Test valid strategy names."""
        valid_strategies = ["template", "ema", "rsi", "macd", "bollinger", "custom"]
        
        for strategy in valid_strategies:
            validate_strategy(strategy)
            validate_strategy(strategy.upper())
            validate_strategy(strategy.capitalize())

    def test_invalid_strategies(self):
        """Test invalid strategy names."""
        invalid_strategies = ["nonexistent", "unknown", "invalid", "fake_strategy", "test_strategy"]
        
        for strategy in invalid_strategies:
            with pytest.raises(ValueError, match=f"Unknown strategy: {strategy}"):
                validate_strategy(strategy)


class TestValidateMarketType:
    """Test cases for validate_market_type function."""

    def test_valid_market_types(self):
        """Test valid market types."""
        valid_market_types = ["spot", "futures", "options"]
        
        for market_type in valid_market_types:
            validate_market_type(market_type)
            validate_market_type(market_type.upper())
            validate_market_type(market_type.capitalize())

    def test_invalid_market_types(self):
        """Test invalid market types."""
        invalid_market_types = ["invalid", "unknown", "spot_futures", "forex", "stocks"]
        
        for market_type in invalid_market_types:
            with pytest.raises(ValueError, match=f"Invalid market type: {market_type}"):
                validate_market_type(market_type)


class TestValidateDateFormat:
    """Test cases for validate_date_format function."""

    def test_valid_date_formats(self):
        """Test valid date formats."""
        valid_dates = [
            "2023-01-01",
            "2023-12-31",
            "2000-02-29",  # Leap year
            "2021-02-28",  # Non-leap year
            "1999-06-15",
        ]
        
        for date in valid_dates:
            validate_date_format(date)

    def test_invalid_date_formats(self):
        """Test invalid date formats."""
        invalid_dates = [
            "2023-1-1",      # Missing leading zeros
            "2023-01-1",     # Missing leading zero
            "23-01-01",      # Two-digit year
            "2023/01/01",    # Wrong separator
            "01-01-2023",    # Wrong order
            "2023-13-01",    # Invalid month
            "2023-01-32",    # Invalid day
            "2023-04-31",    # April has 30 days
            "2023-02-30",    # February has max 29 days
            "invalid_date",
            "",
            "2023-00-01",    # Invalid month
            "2023-01-00",    # Invalid day
            "2023-01",       # Incomplete format
            "2023",          # Incomplete format
            "2023-01-01-01", # Too many parts
        ]
        
        for date in invalid_dates:
            with pytest.raises(ValueError):
                validate_date_format(date)

    def test_invalid_dates_that_exist_but_not_valid(self):
        """Test dates that are not valid in calendar terms."""
        invalid_dates = [
            "2023-02-29",  # 2023 is not a leap year
            "2023-04-31",  # April has 30 days
            "2023-06-31",  # June has 30 days
            "2023-09-31",  # September has 30 days
            "2023-11-31",  # November has 30 days
        ]
        
        for date in invalid_dates:
            with pytest.raises(ValueError):
                validate_date_format(date)


class TestValidatePathExists:
    """Test cases for validate_path_exists function."""

    @patch('pathlib.Path.exists')
    def test_existing_path(self, mock_exists):
        """Test existing path."""
        mock_exists.return_value = True
        path = Path("existing/path")
        validate_path_exists(path)

    @patch('pathlib.Path.exists')
    def test_non_existing_path(self, mock_exists):
        """Test non-existing path."""
        mock_exists.return_value = False
        path = Path("non/existing/path")
        
        with pytest.raises(ValueError, match="Path not found: non/existing/path"):
            validate_path_exists(path)

    @patch('pathlib.Path.exists')
    def test_existing_path_with_custom_file_type(self, mock_exists):
        """Test existing path with custom file type."""
        mock_exists.return_value = True
        path = Path("existing/path")
        validate_path_exists(path, "directory")

    @patch('pathlib.Path.exists')
    def test_non_existing_path_with_custom_file_type(self, mock_exists):
        """Test non-existing path with custom file type."""
        mock_exists.return_value = False
        path = Path("non/existing/path")
        
        with pytest.raises(ValueError, match="Directory not found: non/existing/path"):
            validate_path_exists(path, "directory")


class TestValidatePositiveNumber:
    """Test cases for validate_positive_number function."""

    def test_positive_numbers(self):
        """Test positive numbers."""
        positive_values = [1, 1.0, 0.1, 100, 99.99, 0.001, "1", "1.5", "100.0"]
        
        for value in positive_values:
            validate_positive_number(value)

    def test_zero_and_negative_numbers(self):
        """Test zero and negative numbers."""
        non_positive_values = [0, -1, -0.1, -100, "-1", "-1.5", "0", "0.0"]
        
        for value in non_positive_values:
            with pytest.raises(ValueError, match="value must be positive"):
                validate_positive_number(value)

    def test_invalid_types(self):
        """Test invalid types."""
        invalid_values = ["abc", "not_a_number", "", " ", "1.2.3", "1,2", "inf", "-inf", "nan"]
        
        for value in invalid_values:
            with pytest.raises(ValueError, match="Invalid value"):
                validate_positive_number(value)

    def test_custom_name(self):
        """Test with custom name."""
        with pytest.raises(ValueError, match="amount must be positive"):
            validate_positive_number(-5, "amount")