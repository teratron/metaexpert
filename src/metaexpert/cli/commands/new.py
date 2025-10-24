# src/metaexpert/cli/commands/new.py
"""Command to create new expert project."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from metaexpert.cli.app import get_config
from metaexpert.cli.core.exceptions import TemplateError, ValidationError
from metaexpert.cli.core.output import OutputFormatter, console
from metaexpert.cli.templates.generator import TemplateGenerator
from metaexpert.cli.utils.validators import validate_project_name


def cmd_new(
    project_name: Annotated[
        str,
        typer.Argument(help="Name of the new expert project"),
    ],
    exchange: Annotated[
        str,
        typer.Option("--exchange", "-e", help="Target exchange"),
    ] = "binance",
    strategy: Annotated[
        str,
        typer.Option(
            "--strategy", "-s", help="Strategy type (ema, rsi, macd, template)"
        ),
    ] = "template",
    market_type: Annotated[
        str,
        typer.Option("--market-type", help="Market type (spot, futures, options)"),
    ] = "futures",
    output_dir: Annotated[
        Optional[Path],
        typer.Option("--output-dir", "-o", help="Output directory"),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite existing directory"),
    ] = False,
) -> None:
    """
    Create a new trading expert project from template.

    Example:
        metaexpert new my-bot --exchange binance --strategy ema
    """
    config = get_config()
    output = OutputFormatter()

    # Validate project name
    try:
        validate_project_name(project_name)
    except ValueError as e:
        raise ValidationError(str(e))

    # Set output directory
    if output_dir is None:
        output_dir = Path.cwd()

    # Prepare template context
    context = {
        "exchange": exchange.lower(),
        "strategy": strategy.lower(),
        "market_type": market_type.lower(),
        "contract_type": "linear",  # Default for futures
        "margin_mode": "isolated",
        "position_mode": "hedge",
        "requires_passphrase": exchange.lower() in ["okx", "kucoin"],
        "leverage": 10,
        "stop_loss_pct": 2.0,
        "take_profit_pct": 4.0,
        "size_value": 1.5,
    }

    # Generate project
    try:
        generator = TemplateGenerator()

        console.print(f"\n[bold cyan]Creating project:[/] {project_name}")
        console.print(f"[dim]Exchange:[/] {exchange}")
        console.print(f"[dim]Strategy:[/] {strategy}")
        console.print(f"[dim]Market:[/] {market_type}\n")

        generator.generate_project(
            output_dir=output_dir,
            project_name=project_name,
            context=context,
            force=force,
        )

        project_path = output_dir / project_name

        # Display success message
        output.success(f"Project created at {project_path}")

        # Show next steps
        console.print("\n[bold green]Next Steps:[/]\n")
        console.print(f"  1. [cyan]cd {project_name}[/]")
        console.print(f"  2. [cyan]cp .env.example .env[/]  # Configure API keys")
        console.print(f"  3. [cyan]uv sync[/]  # Install dependencies")
        console.print(f"  4. [cyan]metaexpert run[/]  # Start in paper mode\n")

        console.print("[dim]Documentation: https://teratron.github.io/metaexpert[/]\n")

    except TemplateError as e:
        output.error(str(e))
        raise typer.Exit(code=1)
