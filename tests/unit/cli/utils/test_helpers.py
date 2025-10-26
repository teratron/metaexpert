"""Tests for helper functions in src/metaexpert/cli/utils/helpers.py"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import yaml

from metaexpert.cli.utils.helpers import (
    clear_directory,
    convert_to_bool,
    convert_to_type,
    dict_to_pydantic,
    ensure_directory_exists,
    format_bytes,
    get_config_file_path,
    get_env_var,
    get_file_size,
    is_valid_path,
    merge_dicts,
    safe_json_load,
    safe_yaml_load,
    truncate_string,
    validate_pydantic_model,
)


class TestGetConfigFilePath:
    """Test cases for get_config_file_path function."""

    @patch("metaexpert.cli.utils.helpers.Path.home")
    def test_get_config_file_path(self, mock_home):
        """Test getting config file path."""
        mock_home.return_value = Path("/home/user")

        result = get_config_file_path()

        expected = Path("/home/user/.metaexpert/config.yaml")
        assert result == expected


class TestEnsureDirectoryExists:
    """Test cases for ensure_directory_exists function."""

    def test_ensure_directory_exists_string_path(self):
        """Test ensuring directory exists with string path."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            path = "/test/path"
            result = ensure_directory_exists(path)

            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            assert str(result) == path

    def test_ensure_directory_exists_path_object(self):
        """Test ensuring directory exists with Path object."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            path = Path("/test/path")
            result = ensure_directory_exists(path)

            mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
            assert result == path


class TestClearDirectory:
    """Test cases for clear_directory function."""

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    @patch("pathlib.Path.iterdir")
    def test_clear_directory_exists_and_is_dir(
        self, mock_iterdir, mock_is_dir, mock_exists
    ):
        """Test clearing directory that exists and is a directory."""
        mock_exists.return_value = True
        mock_is_dir.return_value = True

        mock_file = MagicMock()
        mock_file.is_file.return_value = True
        mock_file.is_dir.return_value = False
        mock_file.match.return_value = False

        mock_iterdir.return_value = [mock_file]

        clear_directory("/test/dir")

        mock_file.unlink.assert_called_once()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    def test_clear_directory_not_exists(self, mock_is_dir, mock_exists):
        """Test clearing directory that doesn't exist."""
        mock_exists.return_value = False

        # This should not raise an exception
        clear_directory("/nonexistent/dir")

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.is_dir")
    def test_clear_directory_exists_but_not_dir(self, mock_is_dir, mock_exists):
        """Test clearing path that exists but is not a directory."""
        mock_exists.return_value = True
        mock_is_dir.return_value = False

        # This should not raise an exception
        clear_directory("/not/a/dir")


class TestSafeJsonLoad:
    """Test cases for safe_json_load function."""

    def test_safe_json_load_valid_file(self):
        """Test loading valid JSON file."""
        mock_data = {"name": "test", "value": 123}
        json_content = json.dumps(mock_data)

        with patch("builtins.open", mock_open(read_data=json_content)):
            result = safe_json_load("/test/file.json")
            assert result == mock_data

    def test_safe_json_load_file_not_found(self):
        """Test loading non-existent JSON file."""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = safe_json_load("/nonexistent/file.json")
            assert result is None

    def test_safe_json_load_invalid_json(self):
        """Test loading invalid JSON file."""
        with patch("builtins.open", mock_open(read_data="invalid json content")):
            result = safe_json_load("/invalid/file.json")
            assert result is None


class TestSafeYamlLoad:
    """Test cases for safe_yaml_load function."""

    def test_safe_yaml_load_valid_file(self):
        """Test loading valid YAML file."""
        mock_data = {"name": "test", "value": 123}
        yaml_content = yaml.dump(mock_data)

        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = safe_yaml_load("/test/file.yaml")
            assert result == mock_data

    def test_safe_yaml_load_file_not_found(self):
        """Test loading non-existent YAML file."""
        with patch("builtins.open", side_effect=FileNotFoundError()):
            result = safe_yaml_load("/nonexistent/file.yaml")
            assert result is None

    def test_safe_yaml_load_invalid_yaml(self):
        """Test loading invalid YAML file."""
        with patch("builtins.open", mock_open(read_data="invalid: yaml: content: [")):
            result = safe_yaml_load("/invalid/file.yaml")
            assert result is None


