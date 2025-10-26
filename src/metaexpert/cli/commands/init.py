# src/metaexpert/cli/commands/init.py
"""Command to initialize MetaExpert CLI environment."""

from pathlib import Path
from typing import Annotated

import typer

from metaexpert.cli.core.config import CLIConfig
from metaexpert.cli.core.output import OutputFormatter


def cmd_init(
    interactive: Annotated[
        bool,
        typer.Option("--interactive", "-i", help="Interactive setup"),
    ] = True,
) -> None:
    """
    Initialize MetaExpert CLI environment.

    Example:
        metaexpert init --interactive
    """
    output = OutputFormatter()

    # Load existing config or create default
    config = CLIConfig.load()

    if interactive:
        # Interactive setup
        output.info("Starting interactive setup for MetaExpert CLI")

        # Get default exchange
        current_exchange = config.default_exchange
        exchange = typer.prompt(
            "Default exchange",
            default=current_exchange,
        )
        config.default_exchange = exchange

        # Get default strategy
        current_strategy = config.default_strategy
        strategy = typer.prompt(
            "Default strategy",
            default=current_strategy,
        )
        config.default_strategy = strategy

        # Get timeout
        current_timeout = config.default_timeout
        timeout = typer.prompt(
            "Default timeout for operations (seconds)",
            default=current_timeout,
            type=int,
        )
        config.default_timeout = timeout

        # Get log level
        current_log_level = config.log_level
        log_level = typer.prompt(
            "Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
            default=current_log_level,
        )
        config.log_level = log_level.upper()

        # Get output format
        current_format = config.output_format
        output_format = typer.prompt(
            "Default output format (table, json, csv)",
            default=current_format,
        )
        config.output_format = output_format

        # Ask about color output
        current_no_color = config.no_color
        no_color = typer.confirm(
            "Disable colored output?",
            default=current_no_color,
        )
        config.no_color = no_color

        # Ask about cache
        current_cache_enabled = config.cache_enabled
        cache_enabled = typer.confirm(
            "Enable caching?",
            default=current_cache_enabled,
        )
        config.cache_enabled = cache_enabled

        # Ask about verbose mode
        current_verbose = config.verbose
        verbose = typer.confirm(
            "Enable verbose output by default?",
            default=current_verbose,
        )
        config.verbose = verbose

        # Ask about debug mode
        current_debug = config.debug
        debug = typer.confirm(
            "Enable debug mode?",
            default=current_debug,
        )
        config.debug = debug

        output.success("Configuration completed")
    else:
        # Non-interactive setup - just save the default config
        output.info("Initializing with default configuration")

    # Ensure necessary directories exist
    config.pid_dir.mkdir(parents=True, exist_ok=True)
    if config.log_dir:
        config.log_dir.mkdir(parents=True, exist_ok=True)

    # Save the configuration
    config_path = Path.home() / ".metaexpert"
    config.save(config_path)

    output.success(
        f"CLI initialized successfully. Configuration saved to {config_path}"
    )
