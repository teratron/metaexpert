"""CLI command to stop a running trading expert."""

from pathlib import Path

import typer

from metaexpert.cli.pid_lock import (
    cleanup_pid_file,
    get_pid_from_file,
    terminate_process,
)


def cmd_stop(
    path: Path = typer.Argument(..., help="The path to the expert project directory."),
) -> None:
    """Stops a running trading expert."""
    if not path.is_dir():
        typer.secho(
            f"Error: Project directory '{path}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    pid_file_path = path / ".metaexpert.pid"
    pid = get_pid_from_file(pid_file_path)

    if pid is None:
        typer.secho(
            f"Error: PID file not found at '{pid_file_path}'. Is the expert running?",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.secho(
        f"Attempting to stop expert with PID {pid} at '{path}'...", fg=typer.colors.BLUE
    )

    try:
        terminate_process(pid)
        typer.secho(
            f"Successfully stopped process {pid}. PID file removed.",
            fg=typer.colors.GREEN,
        )
    except ProcessLookupError:
        typer.secho(
            f"Warning: Process with PID {pid} not found. PID file was stale. Removing it.",
            fg=typer.colors.YELLOW,
        )
    except OSError as e:
        typer.secho(f"Error stopping expert with PID {pid}: {e}", fg=typer.colors.RED)
        cleanup_pid_file(pid_file_path)
        raise typer.Exit(code=1) from e
    finally:
        cleanup_pid_file(pid_file_path)
