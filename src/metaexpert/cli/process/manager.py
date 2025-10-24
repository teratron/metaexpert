# src/metaexpert/cli/process/manager.py
"""Process lifecycle management."""

import os
import signal
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import psutil

from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.cli.process.pid_lock import PIDFileLock


@dataclass
class ProcessInfo:
    """Information about a running process."""

    pid: int
    name: str
    project_path: Path
    started_at: datetime
    status: str
    memory_mb: float
    cpu_percent: float


class ProcessManager:
    """Manages expert process lifecycle."""

    def __init__(self, pid_dir: Path):
        self.pid_dir = pid_dir
        self.pid_dir.mkdir(parents=True, exist_ok=True)

    def start(
        self,
        project_path: Path,
        script: str = "main.py",
        detach: bool = True,
    ) -> int:
        """
        Start an expert process.

        Args:
            project_path: Path to the project directory
            script: Script to run (default: main.py)
            detach: Run in background

        Returns:
            Process PID

        Raises:
            ProcessError: If process is already running or fails to start
        """
        pid_file = self._get_pid_file(project_path)

        # Check if already running
        if self.is_running(project_path):
            existing_pid = self._read_pid(pid_file)
            raise ProcessError(
                f"Expert already running with PID {existing_pid}. "
                f"Use 'metaexpert stop {project_path.name}' to stop it first."
            )

        script_path = project_path / script
        if not script_path.exists():
            raise ProcessError(f"Script not found: {script_path}")

        # Prepare command
        python_exe = sys.executable
        command = [python_exe, str(script_path)]

        # Start process
        try:
            if detach:
                pid = self._start_detached(command, project_path)
            else:
                pid = self._start_attached(command, project_path)

            # Write PID file
            with PIDFileLock(pid_file):
                pid_file.write_text(str(pid))

            return pid

        except Exception as e:
            raise ProcessError(f"Failed to start process: {e}") from e

    def stop(self, project_path: Path, timeout: int = 30, force: bool = False) -> None:
        """
        Stop an expert process.

        Args:
            project_path: Path to the project directory
            timeout: Graceful shutdown timeout in seconds
            force: Force kill if graceful shutdown fails

        Raises:
            ProcessError: If process is not running or cannot be stopped
        """
        pid_file = self._get_pid_file(project_path)

        if not self.is_running(project_path):
            raise ProcessError(f"No running expert found for {project_path.name}")

        pid = self._read_pid(pid_file)

        try:
            process = psutil.Process(pid)

            # Try graceful shutdown
            if not force:
                process.terminate()
                try:
                    process.wait(timeout=timeout)
                except psutil.TimeoutExpired:
                    if force:
                        process.kill()
                    else:
                        raise ProcessError(
                            f"Process {pid} did not terminate within {timeout}s. "
                            "Use --force to kill it."
                        )
            else:
                process.kill()

            # Clean up PID file
            pid_file.unlink(missing_ok=True)

        except psutil.NoSuchProcess:
            # Process already dead, clean up PID file
            pid_file.unlink(missing_ok=True)
        except Exception as e:
            raise ProcessError(f"Failed to stop process {pid}: {e}") from e

    def is_running(self, project_path: Path) -> bool:
        """Check if an expert process is running."""
        pid_file = self._get_pid_file(project_path)

        if not pid_file.exists():
            return False

        pid = self._read_pid(pid_file)
        if pid is None:
            return False

        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_info(self, project_path: Path) -> Optional[ProcessInfo]:
        """Get information about a running process."""
        if not self.is_running(project_path):
            return None

        pid_file = self._get_pid_file(project_path)
        pid = self._read_pid(pid_file)

        if pid is None:
            return None

        try:
            process = psutil.Process(pid)

            return ProcessInfo(
                pid=pid,
                name=project_path.name,
                project_path=project_path,
                started_at=datetime.fromtimestamp(process.create_time()),
                status=process.status(),
                memory_mb=process.memory_info().rss / 1024 / 1024,
                cpu_percent=process.cpu_percent(interval=0.1),
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def list_running(self, search_path: Path = Path.cwd()) -> List[ProcessInfo]:
        """List all running experts."""
        running = []

        # Search for PID files
        for pid_file in self.pid_dir.glob("*.pid"):
            project_name = pid_file.stem
            project_path = search_path / project_name

            if project_path.exists() and self.is_running(project_path):
                info = self.get_info(project_path)
                if info:
                    running.append(info)

        return running

    def _start_detached(self, command: List[str], cwd: Path) -> int:
        """Start process detached from terminal."""
        kwargs = {
            "cwd": str(cwd),
            "stdout": subprocess.DEVNULL,
            "stderr": subprocess.DEVNULL,
            "stdin": subprocess.DEVNULL,
        }

        if sys.platform == "win32":
            kwargs["creationflags"] = (
                subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            kwargs["start_new_session"] = True

        process = subprocess.Popen(command, **kwargs)
        return process.pid

    def _start_attached(self, command: List[str], cwd: Path) -> int:
        """Start process attached to terminal."""
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
        )
        return process.pid

    def _get_pid_file(self, project_path: Path) -> Path:
        """Get PID file path for a project."""
        return self.pid_dir / f"{project_path.name}.pid"

    def _read_pid(self, pid_file: Path) -> Optional[int]:
        """Read PID from file."""
        try:
            return int(pid_file.read_text().strip())
        except (ValueError, FileNotFoundError):
            return None

