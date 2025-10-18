import typer
from metaexpert.cli.new_cmd import new_cmd

app = typer.Typer(
    name="metaexpert",
    help="A CLI for managing trading experts.",
    no_args_is_help=True,
)

app.command("new")(new_cmd)
