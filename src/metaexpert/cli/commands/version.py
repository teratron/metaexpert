"""Version command for CLI."""

import typer

from metaexpert.__version__ import __version__
from metaexpert.cli.core.output import OutputFormatter


def cmd_version(
    short: bool = typer.Option(False, "--short", "-s", help="Show only version number"),
) -> None:
    """
    Show CLI version.

    Args:
        short: Show only version number.
    """
    output = OutputFormatter()

    if short:
        output.info(__version__)
    else:
        output.success(f"MetaExpert CLI v{__version__}")
        output.info("A powerful cryptocurrency trading framework.")
        output.info("Documentation: https://teratron.github.io/metaexpert")
