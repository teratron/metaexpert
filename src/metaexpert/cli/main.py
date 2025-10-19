import typer

from metaexpert.cli.backtest_cmd import backtest_cmd
from metaexpert.cli.list_cmd import list_cmd
from metaexpert.cli.logs_cmd import logs_cmd
from metaexpert.cli.new_cmd import new_cmd
from metaexpert.cli.run_cmd import run_cmd
from metaexpert.cli.stop_cmd import stop_cmd

app = typer.Typer(
    name="metaexpert",
    help="A CLI for managing trading experts.",
    no_args_is_help=True,
)

app.command("new")(new_cmd)
app.command("run")(run_cmd)
app.command("backtest")(backtest_cmd)
app.command("list")(list_cmd)
app.command("stop")(stop_cmd)
app.command("logs")(logs_cmd)
