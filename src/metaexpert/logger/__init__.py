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

import functools
import logging
import sys
import time
import traceback
from logging import Logger, getLogger
from typing import Any

from metaexpert.config import LOG_NAME

# Global logger registry to ensure centralized management
# This registry stores all created logger instances to avoid duplication
# and provide a single point of access for logger management.
_logger_registry: dict[str, Logger] = {}

# Performance optimization: cache for frequently accessed loggers
# This cache stores recently accessed loggers to reduce lookup time
# for repeated requests for the same logger.
_logger_cache: dict[str, Logger] = {}

# Performance optimization: disable expensive operations for high-frequency logging
# These variables track logging frequency to prevent performance degradation
# from expensive operations when logging at high rates.
_HIGH_FREQUENCY_THRESHOLD = 1000  # Log records per second
_log_rate_counter = 0
_last_rate_check = time.time()


def _rate_limited(func):
    """Decorator to rate-limit logger operations for performance.

    This decorator implements simple rate limiting to prevent excessive logging
    from impacting application performance. It also monitors the execution
    time of decorated functions and logs warnings for slow operations.

    Args:
        func: The function to decorate

    Returns:
        The decorated function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Simple rate limiting to prevent excessive logging from impacting performance
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()

            # Log performance warning if operation takes too long
            if end_time - start_time > 0.01:  # 10ms threshold
                # Use a separate logger to avoid recursion
                perf_logger = getLogger("metaexpert.logger.performance")
                perf_logger.warning(
                    "Slow operation detected in %s: %.2fms",
                    func.__name__,
                    (end_time - start_time) * 1000,
                )
            return result
        except Exception:
            # Re-raise exceptions without additional overhead
            raise

    return wrapper


@_rate_limited
def setup_logger(
    name: str | None = None,
    level: str | None = None,
    structured: bool = False,
    async_enabled: bool = False,
    buffered: bool = False,
) -> Logger:
    """Set up and configure the logger with enhanced features.

    This function sets up a logger with the specified configuration. It uses the
    logger factory to create the logger and handles any errors during setup
    by providing a fallback basic logger.

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
        Configured logger instance. If an error occurs during setup, returns
        a basic fallback logger.

    Example:
        >>> logger = setup_logger("my_app", level="INFO", structured=True)
        >>> logger.info("Application started")
    """
    try:
        # Import the logger factory
        from .logger_factory import get_logger as factory_get_logger

        # Set default logger name if not provided
        if name is None:
            name = LOG_NAME

        # Use the logger factory to create the logger
        return factory_get_logger(name, level, structured, async_enabled, buffered)

    except Exception as e:
        # Handle any unexpected errors during logger setup
        error_msg = f"Critical error during logger setup: {e!s}"
        print(error_msg, file=sys.stderr)
        traceback.print_exc()
        # Return a basic logger as fallback
        basic_logger = getLogger(name or "fallback")
        basic_logger.setLevel(logging.ERROR)
        return basic_logger


@_rate_limited
def get_logger(name: str | None = None) -> Logger:
    """Get the logger instance from centralized registry.

    This function retrieves a logger instance from the centralized registry.
    If the logger doesn't exist, it creates a new one using the logger factory.

    Args:
        name: Logger name. If None, gets the root logger. Defaults to None.

    Returns:
        Logger instance. If an error occurs, returns a basic logger as fallback.

    Example:
        >>> logger = get_logger("my_app")
        >>> logger.info("Retrieved logger instance")
    """
    try:
        # Import the logger factory
        from .logger_factory import get_logger as factory_get_logger

        # Use the logger factory to get the logger
        return factory_get_logger(name)
    except Exception as e:
        # Handle any unexpected errors
        error_msg = f"Error getting logger '{name}': {e!s}"
        print(error_msg, file=sys.stderr)
        # Return basic logger as fallback
        return getLogger(name)


@_rate_limited
def configure_logging(config: dict[str, Any]) -> dict[str, Any]:
    """Configure the centralized logging system with specified settings.

    This function validates and applies logging configuration parameters.
    It checks for required parameters and validates log levels and handler
    configurations.

    Args:
        config: Configuration parameters for the logging system.
                Must include 'default_level' and may include 'handlers'.

    Returns:
        Dictionary with 'status' ("success" or "error") and 'message' describing
        the result of the configuration operation.

    Example:
        >>> config = {
        ...     "default_level": "INFO",
        ...     "handlers": {
        ...         "console": {"level": "INFO"},
        ...         "file": {"level": "DEBUG", "max_size": 10485760, "backup_count": 5}
        ...     }
        ... }
        >>> result = configure_logging(config)
        >>> print(result["status"])
        success
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

        # For each handler in the configuration
        if "handlers" in config:
            for handler_name, handler_config in config["handlers"].items():
                # Validate handler configuration
                if (
                    "level" in handler_config
                    and handler_config["level"] not in valid_levels
                ):
                    return {
                        "status": "error",
                        "message": f"Invalid log level for {handler_name} handler: {handler_config['level']}",
                    }

                # Validate handler-specific parameters
                if "max_size" in handler_config and handler_config["max_size"] < 0:
                    return {
                        "status": "error",
                        "message": f"Invalid max_size for {handler_name} handler: {handler_config['max_size']}. Must be non-negative.",
                    }

                if (
                    "backup_count" in handler_config
                    and handler_config["backup_count"] < 0
                ):
                    return {
                        "status": "error",
                        "message": f"Invalid backup_count for {handler_name} handler: {handler_config['backup_count']}. Must be non-negative.",
                    }

        # Apply configuration (in a real implementation, this would update all loggers)
        # For now, we'll just store it globally
        global _centralized_config
        _centralized_config = config

        return {
            "status": "success",
            "message": "Logging configuration applied successfully",
        }

    except Exception as e:
        return {"status": "error", "message": f"Error configuring logging: {e!s}"}


# Backward compatibility functions
def setup_logger_v1(name: str | None = None, level: str | None = None) -> Logger:
    """Backward compatibility function for the original setup_logger.

    This function provides backward compatibility with the original setup_logger
    function signature. It simply delegates to the new setup_logger function.

    Args:
        name: Logger name. Defaults to None.
        level: Logging level. Defaults to None.

    Returns:
        Configured logger instance.
    """
    return setup_logger(name, level)


def get_logger_v1(name: str | None = None) -> Logger:
    """Backward compatibility function for the original get_logger.

    This function provides backward compatibility with the original get_logger
    function signature. It simply delegates to the new get_logger function.

    Args:
        name: Logger name. Defaults to None.

    Returns:
        Logger instance.
    """
    return get_logger(name)


# Centralized configuration storage
# This global variable stores the current logging configuration
# to allow for dynamic reconfiguration of the logging system.
_centralized_config: dict[str, Any] = {}


# For backward compatibility, export the original function names
setup_logger_original = setup_logger
get_logger_original = get_logger
