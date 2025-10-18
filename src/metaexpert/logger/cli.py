"""CLI module for MetaExpert logging system configuration."""

import typer

from metaexpert.logger import MetaLogger

# Create a Typer app for the logging CLI
app = typer.Typer()


def add_logging_options(app: typer.Typer):
    """Add logging configuration options to a Typer application."""

    def logging_options(
        log_level: str | None = typer.Option(
            None,
            "--log-level",
            "-l",
            help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        ),
        log_directory: str | None = typer.Option(
            None, "--log-directory", help="Directory path for log files"
        ),
        expert_log_file: str | None = typer.Option(
            None, "--expert-log-file", help="Filename for expert logs"
        ),
        trades_log_file: str | None = typer.Option(
            None, "--trades-log-file", help="Filename for trades logs"
        ),
        errors_log_file: str | None = typer.Option(
            None, "--errors-log-file", help="Filename for errors logs"
        ),
        enable_async: bool | None = typer.Option(
            None, "--enable-async/--disable-async", help="Enable asynchronous logging"
        ),
        max_file_size_mb: int | None = typer.Option(
            None, "--max-file-size-mb", help="Maximum file size before rotation in MB"
        ),
        backup_count: int | None = typer.Option(
            None, "--backup-count", help="Number of backup files to keep"
        ),
        enable_structured_logging: bool | None = typer.Option(
            None,
            "--enable-structured-logging/--disable-structured-logging",
            help="Enable structured JSON logging",
        ),
        enable_contextual_logging: bool | None = typer.Option(
            None,
            "--enable-contextual-logging/--disable-contextual-logging",
            help="Enable contextual field inclusion",
        ),
        mask_sensitive_data: bool | None = typer.Option(
            None,
            "--mask-sensitive-data/--show-sensitive-data",
            help="Enable masking of sensitive information",
        ),
    ):
        """Wrapper that captures logging options."""
        # Return a dict of non-None options
        options = {}
        if log_level is not None:
            options["log_level"] = log_level
        if log_directory is not None:
            options["log_directory"] = log_directory
        if expert_log_file is not None:
            options["expert_log_file"] = expert_log_file
        if trades_log_file is not None:
            options["trades_log_file"] = trades_log_file
        if errors_log_file is not None:
            options["errors_log_file"] = errors_log_file
        if enable_async is not None:
            options["enable_async"] = enable_async
        if max_file_size_mb is not None:
            options["max_file_size_mb"] = max_file_size_mb
        if backup_count is not None:
            options["backup_count"] = backup_count
        if enable_structured_logging is not None:
            options["enable_structured_logging"] = enable_structured_logging
        if enable_contextual_logging is not None:
            options["enable_contextual_logging"] = enable_contextual_logging
        if mask_sensitive_data is not None:
            options["mask_sensitive_data"] = mask_sensitive_data

        return options

    return logging_options


@app.command()
def test_logging(
    # Add all the logging options to this command
    log_level: str | None = typer.Option(
        None,
        "--log-level",
        "-l",
        help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    ),
    log_directory: str | None = typer.Option(
        None, "--log-directory", help="Directory path for log files"
    ),
    expert_log_file: str | None = typer.Option(
        None, "--expert-log-file", help="Filename for expert logs"
    ),
    trades_log_file: str | None = typer.Option(
        None, "--trades-log-file", help="Filename for trades logs"
    ),
    errors_log_file: str | None = typer.Option(
        None, "--errors-log-file", help="Filename for errors logs"
    ),
    enable_async: bool | None = typer.Option(
        None, "--enable-async/--disable-async", help="Enable asynchronous logging"
    ),
    max_file_size_mb: int | None = typer.Option(
        None, "--max-file-size-mb", help="Maximum file size before rotation in MB"
    ),
    backup_count: int | None = typer.Option(
        None, "--backup-count", help="Number of backup files to keep"
    ),
    enable_structured_logging: bool | None = typer.Option(
        None,
        "--enable-structured-logging/--disable-structured-logging",
        help="Enable structured JSON logging",
    ),
    enable_contextual_logging: bool | None = typer.Option(
        None,
        "--enable-contextual-logging/--disable-contextual-logging",
        help="Enable contextual field inclusion",
    ),
    mask_sensitive_data: bool | None = typer.Option(
        None,
        "--mask-sensitive-data/--show-sensitive-data",
        help="Enable masking of sensitive information",
    ),
):
    """Test command to initialize logging with CLI options."""
    # Create options dict from CLI parameters
    cli_options = {}
    if log_level is not None:
        cli_options["log_level"] = log_level
    if log_directory is not None:
        cli_options["log_directory"] = log_directory
    if expert_log_file is not None:
        cli_options["expert_log_file"] = expert_log_file
    if trades_log_file is not None:
        cli_options["trades_log_file"] = trades_log_file
    if errors_log_file is not None:
        cli_options["errors_log_file"] = errors_log_file
    if enable_async is not None:
        cli_options["enable_async"] = enable_async
    if max_file_size_mb is not None:
        cli_options["max_file_size_mb"] = max_file_size_mb
    if backup_count is not None:
        cli_options["backup_count"] = backup_count
    if enable_structured_logging is not None:
        cli_options["enable_structured_logging"] = enable_structured_logging
    if enable_contextual_logging is not None:
        cli_options["enable_contextual_logging"] = enable_contextual_logging
    if mask_sensitive_data is not None:
        cli_options["mask_sensitive_data"] = mask_sensitive_data

    # Initialize logger with CLI options (these take highest priority)
    logger = MetaLogger(**cli_options)

    # Log a test message
    logger.info(
        "Logging system initialized via CLI",
        expert_name="CLITestExpert",
        symbol="CLITEST",
    )

    typer.echo("Logging system tested successfully with CLI parameters.")


if __name__ == "__main__":
    app()
