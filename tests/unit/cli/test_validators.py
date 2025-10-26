"""Tests for validator functions in src/metaexpert/cli/utils/validators.py"""

from unittest.mock import patch

import pytest
from src.metaexpert.cli.core.exceptions import ValidationError
from src.metaexpert.cli.utils.validators import (
    validate_date_format,
    validate_datetime_format,
    validate_directory_path,
    validate_exchange_name,
    validate_file_path,
    validate_numeric_range,
    validate_percentage,
    validate_positive_number,
    validate_project_name,
    validate_strategy_name,
    validate_symbol,
    validate_timeframe,
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
            "project_name_2023",
            "my-long-project-name-with-many-parts",
        ]

        for name in valid_names:
            if 3 <= len(name) <= 50:  # Ensure it's within length limits
                assert validate_project_name(name) is True

    def test_invalid_project_names_empty(self):
        """Test empty project name."""
        with pytest.raises(
            ValidationError, match="Project name must be a non-empty string"
        ):
            validate_project_name("")

    def test_invalid_project_names_none(self):
        """Test None project name."""
        with pytest.raises(
            ValidationError, match="Project name must be a non-empty string"
        ):
            validate_project_name(None)

    def test_invalid_project_names_not_string(self):
        """Test non-string project name."""
        with pytest.raises(
            ValidationError, match="Project name must be a non-empty string"
        ):
            validate_project_name(123)

    def test_invalid_project_names_too_short(self):
        """Test project names that are too short."""
        with pytest.raises(
            ValidationError, match="Project name must be at least 3 characters long"
        ):
            validate_project_name("ab")

        with pytest.raises(
            ValidationError, match="Project name must be at least 3 characters long"
        ):
            validate_project_name("a")

    def test_invalid_project_names_too_long(self):
        """Test project names that are too long."""
        long_name = "a" * 51
        with pytest.raises(
            ValidationError,
            match="Project name exceeds maximum length of 50 characters",
        ):
            validate_project_name(long_name)

    def test_invalid_project_names_start_with_number(self):
        """Test project names starting with a number."""
        with pytest.raises(
            ValidationError, match="Project name must start with a letter"
        ):
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
            with pytest.raises(
                ValidationError, match="Project name must start with a letter"
            ):
                validate_project_name(name)

    def test_invalid_project_names_start_with_hyphen(self):
        """Test project names starting with a hyphen."""
        with pytest.raises(
            ValidationError, match="Project name cannot start with underscore or hyphen"
        ):
            validate_project_name("-invalid")

    def test_invalid_project_names_start_with_underscore(self):
        """Test project names starting with an underscore."""
        with pytest.raises(
            ValidationError, match="Project name cannot start with underscore or hyphen"
        ):
            validate_project_name("_invalid")

    def test_invalid_project_names_end_with_hyphen(self):
        """Test project names ending with a hyphen."""
        with pytest.raises(
            ValidationError, match="Project name cannot end with underscore or hyphen"
        ):
            validate_project_name("invalid-")

    def test_invalid_project_names_end_with_underscore(self):
        """Test project names ending with an underscore."""
        with pytest.raises(
            ValidationError, match="Project name cannot end with underscore or hyphen"
        ):
            validate_project_name("invalid_")

    def test_custom_max_length(self):
        """Test custom max length."""
        # Should work with a longer max length
        assert validate_project_name("a" * 60, max_length=60) is True
        # Should fail with a shorter max length
        with pytest.raises(
            ValidationError,
            match="Project name exceeds maximum length of 10 characters",
        ):
            validate_project_name("a" * 20, max_length=10)


