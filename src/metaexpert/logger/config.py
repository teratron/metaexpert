"""Configuration file for the logger module."""

import os

from dotenv import load_dotenv

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

# Log file paths
LOG_DIRECTORY: str = os.getenv("LOG_DIRECTORY", "logs")  # Directory for log files
DEFAULT_LOG_FILE_PATH: str = os.path.join(
    LOG_DIRECTORY, LOG_FILE
)  # Full path to default log file
