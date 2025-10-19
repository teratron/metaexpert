"""CLI command to backtest a trading expert."""

from pathlib import Path

import typer


def backtest_cmd(
    path: Path = typer.Argument(..., help="The path to the expert project directory."),
) -> None:
    """Backtests a trading expert."""
    if not path.is_dir():
        typer.secho(
            f"Error: Project directory '{path}' not found.", fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    main_script = path / "main.py"
    if not main_script.is_file():
        typer.secho(f"Error: 'main.py' not found in '{path}'.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho(f"Attempting to backtest expert at: {path}", fg=typer.colors.BLUE)
    typer.secho("Backtesting logic will be implemented here.", fg=typer.colors.YELLOW)