class TestValidateExchangeName:
    """Test cases for validate_exchange_name function."""

    def test_valid_exchanges(self):
        """Test valid exchange names."""
        valid_exchanges = ["binance", "bybit", "okx", "kucoin", "mexc", "bitget"]

        for exchange in valid_exchanges:
            assert validate_exchange_name(exchange) is True
            assert validate_exchange_name(exchange.upper()) is True  # Test uppercase
            assert (
                validate_exchange_name(exchange.capitalize()) is True
            )  # Test capitalized

    def test_invalid_exchanges(self):
        """Test invalid exchange names."""
        invalid_exchanges = [
            "nonexistent",
            "unknown",
            "invalid",
            "fake_exchange",
            "test_exchange",
        ]

        for exchange in invalid_exchanges:
            with pytest.raises(
                ValidationError, match=f"Invalid exchange name: '{exchange}'"
            ):
                validate_exchange_name(exchange)

    def test_empty_exchange_name(self):
        """Test empty exchange name."""
        with pytest.raises(
            ValidationError, match="Exchange name must be a non-empty string"
        ):
            validate_exchange_name("")

    def test_none_exchange_name(self):
        """Test None exchange name."""
        with pytest.raises(
            ValidationError, match="Exchange name must be a non-empty string"
        ):
            validate_exchange_name(None)

    def test_non_string_exchange_name(self):
        """Test non-string exchange name."""
        with pytest.raises(
            ValidationError, match="Exchange name must be a non-empty string"
        ):
            validate_exchange_name(123)


class TestValidateStrategyName:
    """Test cases for validate_strategy_name function."""

    def test_valid_strategies(self):
        """Test valid strategy names."""
        valid_strategies = ["template", "ema", "rsi", "macd", "bollinger", "custom"]

        for strategy in valid_strategies:
            assert validate_strategy_name(strategy) is True
            assert validate_strategy_name(strategy.upper()) is True
            assert validate_strategy_name(strategy.capitalize()) is True

    def test_invalid_strategies(self):
        """Test invalid strategy names."""
        invalid_strategies = ["", "a", "ab", "a" * 51]  # Too short, too long, empty

        for strategy in invalid_strategies:
            with pytest.raises(ValidationError):
                validate_strategy_name(strategy)

    def test_invalid_strategy_names_with_invalid_chars(self):
        """Test strategy names with invalid characters."""
        invalid_names = [
            "strategy.name",
            "strategy@name",
            "strategy name",  # space
            "strategy$name",
            "strategy!name",
            "strategy#name",
            "strategy%name",
            "strategy&name",
            "strategy*name",
            "strategy=name",
            "strategy+name",
            "strategy[name]",
            "strategy{name}",
            "strategy|name",
            "strategy\\name",
            "strategy/name",
            "strategy:name",
            "strategy;name",
            "strategy,name",
            "strategy<name>",
            "strategy>name",
        ]

        for name in invalid_names:
            with pytest.raises(
                ValidationError, match="Strategy name must start with a letter"
            ):
                validate_strategy_name(name)

    def test_strategy_names_starting_with_number(self):
        """Test strategy names starting with a number."""
        with pytest.raises(
            ValidationError, match="Strategy name must start with a letter"
        ):
            validate_strategy_name("123strategy")

    def test_empty_strategy_name(self):
        """Test empty strategy name."""
        with pytest.raises(
            ValidationError, match="Strategy name must be a non-empty string"
        ):
            validate_strategy_name("")

    def test_none_strategy_name(self):
        """Test None strategy name."""
        with pytest.raises(
            ValidationError, match="Strategy name must be a non-empty string"
        ):
            validate_strategy_name(None)

    def test_non_string_strategy_name(self):
        """Test non-string strategy name."""
        with pytest.raises(
            ValidationError, match="Strategy name must be a non-empty string"
        ):
            validate_strategy_name(123)


