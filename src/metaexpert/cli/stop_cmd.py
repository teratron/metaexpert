"""CLI command to stop a running trading expert."""

import os
import signal
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import typer

from metaexpert.cli.pid_lock import PidFileLock  # Import the new utility


def stop_cmd(
    path: Path = typer.Argument(..., help="The path to the expert project directory."),
) -> None:
    """Stops a running trading expert."""
    if not path.is_dir():
        typer.secho(
            f"Error: Project directory '{path}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    pid_file_path = path / ".metaexpert.pid"

    if not pid_file_path.is_file():
        typer.secho(
            f"Error: PID file not found for expert at '{path}'. Is it running?",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    try:
        with open(pid_file_path) as f:
            pid = int(f.read().strip())
    except (OSError, ValueError):
        typer.secho(
            f"Error: Malformed PID file found at '{pid_file_path}'.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    typer.secho(
        f"Attempting to stop expert with PID {pid} at '{path}'...", fg=typer.colors.BLUE
    )

    try:
        if sys.platform == "win32":
            result = subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)
            if result.returncode != 0:
                # Check if the error is due to process not found
                if f"No running instance of the task with PID {pid} was found." in result.stderr.decode():
                    raise ProcessLookupError
                else:
                    # Re-raise other taskkill errors
                    raise Exception(f"taskkill failed: {result.stderr.decode()}")
        else:
            os.kill(pid, signal.SIGTERM)
        typer.secho(
            f"Sent SIGTERM to process {pid}. PID file removed.",
            fg=typer.colors.GREEN,
        )
        if pid_file_path.exists():
            pid_file_path.unlink()
    except ProcessLookupError:
        typer.secho(
            f"Warning: Process with PID {pid} not found. PID file was stale. Removing it.",
            fg=typer.colors.YELLOW,
        )
        if pid_file_path.exists():
            pid_file_path.unlink()
        raise typer.Exit(code=0)  # Exit with 0 as the process is effectively stopped
    except Exception as e:
        typer.secho(f"Error stopping expert with PID {pid}: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from e
