from pathlib import Path

from typer.testing import CliRunner

from metaexpert.cli.main import app

runner = CliRunner()


def test_new_command_success(tmp_path):
    """Test the `new` command successfully creates a project."""
    project_name = "test_project_success"
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(app, ["new", project_name])

        assert result.exit_code == 0, result.stdout
        assert f"Successfully created new expert '{project_name}'" in result.stdout

        project_path = Path(td) / project_name
        assert project_path.is_dir()
        assert (project_path / "main.py").is_file()
        assert (project_path / "pyproject.toml").is_file()


def test_new_command_already_exists_error(tmp_path):
    """Test the `new` command fails if the directory already exists."""
    project_name = "test_project_exists"
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        project_path = Path(td) / project_name
        project_path.mkdir()

        result = runner.invoke(app, ["new", project_name])

        assert result.exit_code == 1, result.stdout
        assert f"Error: Directory '{project_name}' already exists." in result.stdout


def test_new_command_force_overwrite(tmp_path):
    """Test the `new` command overwrites with --force."""
    project_name = "test_project_force"
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        project_path = Path(td) / project_name
        project_path.mkdir()
        (project_path / "old_file.txt").touch()

        result = runner.invoke(app, ["new", project_name, "--force"])

        assert result.exit_code == 0, result.stdout
        assert (
            f"Warning: Overwriting existing directory '{project_name}'" in result.stdout
        )
        assert not (project_path / "old_file.txt").exists()
        assert (project_path / "main.py").is_file()


def test_new_command_with_exchange(tmp_path):
    """Test the `new` command correctly sets the exchange."""
    project_name = "test_project_exchange"
    exchange_name = "bybit"
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(app, ["new", project_name, "--exchange", exchange_name])

        assert result.exit_code == 0, result.stdout
        project_path = Path(td) / project_name
        main_py_content = (project_path / "main.py").read_text()

        assert f'exchange="{exchange_name}"' in main_py_content
