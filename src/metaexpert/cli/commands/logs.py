# src/metaexpert/cli/commands/logs.py
"""Command to view expert logs."""

import time
from pathlib import Path
from typing import Annotated, Optional

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.output import OutputFormatter, console


def cmd_logs(
    project_name: Annotated[
        str,
        typer.Argument(help="Name of the expert project"),
    ],
    follow: Annotated[
        bool,
        typer.Option("--follow", "-f", help="Follow log output (like tail -f)"),
    ] = False,
    lines: Annotated[
        int,
        typer.Option("--lines", "-n", help="Number of lines to show"),
    ] = 50,
    level: Annotated[
        Optional[str],
        typer.Option("--level", "-l", help="Filter by log level (DEBUG, INFO, etc)"),
    ] = None,
) -> None:
    """
    View logs for an expert.

    Example:
        metaexpert logs my-bot
        metaexpert logs my-bot --follow
        metaexpert logs my-bot --level ERROR
    """
    config = get_config()
    output = OutputFormatter()

    log_file = config.log_dir / project_name / "expert.log"

    if not log_file.exists():
        output.error(f"Log file not found: {log_file}")
        output.info("Is the expert running?")
        raise typer.Exit(code=1)

    try:
        if follow:
            _tail_follow(log_file, level)
        else:
            _tail_lines(log_file, lines, level)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped tailing logs[/]")


def _tail_lines(log_file: Path, lines: int, level: Optional[str]) -> None:
    """Display last N lines of log file."""
    with open(log_file) as f:
        content = f.readlines()

        if level:
            content = [line for line in content if level.upper() in line]

        for line in content[-lines:]:
            console.print(line.rstrip())


def _tail_follow(log_file: Path, level: Optional[str]) -> None:
    """Follow log file in real-time."""
    with open(log_file) as f:
        # Seek to end
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            if level and level.upper() not in line:
                continue

            console.print(line.rstrip())

