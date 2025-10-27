"""Command to list running experts."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.output import OutputFormatter
from metaexpert.cli.process.manager import ProcessManager


def cmd_list(
    search_path: Annotated[
        Path | None,
        typer.Option("--path", "-p", help="Search path for experts"),
    ] = None,
    format: Annotated[
        str,
        typer.Option("--format", "-f", help="Output format (table, json, yaml)"),
    ] = "table",
) -> None:
    """
    List all running experts.

    Example:
        metaexpert list
        metaexpert list --format json
    """
    config = get_config()
    output = OutputFormatter()

    if search_path is None:
        search_path = Path.cwd()

    manager = ProcessManager(pid_dir=config.pid_dir)
    running = manager.list_running(search_path)

    if not running:
        output.info("No running experts found")
        return

    # Prepare data for display
    data = [
        {
            "Name": info.name,
            "PID": info.pid,
            "Status": info.status,
            "CPU %": f"{info.cpu_percent:.1f}",
            "Memory (MB)": f"{info.memory_mb:.1f}",
            "Started": info.started_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for info in running
    ]

    # Display based on format
    if format == "json":
        output.display_json(data)
    elif format == "yaml":
        output.display_yaml(data)
    else:
        output.display_table(
            data,
            title="Running Experts",
            columns=["Name", "PID", "Status", "CPU %", "Memory (MB)", "Started"],
        )
