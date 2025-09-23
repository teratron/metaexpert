"""Configuration file for the enhanced logger module."""

import os
from typing import Any

from dotenv import load_dotenv  # type: ignore

from metaexpert.config import APP_NAME

_ = load_dotenv()

# Basic Logging configuration
LOG_NAME: str = APP_NAME  # Logger name
LOG_LEVEL: str = os.getenv(
    "LOG_LEVEL", "INFO"
)  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FORMAT: str = os.getenv(
    "LOG_FORMAT", "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
)  # Log format
LOG_CONFIG: str = os.getenv("LOG_CONFIG", "config.json")  # Log configuration file name
LOG_FILE: str = os.getenv("LOG_FILE", "app.log")  # Log file name
LOG_MAX_SIZE: int = int(
    os.getenv("LOG_MAX_SIZE", "10485760")
)  # Maximum log file size (10MB default)
LOG_BACKUP_COUNT: int = int(
    os.getenv("LOG_BACKUP_COUNT", "5")
)  # Number of backup log files

# Enhanced Logging configuration
STRUCTURED_LOGGING_ENABLED: bool = (
    os.getenv("STRUCTURED_LOGGING_ENABLED", "false").lower() == "true"
)  # Enable structured logging
ASYNC_LOGGING_ENABLED: bool = (
    os.getenv("ASYNC_LOGGING_ENABLED", "false").lower() == "true"
)  # Enable async logging
BUFFERED_ASYNC_LOGGING: bool = (
    os.getenv("BUFFERED_ASYNC_LOGGING", "false").lower() == "true"
)  # Enable buffered async logging

# Log file paths
LOG_DIRECTORY: str = os.getenv("LOG_DIRECTORY", "logs")  # Directory for log files
DEFAULT_LOG_FILE_PATH: str = os.path.join(
    LOG_DIRECTORY, LOG_FILE
)  # Full path to default log file

# Performance configuration
ASYNC_QUEUE_SIZE: int = int(
    os.getenv("ASYNC_QUEUE_SIZE", "10000")
)  # Async logging queue size
BUFFER_FLUSH_INTERVAL: float = float(
    os.getenv("BUFFER_FLUSH_INTERVAL", "1.0")
)  # Buffer flush interval (seconds)
BUFFER_SIZE: int = int(os.getenv("BUFFER_SIZE", "100"))  # Buffer size for async logging

# Handler configurations
HANDLER_CONFIGURATIONS: dict[str, dict[str, Any]] = {
    "console": {
        "enabled": True,
        "level": LOG_LEVEL,
        "format": LOG_FORMAT,
        "structured": STRUCTURED_LOGGING_ENABLED,
    },
    "file": {
        "enabled": True,
        "level": LOG_LEVEL,
        "format": LOG_FORMAT,
        "structured": STRUCTURED_LOGGING_ENABLED,
        "filename": DEFAULT_LOG_FILE_PATH,
        "max_bytes": LOG_MAX_SIZE,
        "backup_count": LOG_BACKUP_COUNT,
    },
}

# Centralized configuration
CENTRALIZED_LOGGING_CONFIG: dict[str, Any] = {
    "default_level": LOG_LEVEL,
    "handlers": HANDLER_CONFIGURATIONS,
    "structured_logging": STRUCTURED_LOGGING_ENABLED,
    "async_logging": ASYNC_LOGGING_ENABLED,
    "buffered_async": BUFFERED_ASYNC_LOGGING,
    "performance": {
        "queue_size": ASYNC_QUEUE_SIZE,
        "buffer_flush_interval": BUFFER_FLUSH_INTERVAL,
        "buffer_size": BUFFER_SIZE,
    },
}


def get_logging_config() -> dict[str, Any]:
    """Get the current logging configuration.

    Returns:
        Dictionary with current logging configuration
    """
    return CENTRALIZED_LOGGING_CONFIG


def update_logging_config(new_config: dict[str, Any]) -> None:
    """Update the logging configuration.

    Args:
        new_config: New configuration parameters to apply
    """
    global CENTRALIZED_LOGGING_CONFIG
    CENTRALIZED_LOGGING_CONFIG.update(new_config)


def get_handler_config(handler_name: str) -> dict[str, Any] | None:
    """Get configuration for a specific handler.

    Args:
        handler_name: Name of the handler to get configuration for

    Returns:
        Handler configuration or None if not found
    """
    return HANDLER_CONFIGURATIONS.get(handler_name)


def update_handler_config(handler_name: str, config: dict[str, Any]) -> None:
    """Update configuration for a specific handler.

    Args:
        handler_name: Name of the handler to update
        config: New configuration for the handler
    """
    if handler_name in HANDLER_CONFIGURATIONS:
        HANDLER_CONFIGURATIONS[handler_name].update(config)
    else:
        HANDLER_CONFIGURATIONS[handler_name] = config
