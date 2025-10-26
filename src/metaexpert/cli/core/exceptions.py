# src/metaexpert/cli/core/exceptions.py
"""CLI-specific exceptions."""


class CLIError(Exception):
    """Base exception for CLI errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class ConfigError(CLIError):
    """Error related to configuration issues."""

    def __init__(self, message: str, config_file: str | None = None) -> None:
        super().__init__(message)
        self.config_file = config_file


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


class CommandError(CLIError):
    """Error related to command execution."""

    pass


class ExecutionError(CLIError):
    """Error related to process execution."""

    pass


class PIDLockError(CLIError):
    """Error related to process ID lock management."""

    pass


class OutputFormatError(CLIError):
    """Error related to output formatting."""

    pass


class ArgumentError(CLIError):
    """Error related to command-line argument parsing."""

    pass


class EnvironmentError(CLIError):
    """Error related to environment configuration."""

    pass
