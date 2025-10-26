"""Tests for CLI-specific exceptions."""

from metaexpert.cli.core.exceptions import (
    ArgumentError,
    CLIError,
    CommandError,
    ConfigError,
    EnvironmentError,
    ExecutionError,
    OutputFormatError,
    PIDLockError,
    ProcessError,
    ProjectError,
    TemplateError,
    ValidationError,
)


def test_cli_error_inheritance_from_exception() -> None:
    """Test that CLIError inherits from base Exception."""
    error = CLIError("Test error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)


def test_cli_error_default_exit_code() -> None:
    """Test CLIError default exit code."""
    error = CLIError("Test error")
    assert str(error) == "Test error"
    assert error.exit_code == 1


def test_cli_error_custom_exit_code() -> None:
    """Test CLIError with custom exit code."""
    error = CLIError("Custom error", exit_code=2)
    assert str(error) == "Custom error"
    assert error.exit_code == 2


def test_config_error_inheritance_from_exception() -> None:
    """Test that ConfigError inherits from base Exception."""
    error = ConfigError("Config error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ConfigError)


def test_config_error_inheritance() -> None:
    """Test ConfigError inherits from CLIError."""
    error = ConfigError("Config error")
    assert isinstance(error, CLIError)
    assert str(error) == "Config error"
    assert error.exit_code == 1


def test_config_error_with_config_file() -> None:
    """Test ConfigError with config file parameter."""
    error = ConfigError("Config error", config_file="test_config.yaml")
    assert str(error) == "Config error"
    assert error.config_file == "test_config.yaml"
    assert error.exit_code == 1


def test_config_error_without_config_file() -> None:
    """Test ConfigError without config file parameter."""
    error = ConfigError("Config error")
    assert str(error) == "Config error"
    assert error.config_file is None
    assert error.exit_code == 1


def test_process_error_inheritance_from_exception() -> None:
    """Test that ProcessError inherits from base Exception."""
    error = ProcessError("Process error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ProcessError)


def test_process_error_inheritance() -> None:
    """Test ProcessError inherits from CLIError."""
    error = ProcessError("Process error")
    assert isinstance(error, CLIError)
    assert str(error) == "Process error"
    assert error.exit_code == 1


def test_project_error_inheritance_from_exception() -> None:
    """Test that ProjectError inherits from base Exception."""
    error = ProjectError("Project error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ProjectError)


def test_project_error_inheritance() -> None:
    """Test ProjectError inherits from CLIError."""
    error = ProjectError("Project error")
    assert isinstance(error, CLIError)
    assert str(error) == "Project error"
    assert error.exit_code == 1


def test_template_error_inheritance_from_exception() -> None:
    """Test that TemplateError inherits from base Exception."""
    error = TemplateError("Template error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, TemplateError)


def test_template_error_inheritance() -> None:
    """Test TemplateError inherits from CLIError."""
    error = TemplateError("Template error")
    assert isinstance(error, CLIError)
    assert str(error) == "Template error"
    assert error.exit_code == 1


def test_validation_error_inheritance_from_exception() -> None:
    """Test that ValidationError inherits from base Exception."""
    error = ValidationError("Validation error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ValidationError)


def test_validation_error_inheritance() -> None:
    """Test ValidationError inherits from CLIError."""
    error = ValidationError("Validation error")
    assert isinstance(error, CLIError)
    assert str(error) == "Validation error"
    assert error.exit_code == 1


def test_command_error_inheritance_from_exception() -> None:
    """Test that CommandError inherits from base Exception."""
    error = CommandError("Command error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, CommandError)


def test_command_error_inheritance() -> None:
    """Test CommandError inherits from CLIError."""
    error = CommandError("Command error")
    assert isinstance(error, CLIError)
    assert str(error) == "Command error"
    assert error.exit_code == 1


def test_execution_error_inheritance_from_exception() -> None:
    """Test that ExecutionError inherits from base Exception."""
    error = ExecutionError("Execution error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ExecutionError)


def test_execution_error_inheritance() -> None:
    """Test ExecutionError inherits from CLIError."""
    error = ExecutionError("Execution error")
    assert isinstance(error, CLIError)
    assert str(error) == "Execution error"
    assert error.exit_code == 1


def test_pidlock_error_inheritance_from_exception() -> None:
    """Test that PIDLockError inherits from base Exception."""
    error = PIDLockError("PID lock error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, PIDLockError)


def test_pidlock_error_inheritance() -> None:
    """Test PIDLockError inherits from CLIError."""
    error = PIDLockError("PID lock error")
    assert isinstance(error, CLIError)
    assert str(error) == "PID lock error"
    assert error.exit_code == 1


def test_outputformat_error_inheritance_from_exception() -> None:
    """Test that OutputFormatError inherits from base Exception."""
    error = OutputFormatError("Output format error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, OutputFormatError)


def test_outputformat_error_inheritance() -> None:
    """Test OutputFormatError inherits from CLIError."""
    error = OutputFormatError("Output format error")
    assert isinstance(error, CLIError)
    assert str(error) == "Output format error"
    assert error.exit_code == 1


def test_argument_error_inheritance_from_exception() -> None:
    """Test that ArgumentError inherits from base Exception."""
    error = ArgumentError("Argument error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, ArgumentError)


def test_argument_error_inheritance() -> None:
    """Test ArgumentError inherits from CLIError."""
    error = ArgumentError("Argument error")
    assert isinstance(error, CLIError)
    assert str(error) == "Argument error"
    assert error.exit_code == 1


def test_environment_error_inheritance_from_exception() -> None:
    """Test that EnvironmentError inherits from base Exception."""
    error = EnvironmentError("Environment error")
    assert isinstance(error, Exception)
    assert isinstance(error, CLIError)
    assert isinstance(error, EnvironmentError)


def test_environment_error_inheritance() -> None:
    """Test EnvironmentError inherits from CLIError."""
    error = EnvironmentError("Environment error")
    assert isinstance(error, CLIError)
    assert str(error) == "Environment error"
    assert error.exit_code == 1


def test_error_message_formatting() -> None:
    """Test proper error message formatting for all exception types."""
    error_classes = [
        CLIError,
        ConfigError,
        ProcessError,
        ProjectError,
        TemplateError,
        ValidationError,
        CommandError,
        ExecutionError,
        PIDLockError,
        OutputFormatError,
        ArgumentError,
        EnvironmentError,
    ]

    for error_class in error_classes:
        error = error_class("Test message")
        assert str(error) == "Test message"
        assert len(str(error)) > 0
        assert isinstance(str(error), str)


def test_cli_error_with_empty_message() -> None:
    """Test CLIError with empty message."""
    error = CLIError("")
    assert str(error) == ""
    assert error.exit_code == 1


def test_subclass_error_with_empty_message() -> None:
    """Test subclasses with empty message."""
    error_classes = [
        ConfigError,
        ProcessError,
        ProjectError,
        TemplateError,
        ValidationError,
        CommandError,
        ExecutionError,
        PIDLockError,
        OutputFormatError,
        ArgumentError,
        EnvironmentError,
    ]

    for error_class in error_classes:
        error = error_class("")
        assert str(error) == ""
        assert error.exit_code == 1


def test_cli_error_with_special_characters() -> None:
    """Test CLIError with special characters in message."""
    special_message = "Error with special chars: !@#$%^&*()_+-={}[]|\\:\";'<>?,./"
    error = CLIError(special_message)
    assert str(error) == special_message


def test_all_exceptions_are_catchable_as_base_exception() -> None:
    """Test that all CLI exceptions can be caught as base Exception."""
    error_classes = [
        CLIError,
        ConfigError,
        ProcessError,
        ProjectError,
        TemplateError,
        ValidationError,
        CommandError,
        ExecutionError,
        PIDLockError,
        OutputFormatError,
        ArgumentError,
        EnvironmentError,
    ]

    for error_class in error_classes:
        try:
            raise error_class("Test error")
        except Exception:
            pass  # Successfully caught as base Exception
        else:
            raise AssertionError(
                f"{error_class.__name__} was not caught as base Exception"
            )
