"""Simplified logger factory for creating and managing logger instances."""

import logging
from logging import Logger


def get_logger(
    name: str,
    level: str | None = None,
    structured: bool = False,
    async_enabled: bool = False,
    buffered: bool = False,
) -> Logger:
    """Get a logger instance with specified configuration.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        structured: Whether to use structured logging
        async_enabled: Whether to use async logging
        buffered: Whether to use buffered async logging

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)

    # Set logging level
    logger.setLevel(getattr(logging, level or "INFO", logging.INFO))

    # If no handlers exist, add a basic console handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
