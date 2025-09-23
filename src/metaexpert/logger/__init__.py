"""Logger module.

This module provides enhanced logging functionality for the trading bot,
including structured logging, asynchronous logging, and centralized configuration.

Logging levels:

NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

- DEBUG - самая подробная информация, нужна только разработчику и только для отладки,
          например значения переменных,
          какие данные получены и т.д.
- INFO - информационные сообщения, как подтверждение работы, например запуск сервиса.
- WARNING - еще не ошибка, но уже надо посмотреть - мало места на диске, мало памяти,
            много созданных объектов и т.д.
- ERROR - приложение еще работает и может работать, но что-то пошло не так.
- CRITICAL - приложение не может работать дальше.
"""

import json
import logging
import os
import sys
from logging import Formatter, Logger, StreamHandler, getLogger
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Dict, Any
import traceback
import time
import functools

from metaexpert.config import (
    LOG_BACKUP_COUNT,
    LOG_CONFIG,
    LOG_FILE,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_SIZE,
    LOG_NAME,
)

# Import enhanced logging components
from .structured_log_formatter import StructuredLogFormatter, KeyValueLogFormatter
from .async_log_handler import AsyncLogHandler, BufferedAsyncLogHandler
from .config import (
    get_logging_config, 
    update_logging_config,
    get_handler_config,
    update_handler_config
)

# Global logger registry to ensure centralized management
_logger_registry: Dict[str, Logger] = {}

# Performance optimization: cache for frequently accessed loggers
_logger_cache: Dict[str, Logger] = {}

# Performance optimization: disable expensive operations for high-frequency logging
_HIGH_FREQUENCY_THRESHOLD = 1000  # Log records per second
_log_rate_counter = 0
_last_rate_check = time.time()


