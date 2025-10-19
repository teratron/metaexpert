import os
import subprocess
import sys
import time
from pathlib import Path

from typer.testing import CliRunner

from metaexpert.cli.main import app

runner = CliRunner()


# Helper function to create a dummy expert project
def _create_dummy_expert(project_path: Path):
    project_path.mkdir()
    (project_path / "main.py").write_text(
        "import time\n"
        "import sys\n"
        "with open('expert.log', 'a') as f:\n"
        "    f.write(f'[{time.time()}] [INFO] Expert started\n')\n"
        "try:\n"
        "    while True:\n"
        "        time.sleep(1)\n"
        "except KeyboardInterrupt:\n"
        "    with open('expert.log', 'a') as f:\n"
        "        f.write(f'[{time.time()}] [INFO] Expert stopped\n')\n"
        "    sys.exit(0)\n"
    )


def test_lifecycle_run_list_stop(tmp_path):
    """Test the full run -> list -> stop lifecycle."""
    project_name = "test_lifecycle_expert"
    project_path = tmp_path / project_name
    _create_dummy_expert(project_path)

    # 1. Run the expert
    run_result = runner.invoke(app, ["run", str(project_path)])
    assert run_result.exit_code == 0, run_result.stdout
    assert "Expert started with PID" in run_result.stdout

    # Give it a moment to start and write PID
    time.sleep(0.5)

    # 2. List the expert and check status
    list_result = runner.invoke(app, ["list", str(project_path.parent)])
    assert list_result.exit_code == 0, list_result.stdout
    assert project_name in list_result.stdout
    assert "Running" in list_result.stdout

    # 3. Stop the expert
    stop_result = runner.invoke(app, ["stop", str(project_path)])
    assert stop_result.exit_code == 0, stop_result.stdout
    assert (
        f"Sent SIGTERM to process" in stop_result.stdout
        and "PID file removed." in stop_result.stdout
    )
    # Give it a moment to stop and remove PID
    time.sleep(0.5)

    # 4. List again and check status (should be stopped)
    list_result_after_stop = runner.invoke(app, ["list"])
    assert list_result_after_stop.exit_code == 0, list_result_after_stop.stdout
    assert (
        project_name not in list_result_after_stop.stdout
        or "Stopped" in list_result_after_stop.stdout
    )


def test_run_already_running_race_condition(tmp_path):
    """Test running an expert that is already running."""
    project_name = "test_run_race_expert"
    project_path = tmp_path / project_name
    _create_dummy_expert(project_path)

    # Start the expert in the background
    run_command = [sys.executable, "-m", "metaexpert", "run", str(project_path)]
    if sys.platform == "win32":
        creationflags = (
            subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )
        subprocess.Popen(
            run_command,
            cwd=tmp_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    else:
        subprocess.Popen(
            run_command,
            cwd=tmp_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )

    # Give it a moment to start and write PID
    time.sleep(1)

    # Try to run it again
    run_again_result = runner.invoke(app, ["run", str(project_path)])
    assert run_again_result.exit_code == 1, run_again_result.stdout
    assert (
        f"Error: Expert at '{project_path}' is already running with PID" in run_again_result.stdout
    )
    # Clean up the process
    pid_file_path = project_path / ".metaexpert.pid"
    if pid_file_path.is_file():
        with open(pid_file_path) as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 9)
        except OSError:
            pass
        pid_file_path.unlink()


def test_stop_non_existent_expert(tmp_path):
    """Test stopping an expert that is not running and has no PID file."""
    project_name = "test_stop_non_existent"
    project_path = tmp_path / project_name
    project_path.mkdir()  # Create directory but no PID file

    stop_result = runner.invoke(app, ["stop", str(project_path)])
    assert stop_result.exit_code == 1, stop_result.stdout
    assert "Error: PID file not found" in stop_result.stdout


def test_stop_stale_pid_file(tmp_path):
    """Test stopping an expert with a stale PID file."""
    project_name = "test_stop_stale_pid"
    project_path = tmp_path / project_name
    _create_dummy_expert(project_path)

    # Create a stale PID file (e.g., with a non-existent PID)
    pid_file_path = project_path / ".metaexpert.pid"
    with open(pid_file_path, "w") as f:
        f.write("999999")  # A PID that is very unlikely to exist

    stop_result = runner.invoke(app, ["stop", str(project_path)])
    assert stop_result.exit_code == 0, (
        stop_result.stdout
    )  # Should exit 0 as it cleans up
    assert (
        "Warning: Process with PID 999999 not found. PID file was stale. Removing it."
        in stop_result.stdout
    )
    assert not pid_file_path.is_file()  # PID file should be removed
