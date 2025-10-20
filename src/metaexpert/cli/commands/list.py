"""CLI command to list running trading experts."""

from pathlib import Path

import typer

from metaexpert.cli.pid_lock import get_pid_from_file, is_process_running


def cmd_list(
    path: Path = typer.Argument(
        Path("."), help="The directory to search for expert projects."
    ),
) -> None:
    """Lists all running trading experts."""
    typer.secho("Searching for trading experts...", fg=typer.colors.BLUE)

    found_experts = []
    # Search in the specified directory for subdirectories that are expert projects
    for project_path in path.iterdir():
        if project_path.is_dir() and (project_path / "main.py").is_file():
            pid_file_path = project_path / ".metaexpert.pid"
            status = "Stopped"
            pid = "N/A"

            if pid_file_path.is_file():
                pid_val = get_pid_from_file(pid_file_path)
                if pid_val:
                    pid = str(pid_val)  # Ensure pid is a string for the table
                    if is_process_running(pid_val):
                        status = "Running"
                    else:
                        status = "Stale PID (Not Running)"
                else:
                    status = "Malformed PID File"

            found_experts.append(
                {
                    "name": project_path.name,
                    "path": project_path.resolve(),
                    "pid": pid,
                    "status": status,
                }
            )

    if not found_experts:
        typer.secho(
            "No trading experts found in the current directory.", fg=typer.colors.YELLOW
        )
        return

    # Print a formatted table
    typer.secho("\n--- Found Trading Experts ---", fg=typer.colors.CYAN)
    typer.secho(
        f"{'Project Name':<25} {'Path':<40} {'PID':<10} {'Status':<20}",
        fg=typer.colors.CYAN,
    )
    typer.secho(
        f"{'-' * 25:<25} {'-' * 40:<40} {'-' * 10:<10} {'-' * 20:<20}",
        fg=typer.colors.CYAN,
    )
    for expert in found_experts:
        typer.secho(
            f"{expert['name']:<25} {expert['path']!s:<40} {expert['pid']!s:<10} {expert['status']:<20}"
        )