class TestValidateDateTimeFormat:
    """Test cases for validate_datetime_format function."""

    def test_valid_datetime_formats(self):
        """Test valid datetime formats."""
        valid_datetimes = [
            "2023-01-01 12:00:00",
            "2023-12-31 23:59:59",
            "199-06-15 00:00:00",
            "2024-02-29 12:30:45",  # Leap year
        ]

        for dt in valid_datetimes:
            assert validate_datetime_format(dt) is True

    def test_valid_custom_datetime_format(self):
        """Test valid datetime with custom format."""
        assert (
            validate_datetime_format(
                "2023/01/01 12:00:00", date_format="%Y/%m/%d %H:%M:%S"
            )
            is True
        )

    def test_invalid_datetime_formats(self):
        """Test invalid datetime formats."""
        invalid_datetimes = [
            "2023-1-1 12:00:00",  # Missing leading zeros
            "2023-01-1 12:00:00",  # Missing leading zero
            "23-01-01 12:00:00",  # Two-digit year
            "01-01-2023 12:00:00",  # Wrong order
            "2023-13-01 12:00:00",  # Invalid month
            "2023-01-32 12:00:00",  # Invalid day
            "2023-04-31 12:00:00",  # April has 30 days
            "2023-02-30 12:00:00",  # February has max 29 days
            "invalid_datetime",
            "",
            "2023-00-01 12:00:00",  # Invalid month
            "2023-01-00 12:00:00",  # Invalid day
            "2023-01-01",  # Incomplete format
        ]

        for dt in invalid_datetimes:
            with pytest.raises(ValidationError):
                validate_datetime_format(dt)

    def test_invalid_datetime_formats_custom_format(self):
        """Test invalid datetime with custom format."""
        with pytest.raises(ValidationError):
            validate_datetime_format(
                "2023-01-01 12:00:00", date_format="%Y/%m/%d %H:%M:%S"
            )

    def test_empty_datetime(self):
        """Test empty datetime."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_datetime_format("")

    def test_none_datetime(self):
        """Test None datetime."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_datetime_format(None)

    def test_non_string_datetime(self):
        """Test non-string datetime."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_datetime_format(123)


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
            assert validate_date_format(date) is True

    def test_valid_custom_date_format(self):
        """Test valid date with custom format."""
        assert validate_date_format("2023/01/01", date_format="%Y/%m/%d") is True

    def test_invalid_date_formats(self):
        """Test invalid date formats."""
        invalid_dates = [
            "2023-1-1",  # Missing leading zeros
            "2023-01-1",  # Missing leading zero
            "23-01-01",  # Two-digit year
            "01-01-2023",  # Wrong order
            "2023-13-01",  # Invalid month
            "2023-01-32",  # Invalid day
            "2023-04-31",  # April has 30 days
            "2023-02-30",  # February has max 29 days
            "invalid_date",
            "",
            "2023-00-01",  # Invalid month
            "2023-01-00",  # Invalid day
            "2023-01",  # Incomplete format
            "2023",  # Incomplete format
            "2023-01-01-01",  # Too many parts
        ]

        for date in invalid_dates:
            with pytest.raises(ValidationError):
                validate_date_format(date)

    def test_invalid_date_formats_custom_format(self):
        """Test invalid date with custom format."""
        with pytest.raises(ValidationError):
            validate_date_format("2023-01-01", date_format="%Y/%m/%d")

    def test_empty_date(self):
        """Test empty date."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_date_format("")

    def test_none_date(self):
        """Test None date."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_date_format(None)

    def test_non_string_date(self):
        """Test non-string date."""
        with pytest.raises(ValidationError, match="Date must be a non-empty string"):
            validate_date_format(123)


class TestValidatePositiveNumber:
    """Test cases for validate_positive_number function."""

    def test_positive_numbers(self):
        """Test positive numbers."""
        positive_values = [1, 1.0, 0.1, 100, 99.99, 0.001, "1", "1.5", "100.0"]

        for value in positive_values:
            assert validate_positive_number(value) is True

    def test_zero_and_negative_numbers(self):
        """Test zero and negative numbers."""
        non_positive_values = [0, -1, -0.1, -100, "-1", "-1.5", "0", "0.0"]

        for value in non_positive_values:
            with pytest.raises(
                ValidationError, match="Value must be a positive number"
            ):
                validate_positive_number(value)

    def test_invalid_types(self):
        """Test invalid types."""
        invalid_values = [
            "abc",
            "not_a_number",
            "",
            " ",
            "1.2.3",
            "1,2",
            "inf",
            "-inf",
            "nan",
        ]

        for value in invalid_values:
            with pytest.raises(ValidationError, match="Value must be a number"):
                validate_positive_number(value)

    def test_none_value(self):
        """Test None value."""
        with pytest.raises(ValidationError, match="Value must be a number"):
            validate_positive_number(None)


class TestValidateNumericRange:
    """Test cases for validate_numeric_range function."""

    def test_valid_range_values(self):
        """Test valid values within range."""
        # Test within range
        assert validate_numeric_range(5, min_val=1, max_val=10) is True
        assert validate_numeric_range(1, min_val=1, max_val=10) is True  # At min
        assert validate_numeric_range(10, min_val=1, max_val=10) is True  # At max

        # Test with floats
        assert validate_numeric_range(5.5, min_val=1.0, max_val=10.0) is True
        assert validate_numeric_range(1.0, min_val=1.0, max_val=10.0) is True  # At min
        assert validate_numeric_range(10.0, min_val=1.0, max_val=10.0) is True  # At max

        # Test with strings that convert to numbers
        assert validate_numeric_range("5", min_val=1, max_val=10) is True

    def test_out_of_range_values(self):
        """Test values outside range."""
        # Test below min
        with pytest.raises(ValidationError, match="is less than minimum allowed value"):
            validate_numeric_range(0, min_val=1, max_val=10)

        # Test above max
        with pytest.raises(
            ValidationError, match="is greater than maximum allowed value"
        ):
            validate_numeric_range(11, min_val=1, max_val=10)

        # Test with floats
        with pytest.raises(ValidationError, match="is less than minimum allowed value"):
            validate_numeric_range(0.5, min_val=1.0, max_val=10.0)

        with pytest.raises(
            ValidationError, match="is greater than maximum allowed value"
        ):
            validate_numeric_range(10.5, min_val=1.0, max_val=10.0)

    def test_partial_range_constraints(self):
        """Test with only min or max constraint."""
        # Only min constraint
        assert validate_numeric_range(5, min_val=1) is True
        with pytest.raises(ValidationError, match="is less than minimum allowed value"):
            validate_numeric_range(0, min_val=1)

        # Only max constraint
        assert validate_numeric_range(5, max_val=10) is True
        with pytest.raises(
            ValidationError, match="is greater than maximum allowed value"
        ):
            validate_numeric_range(11, max_val=10)

    def test_invalid_types(self):
        """Test invalid types."""
        invalid_values = [
            "abc",
            "not_a_number",
            "",
            " ",
            "1.2.3",
            "1,2",
            "inf",
            "-inf",
            "nan",
        ]

        for value in invalid_values:
            with pytest.raises(ValidationError, match="Value must be a number"):
                validate_numeric_range(value, min_val=1, max_val=10)

    def test_none_value(self):
        """Test None value."""
        with pytest.raises(ValidationError, match="Value must be a number"):
            validate_numeric_range(None, min_val=1, max_val=10)


class TestValidatePercentage:
    """Test cases for validate_percentage function."""

    def test_valid_percentages(self):
        """Test valid percentage values."""
        valid_percentages = [0, 1, 50, 99, 100, 0.0, 50.5, 100.0, "0", "50", "100"]

        for value in valid_percentages:
            assert validate_percentage(value) is True

    def test_invalid_percentages(self):
        """Test invalid percentage values."""
        # Below 0
        with pytest.raises(ValidationError, match="is less than minimum allowed value"):
            validate_percentage(-1)

        with pytest.raises(ValidationError, match="is less than minimum allowed value"):
            validate_percentage(-0.1)

        # Above 100
        with pytest.raises(
            ValidationError, match="is greater than maximum allowed value"
        ):
            validate_percentage(101)

        with pytest.raises(
            ValidationError, match="is greater than maximum allowed value"
        ):
            validate_percentage(150.5)

    def test_invalid_types(self):
        """Test invalid types."""
        invalid_values = [
            "abc",
            "not_a_number",
            "",
            " ",
            "1.2.3",
            "1,2",
            "inf",
            "-inf",
            "nan",
        ]

        for value in invalid_values:
            with pytest.raises(ValidationError, match="Value must be a number"):
                validate_percentage(value)


class TestValidateFilePath:
    """Test cases for validate_file_path function."""

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.is_file")
    def test_valid_file_path_exists_and_is_file(
        self, mock_is_file, mock_is_dir, mock_exists
    ):
        """Test valid file path that exists and is a file."""
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_is_dir.return_value = False

        result = validate_file_path(
            "existing_file.txt", must_exist=True, must_be_file=True
        )
        assert result is True

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.is_file")
    def test_valid_file_path_exists_and_is_dir(
        self, mock_is_file, mock_is_dir, mock_exists
    ):
        """Test valid directory path that exists and is a directory."""
        mock_exists.return_value = True
        mock_is_file.return_value = False
        mock_is_dir.return_value = True

        result = validate_file_path("existing_dir", must_exist=True, must_be_file=False)
        assert result is True

    @patch("pathlib.Path.exists")
    def test_non_existing_path_with_must_exist_true(self, mock_exists):
        """Test non-existing path with must_exist=True."""
        mock_exists.return_value = False

        with pytest.raises(ValidationError, match="Path does not exist"):
            validate_file_path("non_existing_path", must_exist=True)

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    def test_existing_path_is_dir_but_expected_file(self, mock_is_dir, mock_exists):
        """Test path exists as directory but expected file."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        with pytest.raises(
            ValidationError, match="Path exists but is a directory, expected file"
        ):
            validate_file_path("existing_dir", must_exist=True, must_be_file=True)

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_file")
    def test_existing_path_is_file_but_expected_dir(self, mock_is_file, mock_exists):
        """Test path exists as file but expected directory."""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        with pytest.raises(
            ValidationError, match="Path exists but is a file, expected directory"
        ):
            validate_file_path("existing_file.txt", must_exist=True, must_be_file=False)

    def test_empty_path(self):
        """Test empty path."""
        with pytest.raises(ValidationError, match="Path must be a non-empty string"):
            validate_file_path("")

    def test_none_path(self):
        """Test None path."""
        with pytest.raises(ValidationError, match="Path must be a non-empty string"):
            validate_file_path(None)

    def test_non_string_path(self):
        """Test non-string path."""
        with pytest.raises(ValidationError, match="Path must be a non-empty string"):
            validate_file_path(123)

    def test_path_with_invalid_characters(self):
        """Test path with invalid characters."""
        invalid_chars = '<>:"|?*'

        for char in invalid_chars:
            path_with_char = f"test{char}path"
            with pytest.raises(
                ValidationError,
                match=f"Path contains invalid characters: {invalid_chars}",
            ):
                validate_file_path(path_with_char)

    def test_path_with_directory_traversal(self):
        """Test path with directory traversal."""
        with pytest.raises(ValidationError, match="Path contains directory traversal"):
            validate_file_path("../unsafe_path")

        with pytest.raises(ValidationError, match="Path contains directory traversal"):
            validate_file_path("subfolder/../../unsafe_path")


