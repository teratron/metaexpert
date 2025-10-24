"""CLI command to run a trading expert."""

import os
import subprocess
import sys
from pathlib import Path

import typer

from metaexpert.cli.pid_lock import (
    PidFileLock,
    cleanup_pid_file,
    get_pid_from_file,
    is_process_running,
)


def cmd_run(
    path: Path = typer.Argument(..., help="The path to the expert project directory."),
) -> None:
    """Runs a trading expert in a detached process."""
    if not path.is_dir():
        typer.secho(
            f"Error: Project directory '{path}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    main_script = path / "main.py"
    if not main_script.is_file():
        typer.secho(f"Error: 'main.py' not found in '{path}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    pid_file_path = path / ".metaexpert.pid"

    pid_from_file = get_pid_from_file(pid_file_path)
    if pid_from_file:
        if is_process_running(pid_from_file):
            typer.secho(
                f"Error: Expert at '{path}' is already running with PID {pid_from_file}.",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)
        else:
            typer.secho(
                f"Warning: Stale PID file found for PID {pid_from_file}. Removing.",
                fg=typer.colors.YELLOW,
            )
            cleanup_pid_file(pid_file_path)

    try:
        with PidFileLock(pid_file_path) as pid_lock:
            typer.secho(f"Starting expert at '{path}'...", fg=typer.colors.BLUE)

            # Use sys.executable to ensure the correct Python interpreter is used
            command = [sys.executable, str(main_script)]

            # Detach process
            if sys.platform == "win32":
                process = subprocess.Popen(
                    command,
                    cwd=path,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    close_fds=True,
                    creationflags=(
                        subprocess.DETACHED_PROCESS
                        | subprocess.CREATE_NEW_PROCESS_GROUP
                    ),
                )
            else:  # Unix-like systems
                process = subprocess.Popen(
                    command,
                    cwd=path,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    close_fds=True,
                    preexec_fn=os.setsid,
                )

            pid = process.pid
            # Write the actual child process PID to the locked file
            with open(pid_file_path, "w") as f:
                f.write(str(pid))

            pid_lock.keep_file = True  # Keep the PID file after successful startup

            typer.secho(
                f"Expert started with PID {pid}. Log file: {path}/expert.log",
                fg=typer.colors.GREEN,
            )
            typer.secho(
                f"To stop the expert, use: metaexpert stop {path}",
                fg=typer.colors.YELLOW,
            )

    except RuntimeError as e:  # PidFileLock raises RuntimeError if already locked
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from e
    except Exception as e:
        typer.secho(f"Error starting expert: {e}", fg=typer.colors.RED)
        if pid_file_path.exists():
            pid_file_path.unlink()  # Clean up PID file if creation failed
        raise typer.Exit(code=1) from e