class TestConvertToBool:
    """Test cases for convert_to_bool function."""

    def test_convert_to_bool_true_values(self):
        """Test converting various true-like values."""
        true_values = [
            True,
            1,
            "true",
            "True",
            "TRUE",
            "1",
            "yes",
            "Yes",
            "YES",
            "on",
            "ON",
            "y",
            "Y",
            "t",
            "T",
        ]

        for value in true_values:
            assert convert_to_bool(value) is True

    def test_convert_to_bool_false_values(self):
        """Test converting various false-like values."""
        false_values = [
            False,
            0,
            "false",
            "False",
            "FALSE",
            "0",
            "no",
            "No",
            "NO",
            "off",
            "OFF",
            "n",
            "N",
            "f",
            "F",
            "",
            "invalid",
        ]

        for value in false_values:
            assert convert_to_bool(value) is False

    def test_convert_to_bool_with_int(self):
        """Test converting integer values."""
        assert convert_to_bool(1) is True
        assert convert_to_bool(0) is False
        assert convert_to_bool(5) is True  # Non-zero integers are True


class TestConvertToType:
    """Test cases for convert_to_type function."""

    def test_convert_to_type_bool(self):
        """Test converting to boolean."""
        assert convert_to_type("true", bool) is True
        assert convert_to_type("false", bool) is False
        assert convert_to_type(1, bool) is True
        assert convert_to_type(0, bool) is False

    def test_convert_to_type_int(self):
        """Test converting to integer."""
        assert convert_to_type("123", int) == 123
        assert convert_to_type(45.6, int) == 45
        assert convert_to_type("invalid", int) == 0  # Default fallback

    def test_convert_to_type_float(self):
        """Test converting to float."""
        assert convert_to_type("123.45", float) == 123.45
        assert convert_to_type("123", float) == 123.0
        assert convert_to_type("invalid", float) == 0.0  # Default fallback

    def test_convert_to_type_str(self):
        """Test converting to string."""
        assert convert_to_type(123, str) == "123"
        assert convert_to_type(45.6, str) == "45.6"
        assert convert_to_type(True, str) == "True"

    def test_convert_to_type_list(self):
        """Test converting to list."""
        assert convert_to_type("a,b,c", list) == ["a", "b", "c"]
        assert convert_to_type([1, 2, 3], list) == [1, 2, 3]
        assert convert_to_type("x, y, z", list) == ["x", "y", "z"]  # With spaces

    def test_convert_to_type_dict(self):
        """Test converting to dictionary."""
        json_str = '{"name": "test", "value": 123}'
        expected = {"name": "test", "value": 123}
        assert convert_to_type(json_str, dict) == expected

        assert convert_to_type({"a": 1, "b": 2}, dict) == {"a": 1, "b": 2}

        # Invalid JSON should return empty dict
        assert convert_to_type("invalid json", dict) == {}

    def test_convert_to_type_none(self):
        """Test converting None value."""
        assert convert_to_type(None, str) is None
        assert convert_to_type(None, int) is None
        assert convert_to_type(None, bool) is None


class TestGetEnvVar:
    """Test cases for get_env_var function."""

    def test_get_env_var_exists(self):
        """Test getting existing environment variable."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            result = get_env_var("TEST_VAR")
            assert result == "test_value"

    def test_get_env_var_not_exists_with_default(self):
        """Test getting non-existing environment variable with default."""
        result = get_env_var("NONEXISTENT_VAR", "default_value")
        assert result == "default_value"

    def test_get_env_var_not_exists_without_default(self):
        """Test getting non-existing environment variable without default."""
        result = get_env_var("NONEXISTENT_VAR")
        assert result is None


class TestFormatBytes:
    """Test cases for format_bytes function."""

    def test_format_bytes_bytes(self):
        """Test formatting bytes in bytes."""
        assert format_bytes(512) == "512.00 B"
        assert format_bytes(1023) == "1023.00 B"

    def test_format_bytes_kb(self):
        """Test formatting bytes in KB."""
        assert format_bytes(1024) == "1.0 KB"
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
        assert format_bytes(1024.5) == "1.0 KB"


class TestIsValidPath:
    """Test cases for is_valid_path function."""

    def test_is_valid_path_valid(self):
        """Test with valid path."""
        # Using a path that should be valid on most systems
        assert is_valid_path(".") is True  # Current directory
        assert is_valid_path("/") is True  # Root directory (on Unix-like systems)

    def test_is_valid_path_invalid(self):
        """Test with invalid path."""
        # Testing with a path that contains invalid characters (this may vary by OS)
        # On Windows, this would be invalid, on Unix it might be valid
        # Let's use a path that's likely to be invalid
        invalid_path = "invalid\0path"  # null byte in path
        assert is_valid_path(invalid_path) is False


class TestGetFileSize:
    """Test cases for get_file_size function."""

    def test_get_file_size_exists(self):
        """Test getting size of existing file."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name

        try:
            size = get_file_size(tmp_path)
            assert size == 12  # Length of "test content"
        finally:
            os.unlink(tmp_path)

    def test_get_file_size_not_exists(self):
        """Test getting size of non-existing file."""
        assert get_file_size("/nonexistent/file.txt") == -1

    def test_get_file_size_directory(self):
        """Test getting size of directory."""
        # Using current directory which exists but is not a file
        assert get_file_size(".") == -1


