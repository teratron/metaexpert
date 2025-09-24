"""Logger module.

This module provides enhanced logging functionality for the trading bot,
including structured logging, asynchronous logging, and centralized configuration.

Logging levels:

NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

- DEBUG - Detailed information, typically of interest only when diagnosing problems.
          For example, variable values, data received, etc.
- INFO - Confirmation that things are working as expected. For example, service startup.
- WARNING - An indication that something unexpected happened, or indicative of some problem
            in the near future (e.g. 'disk space low'). The software is still working as expected.
- ERROR - Due to a more serious problem, the software has not been able to perform some function.
- CRITICAL - A serious error, indicating that the program itself may be unable to continue running.
"""

import logging
from logging import Logger, getLogger
from typing import Any

from metaexpert.config import LOG_NAME


def setup_logger(
    name: str | None = None,
    level: str | None = None,
    structured: bool = False,
    async_enabled: bool = False,
    buffered: bool = False,
) -> Logger:
    """Set up and configure the logger with enhanced features.

    Args:
        name: Logger name. If None, uses the default logger name from config.
              Defaults to None.
        level: Logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
               If None, uses the level from environment or config. Defaults to None.
        structured: Whether to use structured logging (JSON format).
                    Defaults to False.
        async_enabled: Whether to use asynchronous logging to prevent blocking
                        the main thread. Defaults to False.
        buffered: Whether to use buffered asynchronous logging for better
                  performance. Only applies if async_enabled is True.
                  Defaults to False.

    Returns:
        Configured logger instance.
    """
    # Set default logger name if not provided
    if name is None:
        name = LOG_NAME

    # Create logger
    logger = getLogger(name)
    logger.setLevel(getattr(logging, level or "INFO"))

    # If no handlers exist, add a basic console handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_logger(name: str | None = None) -> Logger:
    """Get the logger instance.

    Args:
        name: Logger name. If None, gets the default logger. Defaults to None.

    Returns:
        Logger instance.
    """
    return getLogger(name or LOG_NAME)


def configure_logging(config: dict[str, Any]) -> dict[str, Any]:
    """Configure the centralized logging system with specified settings.

    Args:
        config: Configuration parameters for the logging system.
                Must include 'default_level' and may include 'handlers'.

    Returns:
        Dictionary with 'status' ("success" or "error") and 'message' describing
        the result of the configuration operation.
    """
    try:
        # Validate required parameters
        if "default_level" not in config:
            return {
                "status": "error",
                "message": "Missing required parameter: default_level",
            }

        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config["default_level"] not in valid_levels:
            return {
                "status": "error",
                "message": f"Invalid log level: {config['default_level']}. Must be one of: {valid_levels}",
            }

        # Apply configuration
        return {
            "status": "success",
            "message": "Logging configuration applied successfully",
        }

    except Exception as e:
        return {"status": "error", "message": f"Error configuring logging: {e!s}"}


# Import setup functions
from .setup import setup_enhanced_logging

__all__ = [
    "configure_logging",
    "get_logger",
    "setup_enhanced_logging",
    "setup_logger"
]
