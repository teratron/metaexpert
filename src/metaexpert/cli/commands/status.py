"""Status command for CLI."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.cli.process.manager import ProcessManager


def cmd_status(
    project_path: Annotated[
        Path,
        typer.Argument(
            help="Path to the project directory",
            exists=True,
            file_okay=False,
            dir_okay=True,
        ),
    ],
) -> None:
    """
    Show expert status.

    Args:
        project_path: Path to the project directory.
    """
    output = OutputFormatter()
    config = CLIConfig.load()
    manager = ProcessManager(config.pid_dir)

    # Get process info
    info = manager.get_info(project_path)
    if info is None:
        output.error("Project is not running or PID file not found.")
        raise typer.Exit(code=1)

    # Display status information
    data = [
        {
            "Property": "PID",
            "Value": str(info.pid),
        },
        {
            "Property": "Name",
            "Value": info.name,
        },
        {
            "Property": "Status",
            "Value": info.status,
        },
        {
            "Property": "CPU %",
            "Value": f"{info.cpu_percent:.1f}",
        },
        {
            "Property": "Memory (MB)",
            "Value": f"{info.memory_mb:.1f}",
        },
        {
            "Property": "Started",
            "Value": info.started_at.strftime("%Y-%m-%d %H:%M:%S"),
        },
        {
            "Property": "Working Directory",
            "Value": info.working_directory,
        },
        {
            "Property": "Command",
            "Value": info.command,
        },
    ]

    output.custom_table(data, columns=["Property", "Value"], title="Expert Status")