class TestMergeDicts:
    """Test cases for merge_dicts function."""

    def test_merge_dicts_simple(self):
        """Test merging simple dictionaries."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        result = merge_dicts(base, override)

        assert result == {"a": 1, "b": 3, "c": 4}

    def test_merge_dicts_nested(self):
        """Test merging nested dictionaries."""
        base = {"a": 1, "nested": {"x": 1, "y": 2}}
        override = {"nested": {"y": 3, "z": 4}, "b": 2}
        result = merge_dicts(base, override)

        expected = {"a": 1, "nested": {"x": 1, "y": 3, "z": 4}, "b": 2}
        assert result == expected

    def test_merge_dicts_override_with_non_dict(self):
        """Test overriding dict with non-dict value."""
        base = {"nested": {"x": 1, "y": 2}}
        override = {"nested": "not_a_dict"}
        result = merge_dicts(base, override)

        assert result == {"nested": "not_a_dict"}

    def test_merge_dicts_empty_base(self):
        """Test merging with empty base dictionary."""
        base = {}
        override = {"a": 1, "b": 2}
        result = merge_dicts(base, override)

        assert result == {"a": 1, "b": 2}

    def test_merge_dicts_empty_override(self):
        """Test merging with empty override dictionary."""
        base = {"a": 1, "b": 2}
        override = {}
        result = merge_dicts(base, override)

        assert result == {"a": 1, "b": 2}


class TestTruncateString:
    """Test cases for truncate_string function."""

    def test_truncate_string_shorter_than_max(self):
        """Test string shorter than max length."""
        text = "short"
        result = truncate_string(text, 10)
        assert result == "short"

    def test_truncate_string_exact_length(self):
        """Test string exactly at max length."""
        text = "exactlength"
        result = truncate_string(text, 11)
        assert result == "exactlength"

    def test_truncate_string_longer_than_max(self):
        """Test string longer than max length."""
        text = "this is a very long string"
        result = truncate_string(text, 10)
        assert result == "this i..."  # Default suffix

    def test_truncate_string_custom_suffix(self):
        """Test string truncation with custom suffix."""
        text = "this is a very long string"
        result = truncate_string(text, 15, " [truncated]")
        assert result == "this is a [truncated]"

    def test_truncate_string_max_length_less_than_suffix(self):
        """Test when max length is less than suffix length."""
        text = "very long string"
        result = truncate_string(text, 2, "...")
        # Should return just the suffix since there's no room for content
        assert result == "..."


class TestValidatePydanticModel:
    """Test cases for validate_pydantic_model function."""

    def test_validate_pydantic_model_valid(self):
        """Test validating data against a Pydantic model with valid data."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            age: int

        valid_data = {"name": "John", "age": 30}
        assert validate_pydantic_model(TestModel, valid_data) is True

    def test_validate_pydantic_model_invalid(self):
        """Test validating data against a Pydantic model with invalid data."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            age: int

        invalid_data = {"name": "John", "age": "not_a_number"}
        assert validate_pydantic_model(TestModel, invalid_data) is False


class TestDictToPydantic:
    """Test cases for dict_to_pydantic function."""

    def test_dict_to_pydantic_valid(self):
        """Test converting dict to Pydantic model with valid data."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            age: int

        valid_data = {"name": "John", "age": 30}
        result = dict_to_pydantic(TestModel, valid_data)

        assert result is not None
        assert result.name == "John"
        assert result.age == 30

    def test_dict_to_pydantic_invalid(self):
        """Test converting dict to Pydantic model with invalid data."""
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str
            age: int

        invalid_data = {"name": "John", "age": "not_a_number"}
        result = dict_to_pydantic(TestModel, invalid_data)

        assert result is None
