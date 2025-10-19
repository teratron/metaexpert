"""CLI command to view expert logs."""

import re
import time
from pathlib import Path

import typer


def cmd_logs(
        path: Path = typer.Argument(..., help="The path to the expert project directory."),
        level: str = typer.Option(
            None, "--level", "-l", help="Filter logs by level (e.g., INFO, WARNING, ERROR)."
        ),
) -> None:
    """Views logs for a trading expert."""
    if not path.is_dir():
        typer.secho(
            f"Error: Project directory '{path}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    log_file_path = path / "expert.log"

    if not log_file_path.is_file():
        typer.secho(
            f"Error: Log file '{log_file_path}' not found. Is the expert running?",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.secho(f"Tailing logs for expert at: {path}", fg=typer.colors.BLUE)
    if level:
        typer.secho(f"Filtering by level: {level}", fg=typer.colors.BLUE)

    # Regex to match log level (e.g., INFO, WARNING, ERROR)
    # Assumes log format like: [TIMESTAMP] [LEVEL] MESSAGE
    level_pattern = re.compile(r"\[(INFO|WARNING|ERROR|DEBUG)\]")

    try:
        with open(log_file_path) as f:
            # Seek to the end of the file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Wait a bit before trying again
                    continue

                if level:
                    match = level_pattern.search(line)
                    if match and match.group(1).upper() == level.upper():
                        typer.echo(line.strip())
                else:
                    typer.echo(line.strip())
    except KeyboardInterrupt:
        typer.secho("\nStopped tailing logs.", fg=typer.colors.YELLOW)
    except Exception as e:
        typer.secho(f"Error reading log file: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from e
