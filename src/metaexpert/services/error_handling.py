"""Error handling and logging module."""

import json
from functools import wraps
from typing import Any

from metaexpert.exceptions import ConfigurationError as MetaExpertConfigurationError
from metaexpert.exceptions import ProcessError


class TemplateCreationError(ProcessError):
    """Exception raised for errors in template creation."""

    def __init__(self, message: str, error_code: str | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            error_code: Optional error code
        """
        self.message = message
        self.error_code = error_code
        super().__init__("template_creator", message)


class ConfigurationError(MetaExpertConfigurationError):
    """Exception raised for configuration errors."""

    def __init__(self, message: str, parameter: str | None = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            parameter: Optional parameter name that caused the error
        """
        self.message = message
        self.parameter = parameter
        super().__init__("config", message)

def handle_template_errors(func):
    """Decorator to handle template-related errors.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TemplateCreationError as e:
            logger.error(f"Template creation error: {e.message}")
            if e.error_code:
                logger.error(f"Error code: {e.error_code}")
            raise
        except ConfigurationError as e:
            logger.error(f"Configuration error: {e.message}")
            if e.parameter:
                logger.error(f"Parameter: {e.parameter}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise TemplateCreationError(f"Unexpected error: {e}") from e

    return wrapper

def log_template_operation(operation: str, details: str | None = None) -> None:
    """Log a template operation.

    Args:
        operation: Operation being performed
        details: Optional details about the operation
    """
    message = f"Template operation: {operation}"
    if details:
        message += f" - {details}"

    logger.info(message)

def log_configuration_change(parameter: str, old_value: str, new_value: str) -> None:
    """Log a configuration parameter change.

    Args:
        parameter: Parameter name
        old_value: Old value
        new_value: New value
    """
    logger.info(f"Configuration change: {parameter} changed from '{old_value}' to '{new_value}'")

def log_request(request_data: dict[str, Any], endpoint: str) -> None:
    """Log an incoming request.

    Args:
        request_data: Request data
        endpoint: Endpoint that received the request
    """
    logger.info(f"Request to {endpoint}: {json.dumps(request_data, indent=2)}")

def log_response(response_data: dict[str, Any], endpoint: str, duration: float) -> None:
    """Log an outgoing response.

    Args:
        response_data: Response data
        endpoint: Endpoint that sent the response
        duration: Duration of the request in seconds
    """
    logger.info(f"Response from {endpoint} (took {duration:.2f}s): {json.dumps(response_data, indent=2)}")

def log_api_call(exchange: str, method: str, endpoint: str, status_code: int) -> None:
    """Log an API call.

    Args:
        exchange: Exchange name
        method: HTTP method
        endpoint: API endpoint
        status_code: HTTP status code
    """
    logger.info(f"API call: {exchange} {method} {endpoint} - Status: {status_code}")
