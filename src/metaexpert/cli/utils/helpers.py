"""Helper utilities for CLI operations."""

import json
import os
import shutil
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel


def get_config_file_path() -> Path:
    """
    Get the path to the CLI configuration file.

    Returns:
        Path: Path to the configuration file, typically in the user's home directory.
    """
    home_dir = Path.home()
    config_dir = home_dir / ".metaexpert"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.yaml"


def ensure_directory_exists(path: str | Path) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        path: Path to the directory to ensure exists.

    Returns:
        Path: The path that was ensured to exist.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_directory(
    path: str | Path, exclude_patterns: list[str] | None = None
) -> None:
    """
    Clear the contents of a directory, optionally excluding certain patterns.

    Args:
        path: Path to the directory to clear.
        exclude_patterns: Optional list of patterns to exclude from deletion.
    """
    path = Path(path)
    if not path.exists() or not path.is_dir():
        return

    exclude_patterns = exclude_patterns or []

    for item in path.iterdir():
        should_delete = True
        for pattern in exclude_patterns:
            if item.match(pattern):
                should_delete = False
                break

        if should_delete:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)


def safe_json_load(file_path: str | Path) -> dict[str, Any] | None:
    """
    Safely load a JSON file, returning None if the file doesn't exist or is invalid.

    Args:
        file_path: Path to the JSON file to load.

    Returns:
        Optional[Dict[str, Any]]: The loaded JSON data or None if loading failed.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def safe_yaml_load(file_path: str | Path) -> dict[str, Any] | None:
    """
    Safely load a YAML file, returning None if the file doesn't exist or is invalid.

    Args:
        file_path: Path to the YAML file to load.

    Returns:
        Optional[Dict[str, Any]]: The loaded YAML data or None if loading failed.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError):
        return None


def convert_to_bool(value: str | int | bool) -> bool:
    """
    Convert a value to boolean following common conventions.

    Args:
        value: Value to convert to boolean.

    Returns:
        bool: Boolean representation of the value.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on", "y", "t")
    return bool(value)


def convert_to_type(value: Any, target_type: type) -> Any:
    """
    Convert a value to a specified type.

    Args:
        value: Value to convert.
        target_type: Target type to convert to.

    Returns:
        Any: Converted value.
    """
    if value is None:
        return None

    if target_type is bool:
        return convert_to_bool(value)

    if target_type is int:
        try:
            return int(value)
        except ValueError:
            return 0

    if target_type is float:
        try:
            return float(value)
        except ValueError:
            return 0.0

    if target_type is str:
        return str(value)

    if target_type is list:
        if isinstance(value, str):
            # Handle comma-separated values
            return [item.strip() for item in value.split(",")]
        return list(value)

    if target_type is dict:
        if isinstance(value, str):
            # Try to parse as JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return {}
        return dict(value)

    # For other types, try direct conversion
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return value


def get_env_var(key: str, default: str | None = None) -> str | None:
    """
    Get an environment variable with an optional default.

    Args:
        key: Name of the environment variable.
        default: Default value if the environment variable is not set.

    Returns:
        Optional[str]: Value of the environment variable or default.
    """
    return os.getenv(key, default)


def format_bytes(bytes_value: int | float) -> str:
    """
    Format bytes value to human-readable format.

    Args:
        bytes_value: Number of bytes to format.

    Returns:
        str: Human-readable format of the bytes value.
    """
    bytes_value = float(bytes_value)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def is_valid_path(path: str | Path) -> bool:
    """
    Check if a path is valid.

    Args:
        path: Path to validate.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    try:
        Path(path).resolve()
        return True
    except OSError:
        return False


def get_file_size(path: str | Path) -> int:
    """
    Get the size of a file in bytes.

    Args:
        path: Path to the file.

    Returns:
        int: Size of the file in bytes, or -1 if the file doesn't exist.
    """
    path = Path(path)
    if path.exists() and path.is_file():
        return path.stat().st_size
    return -1


def merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively merge two dictionaries, with values from override taking precedence.

    Args:
        base: Base dictionary to merge into.
        override: Dictionary with values to override.

    Returns:
        Dict[str, Any]: Merged dictionary.
    """
    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length, adding a suffix if truncated.

    Args:
        text: String to truncate.
        max_length: Maximum length of the string.
        suffix: Suffix to add if the string is truncated.

    Returns:
        str: Truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def validate_pydantic_model(model_class: type, data: dict[str, Any]) -> bool:
    """
    Validate data against a Pydantic model.

    Args:
        model_class: Pydantic model class to validate against.
        data: Data to validate.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    try:
        model_class(**data)
        return True
    except Exception:
        return False


def dict_to_pydantic(model_class: type, data: dict[str, Any]) -> BaseModel | None:
    """
    Convert a dictionary to a Pydantic model instance.

    Args:
        model_class: Pydantic model class to convert to.
        data: Data to convert.

    Returns:
        Optional[BaseModel]: Model instance or None if conversion fails.
    """
    try:
        return model_class(**data)
    except Exception:
        return None
