# src/metaexpert/cli/commands/run.py
"""Command to run an expert."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.cli.core.output import OutputFormatter, console
from metaexpert.cli.process.manager import ProcessManager


def cmd_run(
    project_path: Annotated[
        Path | None,
        typer.Argument(help="Path to expert project (default: current directory)"),
    ] = None,
    detach: Annotated[
        bool,
        typer.Option("--detach", "-d", help="Run in background"),
    ] = True,
    script: Annotated[
        str,
        typer.Option("--script", help="Script to run"),
    ] = "main.py",
) -> None:
    """
    Run a trading expert.

    Example:
        metaexpert run
        metaexpert run my-bot --detach
    """
    config = get_config()
    output = OutputFormatter()

    # Default to current directory
    if project_path is None:
        project_path = Path.cwd()

    # Validate project
    if not project_path.is_dir():
        output.error(f"Project directory not found: {project_path}")
        raise typer.Exit(code=1)

    script_path = project_path / script
    if not script_path.exists():
        output.error(f"Script not found: {script_path}")
        raise typer.Exit(code=1)

    # Start process
    try:
        manager = ProcessManager(pid_dir=config.pid_dir)

        console.print(f"[cyan]Starting expert:[/] {project_path.name}")

        pid = manager.start(
            project_path=project_path,
            script=script,
            detach=detach,
        )

        output.success(f"Expert started with PID {pid}")

        if detach:
            console.print(f"\n[dim]Logs:[/] metaexpert logs {project_path.name}")
            console.print(f"[dim]Stop:[/] metaexpert stop {project_path.name}")
            console.print("[dim]Status:[/] metaexpert list\n")

    except ProcessError as e:
        output.error(str(e))
        raise typer.Exit(code=1) from e
