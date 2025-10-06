"""MetaLogger: Enhanced logging system for MetaExpert trading framework.

This module provides a custom Logger class that integrates with the MetaExpert
logging system, offering structured logging, asynchronous logging, and
specialized handlers for trade and error logging.
"""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from metaexpert.config import (
    APP_NAME,
    DEFAULT_LOG_LEVEL,
    LOG_ASYNC_LOGGING,
    LOG_BACKUP_COUNT,
    LOG_CONSOLE_LOGGING,
    LOG_DIRECTORY,
    LOG_ERROR_FILE,
    LOG_FILE,
    LOG_MAX_FILE_SIZE,
    LOG_STRUCTURED_LOGGING,
    LOG_TRADE_FILE,
)
from metaexpert.logger.async_handler import AsyncHandler
from metaexpert.logger.formatter import ErrorFormatter, MainFormatter, TradeFormatter

# 1. Define custom log levels
TRADE_LEVEL_NUM = 25
logging.addLevelName(TRADE_LEVEL_NUM, "TRADE")

REPORT_LEVEL_NUM = 26
logging.addLevelName(REPORT_LEVEL_NUM, "REPORT")


# 2. Create the custom logger class
class MetaLogger(logging.Logger):
    """
    A self-configuring Logger class for the MetaExpert framework.

    This class extends the standard Logger to provide:
    - Custom `trade()` and `report()` methods.
    - Automatic configuration of file (rotating), console, and specialized
      handlers for trades and errors upon instantiation.
    - Support for structured (JSON), and asynchronous logging.
    """

    def __init__(self, name: str):
        """
        Initialize and configure the logger instance.
        """
        super().__init__(name)
        self.setLevel(DEFAULT_LOG_LEVEL.upper())

        # Prevent re-configuration if handlers are already present
        if self.handlers:
            return

        # --- Configuration ---
        log_dir = Path(LOG_DIRECTORY)
        log_dir.mkdir(exist_ok=True)

        # --- Formatters ---
        main_formatter = (
            MainFormatter()
            if LOG_STRUCTURED_LOGGING
            else logging.Formatter("[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
        )
        trade_formatter = TradeFormatter() if LOG_STRUCTURED_LOGGING else main_formatter
        error_formatter = (
            ErrorFormatter()
            if LOG_STRUCTURED_LOGGING
            else logging.Formatter(
                "[%(asctime)s] %(levelname)s: %(name)s:%(funcName)s:%(lineno)d: %(message)s"
            )
        )

        # --- Handlers ---
        handlers = {
            "main": logging.handlers.RotatingFileHandler(
                log_dir / LOG_FILE,
                maxBytes=LOG_MAX_FILE_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            ),
            "trade": logging.handlers.RotatingFileHandler(
                log_dir / LOG_TRADE_FILE,
                maxBytes=LOG_MAX_FILE_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            ),
            "error": logging.handlers.RotatingFileHandler(
                log_dir / LOG_ERROR_FILE,
                maxBytes=LOG_MAX_FILE_SIZE,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            ),
            "console": logging.StreamHandler(sys.stdout),
        }

        # Set formatters and levels
        handlers["main"].setFormatter(main_formatter)
        handlers["trade"].setFormatter(trade_formatter)
        handlers["error"].setFormatter(error_formatter)
        handlers["console"].setFormatter(main_formatter)

        handlers["main"].setLevel(DEFAULT_LOG_LEVEL.upper())
        handlers["trade"].setLevel(TRADE_LEVEL_NUM)
        handlers["error"].setLevel(logging.ERROR)
        handlers["console"].setLevel(DEFAULT_LOG_LEVEL.upper())

        # Apply async wrapper if enabled
        if LOG_ASYNC_LOGGING:
            for key, handler in handlers.items():
                handlers[key] = AsyncHandler(handler)

        # --- Attach Handlers ---
        self.addHandler(handlers["main"])
        self.addHandler(handlers["error"])
        if LOG_CONSOLE_LOGGING:
            self.addHandler(handlers["console"])
        self.propagate = False

        # Configure the separate trade logger
        trade_logger = logging.getLogger(f"{name}.trade")
        trade_logger.setLevel(TRADE_LEVEL_NUM)
        trade_logger.addHandler(handlers["trade"])
        trade_logger.propagate = False

    def trade(self, message: str, *args, **kwargs) -> None:
        """
        Log a 'TRADE' message.
        """
        if self.isEnabledFor(TRADE_LEVEL_NUM):
            self._log(TRADE_LEVEL_NUM, message, args, **kwargs)

    def report(self, message: str, *args, **kwargs) -> None:
        """
        Log a 'REPORT' message.
        """
        if self.isEnabledFor(REPORT_LEVEL_NUM):
            self._log(REPORT_LEVEL_NUM, message, args, **kwargs)


# 3. Set the custom logger class for all loggers
logging.setLoggerClass(MetaLogger)

# Module-level cache for logger instances
_loggers: dict[str, MetaLogger] = {}


# 4. Main factory function
def get_logger(name: str = APP_NAME) -> MetaLogger:
    """
    Retrieves a logger instance, creating it if it doesn't exist.

    This function acts as a factory and cache. The first time a logger for a
    given name is requested, it instantiates MetaLogger, which handles its
    own configuration. Subsequent calls return the cached instance.
    """
    if name in _loggers:
        return _loggers[name]

    # MetaLogger now handles its own configuration in __init__
    logger = logging.getLogger(name)
    _loggers[name] = logger
    return logger


def shutdown_loggers() -> None:
    """Shuts down all managed loggers and handlers."""
    logging.shutdown()
    _loggers.clear()
