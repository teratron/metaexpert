"""Error handling module for MetaExpert CLI."""

# Import order is important to avoid circular imports
# We import types first, then other modules that depend on them

# Import types
# Import dataclasses
from metaexpert.cli.core.errors.context import ErrorContext
from metaexpert.cli.core.errors.handler import ErrorHandler

# Import classes
from metaexpert.cli.core.errors.recovery import RecoveryStrategy

# Import enums
from metaexpert.cli.core.errors.severity import ErrorSeverity
from metaexpert.cli.core.errors.types import (
    CLIError,
    ProcessError,
    ProjectError,
    TemplateError,
    ValidationError,
)

__all__ = [
    "CLIError",
    "ErrorContext",
    "ErrorHandler",
    "ErrorSeverity",
    "ProcessError",
    "ProjectError",
    "RecoveryStrategy",
    "TemplateError",
    "ValidationError",
]
