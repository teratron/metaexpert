"""Main Typer application with proper structure."""

import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from metaexpert.__version__ import __version__
from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.exceptions import CLIError
from metaexpert.cli.core.output import OutputFormatter, console, error_console

# Initialize Typer app with rich output
app = typer.Typer(
    name="metaexpert",
    help="CLI for managing MetaExpert trading bots",
    add_completion=True,
    rich_markup_mode="rich",
    pretty_exceptions_enable=True,
)

# Global state for CLI configuration
_config: Optional[CLIConfig] = None


def get_config() -> CLIConfig:
    """Get or create CLI configuration."""
    global _config
    if _config is None:
        _config = CLIConfig.load()
    return _config


def version_callback(value: bool) -> None:
    """Display version and exit."""
    if value:
        console.print(f"[bold green]MetaExpert[/] version [cyan]{__version__}[/]")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            help="Enable verbose output",
        ),
    ] = False,
) -> None:
    """
    MetaExpert CLI - Manage your trading bots with ease.

    Use [bold]metaexpert COMMAND --help[/] for command-specific help.
    """
    config = get_config()
    config.verbose = verbose


# Import and register command modules
from metaexpert.cli.commands import backtest, list, logs, new, run, stop

app.command(name="new")(new.cmd_new)
app.command(name="run")(run.cmd_run)
app.command(name="backtest")(backtest.cmd_backtest)
app.command(name="list")(list.cmd_list)
app.command(name="stop")(stop.cmd_stop)
app.command(name="logs")(logs.cmd_logs)


# Error handler
@app.command(hidden=True)
def _handle_error(error: Exception) -> None:
    """Internal error handler."""
    if isinstance(error, CLIError):
        error_console.print(f"[red]Error:[/] {error}")
        raise typer.Exit(code=1)
    raise


if __name__ == "__main__":
    app()
