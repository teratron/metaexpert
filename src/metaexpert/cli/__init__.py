from metaexpert.cli.app import app
from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.exceptions import (
    CLIError,
    ProcessError,
    ProjectError,
    TemplateError,
    ValidationError,
)
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.cli.process.manager import ProcessManager
from metaexpert.cli.templates.generator import TemplateGenerator
from metaexpert.cli.utils.validators import (
    validate_exchange_name,
    validate_project_name,
)

__all__ = [
    "CLIConfig",
    "CLIError",
    "OutputFormatter",
    "ProcessError",
    "ProcessManager",
    "ProjectError",
    "TemplateError",
    "TemplateGenerator",
    "ValidationError",
    "app",
    "validate_exchange_name",
    "validate_project_name",
]


def register_commands() -> None:
    """Register all CLI commands."""
    from metaexpert.cli.commands import backtest, init, list, logs, new, run, stop

    app.command(name="new")(new.cmd_new)
    app.command(name="run")(run.cmd_run)
    app.command(name="backtest")(backtest.cmd_backtest)
    app.command(name="list")(list.cmd_list)
    app.command(name="stop")(stop.cmd_stop)
    app.command(name="logs")(logs.cmd_logs)
    app.command(name="init")(init.cmd_init)


def main() -> None:
    """Main entry point for CLI."""
    register_commands()
    app()
