"""Command to run an expert."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.cli.core.output import OutputFormatter, console
from metaexpert.cli.process.manager import ProcessManager


def cmd_run(
    project_path: Annotated[
        Path | None,
        typer.Argument(help="Path to expert project (default: current directory)"),
    ] = None,
    detach: Annotated[
        bool,
        typer.Option("--detach", "-d", help="Run in background"),
    ] = True,
    script: Annotated[
        str,
        typer.Option("--script", help="Script to run"),
    ] = "main.py",
    env_file: Annotated[
        Path | None,
        typer.Option("--env-file", "-e", help="Environment file to use"),
    ] = None,
    docker: Annotated[
        bool,
        typer.Option("--docker", help="Run in Docker container"),
    ] = False,
    notify: Annotated[
        bool,
        typer.Option("--notify", "-n", help="Send notifications on events"),
    ] = False,
    restart_on_error: Annotated[
        bool,
        typer.Option("--restart-on-error", help="Restart on error"),
    ] = False,
    max_restarts: Annotated[
        int,
        typer.Option("--max-restarts", help="Maximum restart attempts"),
    ] = 5,
) -> None:
    """
    Run a trading expert.

    Example:
        metaexpert run
        metaexpert run my-bot --detach
    """
    # Import dotenv if env_file is provided
    if env_file is not None:
        try:
            import dotenv
            dotenv.load_dotenv(env_file)
        except ImportError:
            console.print("[yellow]Warning:[/] python-dotenv not installed, ignoring --env-file")

    # Handle Docker execution
    if docker:
        # Placeholder for Docker execution logic
        console.print("[red]Error:[/] Docker execution is not yet implemented.")
        raise typer.Exit(code=1)

    config = get_config()
    output = OutputFormatter()

    # Default to current directory
    if project_path is None:
        project_path = Path.cwd()

    # Validate project
    if not project_path.is_dir():
        output.error(f"Project directory not found: {project_path}")
        raise typer.Exit(code=1)

    script_path = project_path / script
    if not script_path.exists():
        output.error(f"Script not found: {script_path}")
        raise typer.Exit(code=1)

    # Start process
    try:
        manager = ProcessManager(pid_dir=config.pid_dir)

        console.print(f"[cyan]Starting expert:[/] {project_path.name}")

        # Handle restart logic
        restart_count = 0
        while True:
            pid = manager.start(
                project_path=project_path,
                script=script,
                detach=detach,
            )

            output.success(f"Expert started with PID {pid}")

            if detach:
                console.print(f"\n[dim]Logs:[/] metaexpert logs {project_path.name}")
                console.print(f"[dim]Stop:[/] metaexpert stop {project_path.name}")
                console.print("[dim]Status:[/] metaexpert list\n")
            
            # If not detached, wait for process to finish
            if not detach:
                # Placeholder for waiting and monitoring logic
                # This would involve checking if the process is still running
                # and handling restarts if restart_on_error is True
                pass
            
            # Break the loop if we're not restarting or max restarts reached
            if not restart_on_error or restart_count >= max_restarts:
                break
                
            restart_count += 1
            console.print(f"[yellow]Restarting expert (attempt {restart_count}/{max_restarts})...[/]")

    except ProcessError as e:
        output.error(str(e))
        if notify:
            # Placeholder for notification logic
            console.print("[yellow]Notification:[/] Error notification would be sent here.")
        raise typer.Exit(code=1) from e
