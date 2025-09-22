"""Template structure validation module."""

import os
import re
from typing import Any


def validate_template_structure(template_path: str) -> dict[str, Any]:
    """Validate that a template file has the correct structure.

    Args:
        template_path: Path to the template file to validate

    Returns:
        Dictionary with validation results
    """
    if not os.path.exists(template_path):
        return {
            "valid": False,
            "errors": [f"Template file not found: {template_path}"]
        }

    try:
        with open(template_path, encoding='utf-8') as f:
            content = f.read()

        errors = []

        # Check for required sections
        required_sections = [
            "EXPERT CORE CONFIGURATION",
            "STRATEGY INITIALIZATION",
            "EVENT HANDLERS",
            "ENTRY POINT"
        ]

        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check for required expert initialization
        if "expert = MetaExpert(" not in content:
            errors.append("Missing expert initialization")

        # Check for required main function
        if "def main() -> None:" not in content:
            errors.append("Missing main function")

        # Check for required if-name-main block
        if 'if __name__ == "__main__":' not in content:
            errors.append("Missing if-name-main block")

        # Check for required imports
        if "from metaexpert import MetaExpert" not in content:
            errors.append("Missing MetaExpert import")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Error reading template file: {e}"]
        }

def validate_template_parameters(template_path: str) -> dict[str, Any]:
    """Validate that a template file has valid parameter definitions.

    Args:
        template_path: Path to the template file to validate

    Returns:
        Dictionary with validation results
    """
    if not os.path.exists(template_path):
        return {
            "valid": False,
            "errors": [f"Template file not found: {template_path}"]
        }

    try:
        with open(template_path, encoding='utf-8') as f:
            content = f.read()

        errors = []

        # Check for valid parameter syntax in expert initialization
        expert_init_match = re.search(r'expert = MetaExpert\((.*?)\)', content, re.DOTALL)
        if expert_init_match:
            expert_params = expert_init_match.group(1)
            # Check for basic parameter syntax
            if not re.search(r'[a-zA-Z_][a-zA-Z0-9_]*\s*=', expert_params):
                errors.append("Invalid parameter syntax in expert initialization")

        # Check for valid parameter syntax in on_init decorator
        on_init_match = re.search(r'@expert\.on_init\((.*?)\)', content, re.DOTALL)
        if on_init_match:
            init_params = on_init_match.group(1)
            # Check for basic parameter syntax
            if not re.search(r'[a-zA-Z_][a-zA-Z0-9_]*\s*=', init_params):
                errors.append("Invalid parameter syntax in on_init decorator")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Error reading template file: {e}"]
        }
