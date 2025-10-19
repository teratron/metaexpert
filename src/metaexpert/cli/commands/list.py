"""CLI command to list running trading experts."""

import os
import sys
from pathlib import Path

import typer


def _is_process_running(pid: int) -> bool:
    """Checks if a process with the given PID is currently running."""
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.WinDLL("kernel32")
            SYNCHRONIZE = 0x00100000
            PROCESS_QUERY_INFORMATION = 0x0400
            STILL_ACTIVE = 259

            process_handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | SYNCHRONIZE, 0, pid)
            if process_handle:
                exit_code = ctypes.c_ulong()
                kernel32.GetExitCodeProcess(process_handle, ctypes.byref(exit_code))
                kernel32.CloseHandle(process_handle)
                return exit_code.value == STILL_ACTIVE
            else:
                # Check if access was denied (e.g., for system processes)
                if kernel32.GetLastError() == 5:  # ERROR_ACCESS_DENIED
                    return True  # Assume it's running if access is denied
                return False
        except Exception:
            return False
    else:  # Unix-like systems
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def cmd_list(
        path: Path = typer.Argument(Path("."), help="The directory to search for expert projects."),
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
                try:
                    with open(pid_file_path) as f:
                        pid_str = f.read().strip()
                        pid = int(pid_str)
                        if _is_process_running(pid):
                            status = "Running"
                        else:
                            status = "Stale PID (Not Running)"
                            # Optionally, remove stale PID file here
                            # pid_file_path.unlink()
                except (OSError, ValueError):
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
