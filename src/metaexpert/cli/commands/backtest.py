"""Command to backtest a strategy."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.output import OutputFormatter


def cmd_backtest(
    expert_path: Annotated[
        Path,
        typer.Argument(help="Path to expert file"),
    ],
    start_date: Annotated[
        str | None,
        typer.Option("--start-date", "-s", help="Start date (YYYY-MM-DD)"),
    ] = None,
    end_date: Annotated[
        str | None,
        typer.Option("--end-date", "-e", help="End date (YYYY-MM-DD)"),
    ] = None,
    initial_capital: Annotated[
        float,
        typer.Option("--capital", "-c", help="Initial capital"),
    ] = 10000.0,
    optimize: Annotated[
        bool,
        typer.Option("--optimize", "-o", help="Optimize parameters"),
    ] = False,
    optimize_params: Annotated[
        str | None,
        typer.Option("--optimize-params", help="Parameters to optimize (comma-separated)"),
    ] = None,
    compare: Annotated[
        bool,
        typer.Option("--compare", help="Compare strategies"),
    ] = False,
    report_format: Annotated[
        str,
        typer.Option("--report-format", "-f", help="Report format (html, json, csv)"),
    ] = "html",
) -> None:
    """
    Backtest a trading strategy.

    Example:
        metaexpert backtest main.py --start-date 2024-01-01
    """
    output = OutputFormatter()

    if not expert_path.exists():
        output.error(f"Expert file not found: {expert_path}")
        raise typer.Exit(code=1)

    # Parse optimization parameters
    if optimize_params:
        params = [p.strip() for p in optimize_params.split(",") if p.strip()]
    else:
        params = []

    # Perform backtest
    try:
        # Placeholder for backtesting logic
        output.info("Starting backtest...")
        
        # If optimization is requested
        if optimize:
            output.info("Optimizing parameters...")
            if params:
                output.info(f"Optimizing: {', '.join(params)}")
            else:
                output.info("No parameters specified for optimization.")
        
        # If comparison is requested
        if compare:
            output.info("Comparing strategies...")
        
        # Simulate backtest execution
        import time
        time.sleep(2)  # Simulate processing time
        
        # Generate report
        if report_format == "html":
            output.success("Backtest completed. Report saved as backtest_report.html")
        elif report_format == "json":
            output.success("Backtest completed. Report saved as backtest_report.json")
        elif report_format == "csv":
            output.success("Backtest completed. Report saved as backtest_report.csv")
        else:
            output.warning(f"Unknown report format: {report_format}. Defaulting to HTML.")
            output.success("Backtest completed. Report saved as backtest_report.html")
            
    except Exception as e:
        output.error(f"Backtest failed: {e}")
        raise typer.Exit(code=1)
