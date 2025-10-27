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
    from metaexpert.cli.commands import (
        backtest,
        clean,
        config,
        doctor,
        export,
        import_,
        init,
        list,
        logs,
        new,
        run,
        status,
        stop,
        version,
    )

    app.command(name="new")(new.cmd_new)
    app.command(name="run")(run.cmd_run)
    app.command(name="backtest")(backtest.cmd_backtest)
    app.command(name="list")(list.cmd_list)
    app.command(name="stop")(stop.cmd_stop)
    app.command(name="logs")(logs.cmd_logs)
    app.command(name="init")(init.cmd_init)
    app.command(name="status")(status.cmd_status)
    app.command(name="config")(config.cmd_config)
    app.command(name="doctor")(doctor.cmd_doctor)
    app.command(name="version")(version.cmd_version)
    app.command(name="clean")(clean.cmd_clean)
    app.command(name="export")(export.cmd_export)
    app.command(name="import")(import_.cmd_import)


def main() -> None:
    """Main entry point for CLI."""
    register_commands()
    app()
