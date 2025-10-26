from metaexpert.cli.app import app
from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.exceptions import (
    CLIError,
    ProcessError,
    ProjectError,
    TemplateError,
    ValidationError,
)
from metaexpert.cli.process.manager import ProcessManager
from metaexpert.cli.templates.generator import TemplateGenerator

__all__ = [
    "CLIConfig",
    "CLIError",
    "ProcessError",
    "ProcessManager",
    "ProjectError",
    "TemplateError",
    "TemplateGenerator",
    "ValidationError",
    "app",
]


def main() -> None:
    """Main entry point for CLI."""
    app()
