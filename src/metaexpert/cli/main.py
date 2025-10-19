import typer

from metaexpert.cli.commands.backtest import cmd_backtest
from metaexpert.cli.commands.list import cmd_list
from metaexpert.cli.commands.logs import cmd_logs
from metaexpert.cli.commands.new import cmd_new
from metaexpert.cli.commands.run import cmd_run
from metaexpert.cli.commands.stop import cmd_stop

app = typer.Typer(
    name="metaexpert",
    help="A CLI for managing trading experts.",
    no_args_is_help=True,
)

app.command("new")(cmd_new)
app.command("run")(cmd_run)
app.command("backtest")(cmd_backtest)
app.command("list")(cmd_list)
app.command("stop")(cmd_stop)
app.command("logs")(cmd_logs)
