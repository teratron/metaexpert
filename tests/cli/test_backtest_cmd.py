from typer.testing import CliRunner

from metaexpert.cli.main import app

runner = CliRunner()


def test_backtest_command_success(tmp_path):
    """Test the `backtest` command successfully processes an expert."""
    project_name = "test_expert_backtest_success"
    project_path = tmp_path / project_name
    project_path.mkdir()
    (project_path / "main.py").write_text("print('Backtest running')")

    result = runner.invoke(app, ["backtest", str(project_path)])

    assert result.exit_code == 0, result.stdout
    assert f"Attempting to backtest expert at: {project_path}" in result.stdout
    assert "Backtesting logic will be implemented here." in result.stdout


def test_backtest_command_project_not_found(tmp_path):
    """Test the `backtest` command fails if the project directory does not exist."""
    non_existent_path = tmp_path / "non_existent_project"
    result = runner.invoke(app, ["backtest", str(non_existent_path)])

    assert result.exit_code == 1
    assert f"Error: Project directory '{non_existent_path}' not found." in result.stdout


def test_backtest_command_main_py_not_found(tmp_path):
    """Test the `backtest` command fails if main.py is not found."""
    project_name = "test_expert_no_main_py_backtest"
    project_path = tmp_path / project_name
    project_path.mkdir()

    result = runner.invoke(app, ["backtest", str(project_path)])

    assert result.exit_code == 1
    assert f"Error: 'main.py' not found in '{project_path}'." in result.stdout
