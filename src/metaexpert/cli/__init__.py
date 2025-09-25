"""CLI module for MetaExpert."""

from .argument_parser import parse_arguments
from .endpoint import parse_cli_arguments
from .template_commands import add_template_commands

# Public API exports
__all__ = [
    "add_template_commands",
    "parse_arguments",
    "parse_cli_arguments",
]
