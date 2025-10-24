# src/metaexpert/cli/core/exceptions.py
"""CLI-specific exceptions."""

from typing import Optional


class CLIError(Exception):
    """Base exception for CLI errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class ProjectError(CLIError):
    """Error related to project operations."""

    pass


class ProcessError(CLIError):
    """Error related to process management."""

    pass


class TemplateError(CLIError):
    """Error related to template generation."""

    pass


class ValidationError(CLIError):
    """Error related to input validation."""

    pass

