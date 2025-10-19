import os
import time
from pathlib import Path

from typer.testing import CliRunner

from metaexpert.cli.main import app

runner = CliRunner()


# Helper function to simulate a running process for testing PID file logic
def _simulate_process(pid_file_path: Path):
    pid = os.getpid()
    with open(pid_file_path, "w") as f:
        f.write(str(pid))
    # Keep the process alive for a short duration to simulate running
    time.sleep(0.1)


def test_run_command_success(tmp_path):
    """Test the `run` command successfully starts an expert and creates a PID file."""
    project_name = "test_expert_run_success"
    project_path = tmp_path / project_name
    project_path.mkdir()
    (project_path / "main.py").write_text(
        "import time; time.sleep(1); print('Expert running')"
    )

    result = runner.invoke(app, ["run", str(project_path)])

    assert result.exit_code == 0, result.stdout
    assert "Expert started with PID" in result.stdout
    assert (project_path / ".metaexpert.pid").is_file()

    # Clean up the process started by the command
    pid_file_path = project_path / ".metaexpert.pid"
    if pid_file_path.is_file():
        with open(pid_file_path) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 9)  # Terminate the process
        except OSError:
            pass  # Process already exited
        pid_file_path.unlink()


def test_run_command_project_not_found(tmp_path):
    """Test the `run` command fails if the project directory does not exist."""
    non_existent_path = tmp_path / "non_existent_project"
    result = runner.invoke(app, ["run", str(non_existent_path)])

    assert result.exit_code == 1
    assert f"Error: Project directory '{non_existent_path}' not found." in result.stdout


def test_run_command_main_py_not_found(tmp_path):
    """Test the `run` command fails if main.py is not found."""
    project_name = "test_expert_no_main_py"
    project_path = tmp_path / project_name
    project_path.mkdir()

    result = runner.invoke(app, ["run", str(project_path)])

    assert result.exit_code == 1
    assert f"Error: 'main.py' not found in '{project_path}'." in result.stdout


def test_run_command_already_running(tmp_path):
    """Test the `run` command fails if the expert is already running."""
    project_name = "test_expert_already_running"
    project_path = tmp_path / project_name
    project_path.mkdir()
    (project_path / "main.py").write_text(
        "import time; time.sleep(1); print('Expert running')"
    )

    # Simulate a running process by creating a PID file with a valid PID
    pid_file_path = project_path / ".metaexpert.pid"
    with open(pid_file_path, "w") as f:
        f.write(str(os.getpid()))  # Use current process PID for simulation

    result = runner.invoke(app, ["run", str(project_path)])

    assert result.exit_code == 1
    assert (
        f"Error: Expert at '{project_path}' is already running with PID {os.getpid()}."
        in result.stdout
    )
    pid_file_path.unlink()  # Clean up simulated PID file


def test_run_command_stale_pid_file(tmp_path):
    """Test the `run` command cleans up a stale PID file."""
    project_name = "test_expert_stale_pid"
    project_path = tmp_path / project_name
    project_path.mkdir()
    (project_path / "main.py").write_text(
        "import time; time.sleep(1); print('Expert running')"
    )

    # Create a stale PID file (e.g., with a non-existent PID)
    pid_file_path = project_path / ".metaexpert.pid"
    with open(pid_file_path, "w") as f:
        f.write("999999")  # A PID that is very unlikely to exist

    result = runner.invoke(app, ["run", str(project_path)])

    assert result.exit_code == 0, result.stdout
    assert "Warning: Stale PID file found for PID 999999. Removing." in result.stdout
    assert "Expert started with PID" in result.stdout
    assert (project_path / ".metaexpert.pid").is_file()

    # Clean up the process started by the command
    if pid_file_path.is_file():
        with open(pid_file_path) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        pid_file_path.unlink()
