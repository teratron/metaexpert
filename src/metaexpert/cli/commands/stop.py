"""Command to stop an expert."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.cli.process.manager import ProcessManager


def cmd_stop(
    project_name: Annotated[
        str,
        typer.Argument(help="Name of the expert project to stop"),
    ],
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Force kill the process"),
    ] = False,
    timeout: Annotated[
        int,
        typer.Option("--timeout", "-t", help="Shutdown timeout in seconds"),
    ] = 30,
) -> None:
    """
    Stop a running expert.

    Example:
        metaexpert stop my-bot
        metaexpert stop my-bot --force
    """
    config = get_config()
    output = OutputFormatter()

    project_path = Path.cwd() / project_name

    try:
        manager = ProcessManager(pid_dir=config.pid_dir)

        output.info(f"Stopping expert: {project_name}")

        manager.stop(
            project_path=project_path,
            timeout=timeout,
            force=force,
        )

        output.success(f"Expert stopped: {project_name}")

    except ProcessError as e:
        output.error(str(e))
        raise typer.Exit(code=1) from e
