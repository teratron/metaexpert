"""Middleware system for CLI commands."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from metaexpert.logger import get_logger


class Middleware(ABC):
    """Base middleware for CLI commands."""

    @abstractmethod
    def before(self, command_name: str, **kwargs) -> None:
        """
        Execute before command.

        Args:
            command_name: Name of the command being executed
            **kwargs: Command arguments
        """
        pass

    @abstractmethod
    def after(self, command_name: str, result: Any) -> None:
        """
        Execute after command.

        Args:
            command_name: Name of the command being executed
            result: Command execution result (or exception if it occurred)
        """
        pass


class PerformanceMiddleware(Middleware):
    """Track command execution time."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.start_time: float = 0

    def before(self, command_name: str, **kwargs) -> None:
        """Record start time."""
        import time

        self.start_time = time.time()
        self.logger.debug(f"Command started: {command_name}", command=command_name)

    def after(self, command_name: str, result: Any) -> None:
        """Log execution time."""
        import time

        duration = time.time() - self.start_time
        self.logger.info(
            f"Command completed: {command_name}",
            command=command_name,
            duration_ms=round(duration * 1000),
        )


class ErrorRecoveryMiddleware(Middleware):
    """Handle errors gracefully."""

    def __init__(self):
        self.logger = get_logger(__name__)

    def before(self, command_name: str, **kwargs) -> None:
        """No pre-processing needed."""
        pass

    def after(self, command_name: str, result: Any) -> None:
        """Log errors."""
        if isinstance(result, Exception):
            self.logger.error(
                f"Command failed: {command_name}",
                command=command_name,
                error=str(result),
            )


class MiddlewareManager:
    """Manage middleware execution."""

    def __init__(self):
        self.middlewares: List[Middleware] = []
        self.logger = get_logger(__name__)

    def register(self, middleware: Middleware) -> None:
        """
        Register middleware.

        Args:
            middleware: Middleware instance to register
        """
        self.middlewares.append(middleware)
        self.logger.debug(f"Registered middleware: {type(middleware).__name__}")

    def command_decorator(self, command_name: str) -> Callable:
        """
        Decorator for commands to apply middleware.

        Args:
            command_name: Name of the command to wrap

        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # Execute 'before' for all middlewares
                for middleware in self.middlewares:
                    try:
                        middleware.before(command_name, *args, **kwargs)
                    except Exception as e:
                        self.logger.error(f"Error in middleware 'before': {e}")

                # Execute the command
                try:
                    result = func(*args, **kwargs)
                    success = True
                except Exception as e:
                    result = e
                    success = False

                # Execute 'after' for all middlewares
                for middleware in self.middlewares:
                    try:
                        middleware.after(command_name, result)
                    except Exception as e:
                        self.logger.error(f"Error in middleware 'after': {e}")

                # Re-raise the exception if the command failed
                if not success:
                    raise result

                return result

            return wrapper

        return decorator


# Global middleware manager instance
_middleware_manager = MiddlewareManager()


def get_middleware_manager() -> MiddlewareManager:
    """Get the global middleware manager instance."""
    return _middleware_manager