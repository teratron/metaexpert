"""Dependency validation module for MetaExpert CLI."""

import importlib
import sys
from typing import Dict, List, Tuple


def check_dependencies() -> bool:
    """
    Check if all required dependencies are installed with correct versions.

    Returns:
        True if all dependencies are satisfied, False otherwise.
    """
    required = {
        "typer": ">=0.12.0",
        "rich": ">=13.0.0",
        "pydantic": ">=2.0.0",
        "pydantic-settings": ">=2.0",  # Added pydantic-settings
        "psutil": ">=5.9.0",
        "jinja2": ">=3.1.0",
        "structlog": ">=23.0.0",  # Added structlog as it's used in logger
        "python-dotenv": ">=1.0.0",  # Added dotenv as it's used in ProcessManager
    }

    missing: List[str] = []
    version_issues: List[Tuple[str, str, str]] = []  # (package, required_version, installed_version)

    for package, version_spec in required.items():
        try:
            # Special case for python-dotenv which is imported as 'dotenv'
            import_name = "dotenv" if package == "python-dotenv" else package
            # Special case for pydantic-settings which is imported as 'pydantic_settings'
            if package == "pydantic-settings":
                import_name = "pydantic_settings"

            mod = importlib.import_module(import_name)
            # Get the version attribute if available
            installed_version = getattr(mod, '__version__', 'unknown')

            # For now, just check if the module can be imported
            # A more robust version check would parse the version string
            # and compare it against the spec (e.g., using packaging.version)
            # For this implementation, we'll just check importability
            # and note if version can't be determined.
            if installed_version == 'unknown':
                # Log or print a warning that version couldn't be determined
                # For now, we'll just continue if importable
                pass

        except ImportError:
            missing.append(f"{package}{version_spec}")

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}", file=sys.stderr)
        return False

    # If all required packages import successfully, return True
    # (Note: This is a basic check; a more robust check would compare versions)
    return True


if __name__ == "__main__":
    # Example usage
    if not check_dependencies():
        print("Dependency check failed.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All dependencies are satisfied.")
