"""Logging endpoint for configuring the enhanced logger system."""

from typing import Any

from metaexpert.logger import configure_logging


def configure_logging_endpoint(request: dict[str, Any]) -> dict[str, Any]:
    """Handle POST /logging/configure endpoint requests.

    Args:
        request: Configuration request with logging parameters

    Returns:
        Response with status and message
    """
    # Validate request
    if not isinstance(request, dict):
        return {
            "status": "error",
            "message": "Invalid request format. Expected JSON object.",
        }

    # Delegate to the logging configuration function
    try:
        result = configure_logging(request)
        return result
    except Exception as e:
        return {"status": "error", "message": f"Internal server error: {e!s}"}