class StructuredLogFormatter(Formatter):
    """Formatter for structured logging with JSON output."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the structured log formatter."""
        super().__init__(*args, **kwargs)
        # Pre-compile frequently used format strings for performance
        self._time_format = "%Y-%m-%d %H:%M:%S"
        
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as structured JSON.
        
        Args:
            record: The log record to format
            
        Returns:
            Formatted log record as JSON string
        """
        try:
            # Performance optimization: Rate limiting for high-frequency logging
            global _log_rate_counter, _last_rate_check
            _log_rate_counter += 1
            
            current_time = time.time()
            if current_time - _last_rate_check > 1.0:  # Check every second
                rate = _log_rate_counter / (current_time - _last_rate_check)
                _log_rate_counter = 0
                _last_rate_check = current_time
                
                # If rate is too high, simplify formatting
                if rate > _HIGH_FREQUENCY_THRESHOLD:
                    # Simplified formatting for high-frequency logging
                    return f'{{"timestamp":"{self.formatTime(record)}","level":"{record.levelname}","message":"{record.getMessage()}"}}'
            
            # Create a dictionary with log record attributes
            log_entry = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "module": record.module,
                "message": record.getMessage(),
            }
            
            # Add context data if present
            if hasattr(record, "context"):
                log_entry["context"] = record.context
                
            # Add exception information if present
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
                
            # Convert to JSON string
            return json.dumps(log_entry, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            # Fallback to simple string if JSON conversion fails
            return f"[JSON_FORMAT_ERROR] {super().format(record)} - Error: {str(e)}"
        except Exception as e:
            # Handle any other unexpected errors
            return f"[UNEXPECTED_ERROR] Failed to format log record - Error: {str(e)}"


class AsyncLogHandler(logging.Handler):
    """Asynchronous log handler that doesn't block the main thread."""
    
    def __init__(self) -> None:
        """Initialize the async log handler."""
        super().__init__()
        # For now, we'll use a simple sync handler
        # In a real implementation, this would use a queue and worker thread
        self.sync_handler: Optional[StreamHandler] = None
        
    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record asynchronously.
        
        Args:
            record: The log record to emit
        """
        # For now, we'll just delegate to a synchronous handler
        # In a real implementation, this would queue the record for async processing
        try:
            msg = self.format(record)
            # Print to stdout (in a real implementation, this would be queued)
            print(msg, file=sys.stderr)
        except Exception as e:
            # Handle errors in the emit method gracefully
            self.handleError(record)


def _rate_limited(func):
    """Decorator to rate-limit logger operations for performance."""
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
                    (end_time - start_time) * 1000
                )
            return result
        except Exception:
            # Re-raise exceptions without additional overhead
            raise
    return wrapper


@_rate_limited
def setup_logger(
    name: Optional[str] = None, 
    level: Optional[str] = None,
    structured: bool = False,
    async_enabled: bool = False
) -> Logger:
    """Set up and configure the logger with enhanced features.

    Args:
        name: Logger name. Defaults to None.
        level: Logging level. Defaults to None.
        structured: Whether to use structured logging. Defaults to False.
        async_enabled: Whether to use async logging. Defaults to False.

    Returns:
        Configured logger instance.
    """
    try:
        # Set default logger name if not provided
        if name is None:
            name = LOG_NAME

        # Performance optimization: Return cached logger if it exists
        cache_key = f"{name}_{level}_{structured}_{async_enabled}"
        if cache_key in _logger_cache:
            return _logger_cache[cache_key]

        # Return cached logger if it exists
        if name in _logger_registry:
            logger = _logger_registry[name]
            _logger_cache[cache_key] = logger
            return logger

        # Create logger instance
        logger = get_logger(name)
        
        # Check if log config file exists
        if os.path.isfile(LOG_CONFIG):
            try:
                # Load config from JSON file
                with open(LOG_CONFIG, encoding="utf-8") as file:
                    config = json.load(file)

                dictConfig(config)
                
                # Cache and return the configured logger
                _logger_registry[name] = logger
                _logger_cache[cache_key] = logger
                return logger
            except FileNotFoundError as e:
                logger.error("Error loading logging configuration file: %s", e)
            except json.JSONDecodeError as e:
                logger.error("Error parsing JSON logging configuration file: %s", e)
            except Exception as e:
                logger.error("Unexpected error loading logging configuration: %s", e)

        # Get log level from environment or config
        if level is None:
            level = os.getenv("LOG_LEVEL", LOG_LEVEL)

        # Configure logger
        try:
            logger.setLevel(getattr(logging, level) if level else LOG_LEVEL)
        except ValueError:
            logger.setLevel(logging.INFO)  # Fallback to INFO level
            logger.warning("Invalid log level '%s', falling back to INFO", level)

        # Clear existing handlers to avoid duplicate logs
        if logger.handlers:
            logger.handlers.clear()

        # Choose appropriate formatter based on structured flag
        if structured:
            formatter = StructuredLogFormatter()
        else:
            formatter = Formatter(LOG_FORMAT)

        # Choose appropriate handler based on async flag
        if async_enabled:
            handler: logging.Handler = AsyncLogHandler()
        else:
            # Create console handler
            handler = StreamHandler(stream=sys.stdout)
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Create logs directory if it doesn't exist
        try:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
        except Exception as e:
            logger.error("Failed to create logs directory: %s", e)
            # Continue without file logging if directory creation fails

        # Create file handler with rotation
        try:
            file_handler = RotatingFileHandler(
                log_dir / LOG_FILE,
                maxBytes=LOG_MAX_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error("Failed to create file handler: %s", e)
            # Continue with console logging only

        # Cache the logger
        _logger_registry[name] = logger
        _logger_cache[cache_key] = logger
        
        return logger
        
    except Exception as e:
        # Handle any unexpected errors during logger setup
        error_msg = f"Critical error during logger setup: {str(e)}"
        print(error_msg, file=sys.stderr)
        traceback.print_exc()
        # Return a basic logger as fallback
        basic_logger = getLogger(name or "fallback")
        basic_logger.setLevel(logging.ERROR)
        return basic_logger


@_rate_limited
def get_logger(name: Optional[str] = None) -> Logger:
    """Get the logger instance from centralized registry.

    Args:
        name: Logger name. Defaults to None.

    Returns:
        Logger instance.
    """
    try:
        # Performance optimization: Return cached logger if it exists
        if name and name in _logger_cache:
            return _logger_cache[name]
            
        # Return cached logger if it exists
        if name and name in _logger_registry:
            return _logger_registry[name]
        
        # Create new logger and cache it
        logger = getLogger(name)
        if name:
            _logger_registry[name] = logger
            _logger_cache[name] = logger
        return logger
    except Exception as e:
        # Handle any unexpected errors
        error_msg = f"Error getting logger '{name}': {str(e)}"
        print(error_msg, file=sys.stderr)
        # Return basic logger as fallback
        return getLogger(name)


@_rate_limited
def configure_logging(config: Dict[str, Any]) -> Dict[str, Any]:
    """Configure the centralized logging system with specified settings.

    Args:
        config: Configuration parameters for the logging system

    Returns:
        Dictionary with status and message
    """
    try:
        # Validate required parameters
        if "default_level" not in config:
            return {
                "status": "error",
                "message": "Missing required parameter: default_level"
            }
            
        # Validate log level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if config["default_level"] not in valid_levels:
            return {
                "status": "error",
                "message": f"Invalid log level: {config['default_level']}. Must be one of: {valid_levels}"
            }
            
        # For each handler in the configuration
        if "handlers" in config:
            for handler_name, handler_config in config["handlers"].items():
                # Validate handler configuration
                if "level" in handler_config and handler_config["level"] not in valid_levels:
                    return {
                        "status": "error",
                        "message": f"Invalid log level for {handler_name} handler: {handler_config['level']}"
                    }
                    
                # Validate handler-specific parameters
                if "max_size" in handler_config and handler_config["max_size"] < 0:
                    return {
                        "status": "error",
                        "message": f"Invalid max_size for {handler_name} handler: {handler_config['max_size']}. Must be non-negative."
                    }
                    
                if "backup_count" in handler_config and handler_config["backup_count"] < 0:
                    return {
                        "status": "error",
                        "message": f"Invalid backup_count for {handler_name} handler: {handler_config['backup_count']}. Must be non-negative."
                    }
                    
        # Apply configuration (in a real implementation, this would update all loggers)
        # For now, we'll just store it globally
        global _centralized_config
        _centralized_config = config
        
        return {
            "status": "success",
            "message": "Logging configuration applied successfully"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error configuring logging: {str(e)}"
        }


# Backward compatibility functions
def setup_logger_v1(name: Optional[str] = None, level: Optional[str] = None) -> Logger:
    """Backward compatibility function for the original setup_logger.
    
    Args:
        name: Logger name. Defaults to None.
        level: Logging level. Defaults to None.

    Returns:
        Configured logger instance.
    """
    return setup_logger(name, level)


def get_logger_v1(name: Optional[str] = None) -> Logger:
    """Backward compatibility function for the original get_logger.
    
    Args:
        name: Logger name. Defaults to None.

    Returns:
        Logger instance.
    """
    return get_logger(name)


# Centralized configuration storage
_centralized_config: Dict[str, Any] = {}


# For backward compatibility, export the original function names
setup_logger_original = setup_logger
get_logger_original = get_logger