class TestValidateDirectoryPath:
    """Test cases for validate_directory_path function."""

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    def test_valid_directory_path_exists(self, mock_is_dir, mock_exists):
        """Test valid directory path that exists."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        result = validate_directory_path("existing_dir", must_exist=True)
        assert result is True

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_file")
    def test_directory_path_exists_as_file(self, mock_is_file, mock_exists):
        """Test path exists as file but expected directory."""
        mock_exists.return_value = True
        mock_is_file.return_value = True

        with pytest.raises(
            ValidationError, match="Path exists but is a file, expected directory"
        ):
            validate_directory_path("existing_file.txt", must_exist=True)

    @patch("pathlib.Path.exists")
    def test_non_existing_directory_path_with_must_exist_true(self, mock_exists):
        """Test non-existing directory path with must_exist=True."""
        mock_exists.return_value = False

        with pytest.raises(ValidationError, match="Path does not exist"):
            validate_directory_path("non_existing_dir", must_exist=True)

    def test_empty_directory_path(self):
        """Test empty directory path."""
        with pytest.raises(ValidationError, match="Path must be a non-empty string"):
            validate_directory_path("")

    def test_none_directory_path(self):
        """Test None directory path."""
        with pytest.raises(ValidationError, match="Path must be a non-empty string"):
            validate_directory_path(None)


class TestValidateTimeframe:
    """Test cases for validate_timeframe function."""

    def test_valid_timeframes(self):
        """Test valid timeframe formats."""
        valid_timeframes = [
            "1s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "4h",
            "1d",
            "3d",
            "1w",
            "2w",
            "1M",
            "3M",
        ]

        for tf in valid_timeframes:
            assert validate_timeframe(tf) is True

    def test_invalid_timeframes(self):
        """Test invalid timeframe formats."""
        invalid_timeframes = [
            "",  # Empty string
            "1",  # Missing unit
            "s",  # Missing number
            "0s",  # Zero value
            "-1m",  # Negative value
            "1x",  # Invalid unit
            "1mm",  # Double unit
            "1ss",  # Double unit
            "abc",  # Completely invalid
            "1h1m",  # Multiple units
        ]

        for tf in invalid_timeframes:
            with pytest.raises(ValidationError):
                validate_timeframe(tf)

    def test_empty_timeframe(self):
        """Test empty timeframe."""
        with pytest.raises(
            ValidationError, match="Timeframe must be a non-empty string"
        ):
            validate_timeframe("")

    def test_none_timeframe(self):
        """Test None timeframe."""
        with pytest.raises(
            ValidationError, match="Timeframe must be a non-empty string"
        ):
            validate_timeframe(None)

    def test_non_string_timeframe(self):
        """Test non-string timeframe."""
        with pytest.raises(
            ValidationError, match="Timeframe must be a non-empty string"
        ):
            validate_timeframe(123)


class TestValidateSymbol:
    """Test cases for validate_symbol function."""

    def test_valid_symbols(self):
        """Test valid symbol formats."""
        valid_symbols = [
            "BTCUSDT",  # Standard format
            "ETHUSDT",  # Standard format
            "BTC-USDT",  # With hyphen
            "ETH/USDT",  # With slash
            "XRPUSDC",  # Different quote currency
            "BTCBUSD",  # BUSD as quote
            "AAPL",  # Just one currency (though unusual)
            "BTC123",  # With numbers
        ]

        for symbol in valid_symbols:
            assert validate_symbol(symbol) is True

    def test_invalid_symbols(self):
        """Test invalid symbol formats."""
        invalid_symbols = [
            "",  # Empty string
            "BTC",  # Too short
            "BTC USDT",  # With space
            "BTC@USDT",  # With special character
            "BTC#USDT",  # With special character
            "BTC$USDT",  # With special character
            "BTC%USDT",  # With special character
            "BTC&USDT",  # With special character
            "BTC*USDT",  # With special character
            "BTC=USDT",  # With special character
            "BTC+USDT",  # With special character
            "BTC[USDT]",  # With brackets
            "BTC{USDT}",  # With braces
            "BTC|USDT",  # With pipe
            "BTC\\USDT",  # With backslash
            "BTC:USDT",  # With colon
            "BTC;USDT",  # With semicolon
            "BTC,USDT",  # With comma
            "BTC<USDT>",  # With angle brackets
        ]

        for symbol in invalid_symbols:
            with pytest.raises(ValidationError):
                validate_symbol(symbol)

    def test_empty_symbol(self):
        """Test empty symbol."""
        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            validate_symbol("")

    def test_none_symbol(self):
        """Test None symbol."""
        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            validate_symbol(None)

    def test_non_string_symbol(self):
        """Test non-string symbol."""
        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            validate_symbol(123)
