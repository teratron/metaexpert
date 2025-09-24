"""Setup functions for the enhanced logger system."""

from logging import Logger
from pathlib import Path

from metaexpert.logger import configure_logging, setup_logger


def setup_enhanced_logging(
    name: str,
    log_level: str = "INFO",
    log_file: str = "expert.log",
    trade_log_file: str = "trades.log",
    error_log_file: str = "errors.log",
    log_to_console: bool = True,
    structured_logging: bool = False,
    async_logging: bool = False,
) -> Logger:
    """Set up enhanced logging with the new features.

    Args:
        name: Name for the logger
        log_level: Logging level
        log_file: Main log file
        trade_log_file: Trade execution log file
        error_log_file: Error-specific log file
        log_to_console: Whether to print logs to console
        structured_logging: Whether to use structured JSON logging
        async_logging: Whether to use asynchronous logging

    Returns:
        Configured logger instance
    """
    try:
        # Configure centralized logging system
        config = {
            "default_level": log_level,
            "handlers": {
                "console": {
                    "level": log_level,
                    "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                    "structured": structured_logging,
                },
                "file": {
                    "level": log_level,
                    "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                    "structured": structured_logging,
                    "filename": log_file,
                    "max_size": 10485760,  # 10MB
                    "backup_count": 5,
                },
                "trade_file": {
                    "level": "INFO",
                    "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                    "structured": structured_logging,
                    "filename": trade_log_file,
                    "max_size": 10485760,  # 10MB
                    "backup_count": 5,
                },
                "error_file": {
                    "level": "ERROR",
                    "format": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
                    "structured": structured_logging,
                    "filename": error_log_file,
                    "max_size": 10485760,  # 10MB
                    "backup_count": 5,
                },
            },
            "structured_logging": structured_logging,
            "async_logging": async_logging,
        }

        # Apply configuration
        result = configure_logging(config)
        if result["status"] == "error":
            logger = setup_logger(name)
            logger.warning(
                "Failed to configure enhanced logging: %s", result["message"]
            )

        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Return the configured logger
        return setup_logger(
            name=name,
            level=log_level,
            structured=structured_logging,
            async_enabled=async_logging,
        )

    except Exception as e:
        logger = setup_logger(name)
        logger.error("Failed to set up enhanced logging: %s", str(e))
        # Return a basic logger as fallback
        return setup_logger(name)
