"""Logger factory for creating and managing logger instances."""

import logging
from typing import Optional, Dict, Any
from logging import Logger

from .structured_log_formatter import StructuredLogFormatter, KeyValueLogFormatter
from .async_log_handler import AsyncLogHandler, BufferedAsyncLogHandler


class LoggerFactory:
    """Factory for creating and managing logger instances with enhanced features."""

    # Singleton instance
    _instance: Optional['LoggerFactory'] = None

    # Logger registry to ensure singleton pattern
    _logger_registry: Dict[str, Logger] = {}

    def __new__(cls) -> 'LoggerFactory':
        """Create or return singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_logger(
        self, 
        name: str, 
        level: Optional[str] = None,
        structured: bool = False,
        async_enabled: bool = False,
        buffered: bool = False
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
        # Return cached logger if it exists
        if name in self._logger_registry:
            return self._logger_registry[name]

        # Create new logger
        logger = logging.getLogger(name)
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Set logging level
        if level:
            logger.setLevel(getattr(logging, level))
        else:
            logger.setLevel(logging.INFO)
            
        # Choose appropriate formatter
        if structured:
            formatter = StructuredLogFormatter()
        else:
            formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s: %(name)s: %(message)s'
            )
            
        # Choose appropriate handler
        if async_enabled:
            if buffered:
                handler = BufferedAsyncLogHandler()
            else:
                handler = AsyncLogHandler()
        else:
            handler = logging.StreamHandler()
            
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add file handler with rotation
        import os
        from pathlib import Path
        from logging.handlers import RotatingFileHandler
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Add file handler
        file_handler = RotatingFileHandler(
            log_dir / f"{name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Cache the logger
        self._logger_registry[name] = logger
        
        return logger

    def get_structured_logger(self, name: str, level: Optional[str] = None) -> Logger:
        """Get a structured logger instance.

        Args:
            name: Logger name
            level: Logging level

        Returns:
            Structured logger instance
        """
        return self.get_logger(name, level, structured=True)

    def get_async_logger(self, name: str, level: Optional[str] = None, buffered: bool = False) -> Logger:
        """Get an async logger instance.

        Args:
            name: Logger name
            level: Logging level
            buffered: Whether to use buffered async logging

        Returns:
            Async logger instance
        """
        return self.get_logger(name, level, async_enabled=True, buffered=buffered)

    def get_structured_async_logger(self, name: str, level: Optional[str] = None, buffered: bool = False) -> Logger:
        """Get a structured async logger instance.

        Args:
            name: Logger name
            level: Logging level
            buffered: Whether to use buffered async logging

        Returns:
            Structured async logger instance
        """
        return self.get_logger(name, level, structured=True, async_enabled=True, buffered=buffered)

    def configure_all_loggers(self, config: Dict[str, Any]) -> None:
        """Configure all registered loggers with specified settings.

        Args:
            config: Configuration parameters for all loggers
        """
        # Apply configuration to all registered loggers
        for logger in self._logger_registry.values():
            if "level" in config:
                logger.setLevel(getattr(logging, config["level"]))
                
            # Update handlers if specified
            if "handlers" in config:
                # Clear existing handlers
                logger.handlers.clear()
                
                # Add new handlers based on configuration
                for handler_config in config["handlers"]:
                    # Implementation would depend on specific handler types
                    pass


# Global factory instance
_factory = LoggerFactory()


def get_logger(
    name: str, 
    level: Optional[str] = None,
    structured: bool = False,
    async_enabled: bool = False,
    buffered: bool = False
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
    return _factory.get_logger(name, level, structured, async_enabled, buffered)


def get_structured_logger(name: str, level: Optional[str] = None) -> Logger:
    """Get a structured logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Structured logger instance
    """
    return _factory.get_structured_logger(name, level)


def get_async_logger(name: str, level: Optional[str] = None, buffered: bool = False) -> Logger:
    """Get an async logger instance.

    Args:
        name: Logger name
        level: Logging level
        buffered: Whether to use buffered async logging

    Returns:
        Async logger instance
    """
    return _factory.get_async_logger(name, level, buffered)


def get_structured_async_logger(name: str, level: Optional[str] = None, buffered: bool = False) -> Logger:
    """Get a structured async logger instance.

    Args:
        name: Logger name
        level: Logging level
        buffered: Whether to use buffered async logging

    Returns:
        Structured async logger instance
    """
    return _factory.get_structured_async_logger(name, level, buffered)


def configure_all_loggers(config: Dict[str, Any]) -> None:
    """Configure all registered loggers with specified settings.

    Args:
        config: Configuration parameters for all loggers
    """
    _factory.configure_all_loggers(config)