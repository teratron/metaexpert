"""Configuration file for the logger module."""

import os

from dotenv_vault import load_dotenv  # type: ignore

from metaexpert.config import APP_NAME

_ = load_dotenv()

# Logging configuration
LOG_NAME: str = APP_NAME  # Logger name
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "")  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FORMAT: str = os.getenv("LOG_FORMAT", "")  # Log format
LOG_CONFIG: str = os.getenv("LOG_CONFIG", "")  # Log configuration file name
LOG_FILE: str = os.getenv("LOG_FILE", "")  # Log file name
LOG_MAX_SIZE: int = int(str(os.getenv("LOG_MAX_SIZE", 10000)))  # Maximum log file size (10*1024*1024 = 10MB)
LOG_BACKUP_COUNT: int = int(str(os.getenv("LOG_BACKUP_COUNT", 5)))  # Number of backup log files
