"""Integration module for the MetaExpert logging system.

This module provides seamless integration between the enhanced logging system
and the MetaExpert trading framework, ensuring backward compatibility while
providing enhanced functionality.
"""

from typing import Any

from metaexpert.logger.enhanced_config import LoggingConfig
from metaexpert.logger.log_manager import log_manager


def configure_logging(
    log_level: str = "INFO",
    log_file: str = "expert.log",
    trade_log_file: str = "trades.log",
    error_log_file: str = "errors.log",
    log_to_console: bool = True,
    structured_logging: bool = False,
    async_logging: bool = False,
    log_directory: str | None = None,
    rate_limit: int = 1200,
    enable_metrics: bool = True,
    persist_state: bool = True,
    state_file: str = "state.json",
) -> dict[str, Any]:
    """
    Configure logging specifically for MetaExpert with all template parameters.

    This function accepts all logging-related parameters from the MetaExpert
    template and configures the enhanced logging system accordingly.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Main log file name
        trade_log_file: Trade execution log file name
        error_log_file: Error-specific log file name
        log_to_console: Whether to print logs to console
        structured_logging: Whether to use structured JSON logging
        async_logging: Whether to use asynchronous logging
        log_directory: Directory for log files (optional)
        rate_limit: Max requests per minute (for future rate limiting features)
        enable_metrics: Enable performance metrics (for future metrics features)
        persist_state: Persist state between runs (for future state features)
        state_file: State persistence file (for future state features)

    Returns:
        Configuration result with status and message
    """
    # Configure the core logging system
    result = log_manager.configure(
        log_level=log_level,
        log_file=log_file,
        trade_log_file=trade_log_file,
        error_log_file=error_log_file,
        log_to_console=log_to_console,
        structured_logging=structured_logging,
        async_logging=async_logging,
        log_directory=log_directory,
    )

    # Add MetaExpert-specific configuration to result
    if result["status"] == "success":
        result["expert_config"] = {
            "rate_limit": rate_limit,
            "enable_metrics": enable_metrics,
            "persist_state": persist_state,
            "state_file": state_file,
        }
        result["message"] = "Expert logging system configured successfully"

    return result


def create_handlers_config(
    log_level: str = "INFO",
    log_file: str = "expert.log",
    trade_log_file: str = "trades.log",
    error_log_file: str = "errors.log",
    log_to_console: bool = True,
) -> dict[str, Any]:
    """
    Create handlers configuration compatible with the original configure_logging function.

    This function creates a configuration dictionary that matches the format
    expected by the original configure_logging function in __init__.py.

    Args:
        log_level: Logging level
        log_file: Main log file name
        trade_log_file: Trade log file name
        error_log_file: Error log file name
        log_to_console: Whether to include console handler

    Returns:
        Handlers configuration dictionary
    """
    handlers_config = {
        "file": {"type": "file", "filename": log_file, "level": log_level},
        "trade_file": {"type": "file", "filename": trade_log_file, "level": "INFO"},
        "error_file": {
            "type": "file",
            "filename": error_log_file,
            "level": "ERROR",
        },
    }

    if log_to_console:
        handlers_config["console"] = {"type": "console", "level": log_level}

    return handlers_config


def get_logger_config() -> dict[str, Any]:
    """
    Get the current logging configuration.

    Returns:
        Current logging configuration dictionary
    """
    return LoggingConfig.create_default_config()


def validate_logging_params(**kwargs) -> dict[str, Any]:
    """
    Validate logging parameters and provide defaults.

    Args:
        **kwargs: Logging parameters to validate

    Returns:
        Validated and normalized parameters
    """
    # Define valid log levels
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

    # Validate and normalize parameters
    params = {
        "log_level": kwargs.get("log_level", "INFO").upper(),
        "log_file": kwargs.get("log_file", "expert.log"),
        "trade_log_file": kwargs.get("trade_log_file", "trades.log"),
        "error_log_file": kwargs.get("error_log_file", "errors.log"),
        "log_to_console": bool(kwargs.get("log_to_console", True)),
        "structured_logging": bool(kwargs.get("structured_logging", False)),
        "async_logging": bool(kwargs.get("async_logging", False)),
    }

    # Validate log level
    if params["log_level"] not in valid_levels:
        params["log_level"] = "INFO"

    # Ensure file names are strings and not empty
    for file_param in ["log_file", "trade_log_file", "error_log_file"]:
        value = params[file_param]
        if not isinstance(value, str) or not value.strip():
            params[file_param] = f"default_{file_param.replace('_file', '')}.log"

    return params


# Convenience functions for common logging scenarios
def log_expert_startup(expert_name: str, exchange: str, symbol: str, timeframe: str) -> None:
    """Log expert startup information."""
    main_logger = log_manager.get_main_logger()
    main_logger.info(
        "Expert started: %s on %s, Symbol: %s, Timeframe: %s",
        expert_name, exchange, symbol, timeframe
    )


def log_expert_shutdown(expert_name: str, reason: str = "normal") -> None:
    """Log expert shutdown information."""
    main_logger = log_manager.get_main_logger()
    main_logger.info("Expert shutdown: %s, Reason: %s", expert_name, reason)


def log_trade_execution(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    order_id: str = "",
    strategy_id: int = 0,
) -> None:
    """Log trade execution with structured data."""
    log_manager.log_trade(
        f"Trade executed: {side} {quantity} {symbol} @ {price}",
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        order_id=order_id,
        strategy_id=strategy_id,
    )


def log_expert_error(
    error_message: str,
    exception: Exception | None = None,
    component: str = "",
    operation: str = "",
) -> None:
    """Log expert-specific errors with context."""
    log_manager.log_error(
        error_message,
        exception=exception,
        component=component,
        operation=operation,
    )
