"""Template validation middleware."""

from collections.abc import Callable
from functools import wraps
from typing import Any

from metaexpert.services.validation_service import (
    validate_template_parameters,
    validate_template_structure,
)


def template_validation_middleware(func: Callable) -> Callable:
    """Middleware to validate template files before processing.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if the function has a template_path parameter
        template_path = kwargs.get('template_path')
        if template_path is None and len(args) > 0:
            # Assume first argument is template_path
            template_path = args[0]

        # Validate template if path is provided
        if template_path and isinstance(template_path, str):
            # Validate template structure
            structure_result = validate_template_structure(template_path)
            if not structure_result["valid"]:
                raise ValueError(f"Template structure validation failed: {structure_result['errors']}")

            # Validate template parameters
            param_result = validate_template_parameters(template_path)
            if not param_result["valid"]:
                raise ValueError(f"Template parameter validation failed: {param_result['errors']}")

        # Call the original function
        return func(*args, **kwargs)

    return wrapper

def validate_template_on_creation(template_path: str) -> dict[str, Any]:
    """Validate a template file after creation.

    Args:
        template_path: Path to the template file to validate

    Returns:
        Dictionary with validation results
    """
    # Validate template structure
    structure_result = validate_template_structure(template_path)
    if not structure_result["valid"]:
        return structure_result

    # Validate template parameters
    param_result = validate_template_parameters(template_path)
    if not param_result["valid"]:
        return param_result

    return {
        "valid": True,
        "message": "Template validation passed"
    }
