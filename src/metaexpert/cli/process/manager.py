"""Process manager for CLI applications.

This module provides a ProcessManager class for managing the lifecycle of CLI processes,
including starting, stopping, checking status, and retrieving process information.
"""

import datetime
import os
import signal
import subprocess
import time
from datetime import timedelta
from pathlib import Path

import psutil
from pydantic import BaseModel, ConfigDict, Field

from metaexpert.cli.core.exceptions import ProcessError
from metaexpert.logger import get_logger


class ProcessInfo(BaseModel):
    """Pydantic model for representing process information."""

    pid: int = Field(..., description="Process ID")
    name: str = Field(..., description="Name of the process")
    command: str = Field(..., description="Command that started the process")
    start_time: float = Field(..., description="Timestamp when process started")
    started_at: datetime.datetime = Field(..., description="When process started")
    status: str = Field(..., description="Current status of the process")
    working_directory: str = Field(..., description="Working directory of the process")
    environment: dict[str, str] = Field(
        default_factory=dict, description="Environment variables"
    )
    cpu_percent: float = Field(default=0.0, description="CPU usage percentage")
    memory_mb: float = Field(default=0.0, description="Memory usage in MB")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProcessManager:
    """Manages the lifecycle of CLI processes."""

    def __init__(
        self,
        pid_dir: Path | None = None,
        logger_name: str | None = None,
        cache_ttl: timedelta | None = None,
    ):
        """Initialize the ProcessManager.

        Args:
            pid_dir: Directory for storing PID files. If not provided, uses default.
            logger_name: Optional name for the logger. If not provided, uses default logger.
            cache_ttl: Cache time-to-live for process info. Defaults to 5 seconds.
        """
        self.pid_dir = pid_dir or Path.cwd() / "pids"
        self.logger = get_logger(logger_name or __name__)
        self.processes: dict[int, ProcessInfo] = {}
        self._process_handles: dict[int, subprocess.Popen] = {}
        self._info_cache: dict[int, tuple[ProcessInfo, datetime.datetime]] = {}
        self._cache_ttl = cache_ttl or timedelta(seconds=5)

    def start_process(
        self,
        command: list[str],
        working_directory: str | None = None,
        environment: dict[str, str] | None = None,
        wait_for_start: bool = True,
        check_interval: float = 0.1,
        max_wait_time: float = 10.0,
    ) -> ProcessInfo | None:
        """Start a new process.

        Args:
            command: Command to execute as a list of arguments
            working_directory: Working directory for the process (defaults to current)
            environment: Environment variables for the process (defaults to current)
            wait_for_start: Whether to wait for the process to start before returning
            check_interval: Interval to check if process has started (in seconds)
            max_wait_time: Maximum time to wait for process to start (in seconds)

        Returns:
            ProcessInfo object if successful, None otherwise
        """
        try:
            # Prepare working directory
            cwd = working_directory or os.getcwd()
            if isinstance(cwd, str):
                cwd = Path(cwd)
            if not cwd.exists():
                raise FileNotFoundError(f"Working directory does not exist: {cwd}")

            # Prepare environment
            env = environment or os.environ.copy()

            # Start the process
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd,
                env=env,
                text=True,
            )

            # Create process info
            process_info = ProcessInfo(
                pid=process.pid,
                name=Path(command[0]).stem if command else "unknown",
                command=" ".join(command),
                start_time=time.time(),
                started_at=datetime.datetime.fromtimestamp(time.time()),
                status="running",
                working_directory=str(cwd),
                environment=env,
            )

            # Store process info and handle
            self.processes[process.pid] = process_info
            self._process_handles[process.pid] = process

            self.logger.info(
                f"Started process {process.pid} with command: {' '.join(command)}",
                extra={"process_id": process.pid, "command": process_info.command},
            )

            # Optionally wait for the process to be confirmed as running
            if wait_for_start:
                start_time = time.time()
                while time.time() - start_time < max_wait_time:
                    if self.is_running(process.pid):
                        break
                    time.sleep(check_interval)
                else:
                    self.logger.warning(
                        f"Process {process.pid} did not start within {max_wait_time} seconds",
                        extra={"process_id": process.pid},
                    )
                    return None

            return process_info

        except Exception as e:
            self.logger.error(
                f"Failed to start process with command: {' '.join(command)} - Error: {e!s}",
                extra={"command": " ".join(command), "error": str(e)},
            )
            return None

    def stop_process(self, pid: int, timeout: int = 5) -> bool:
        """Stop a running process.

        Args:
            pid: Process ID to stop
            timeout: Timeout in seconds to wait for graceful termination

        Returns:
            True if process was stopped successfully, False otherwise
        """
        if pid not in self.processes:
            self.logger.warning(
                f"Process {pid} not found in managed processes",
                extra={"process_id": pid},
            )
            return False

        try:
            process_handle = self._process_handles.get(pid)
            if not process_handle:
                self.logger.warning(
                    f"No process handle found for PID {pid}", extra={"process_id": pid}
                )
                return False

            # Check if process is still running
            if not self.is_running(pid):
                self.logger.info(
                    f"Process {pid} is already stopped", extra={"process_id": pid}
                )
                self._cleanup_process(pid)
                return True

            # Try graceful termination first
            self.logger.info(
                f"Stopping process {pid} gracefully", extra={"process_id": pid}
            )
            os.kill(pid, signal.SIGTERM)

            # Wait for process to terminate
            try:
                process_handle.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                # Force kill if graceful termination failed
                self.logger.warning(
                    f"Graceful termination failed for process {pid}, force killing",
                    extra={"process_id": pid},
                )
                os.kill(pid, signal.SIGKILL)
                process_handle.wait()  # Wait for force kill to complete

            # Clean up process info
            self._cleanup_process(pid)
            self.logger.info(
                f"Successfully stopped process {pid}", extra={"process_id": pid}
            )
            return True

        except ProcessLookupError:
            # Process already terminated
            self._cleanup_process(pid)
            self.logger.info(
                f"Process {pid} was already terminated", extra={"process_id": pid}
            )
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to stop process {pid} - Error: {e!s}",
                extra={"process_id": pid, "error": str(e)},
            )
            return False

    def is_running(self, pid: int | Path) -> bool:
        """Check if a process is currently running.

        Args:
            pid: Process ID to check or Path to project directory to check

        Returns:
            True if process is running, False otherwise
        """
        if isinstance(pid, Path):
            # If it's a Path, read the PID from the project's PID file
            actual_pid = self._read_pid(pid)
            if actual_pid is None:
                return False
            pid = actual_pid

        try:
            os.kill(pid, 0)  # Signal 0 checks if process exists without affecting it
            return True
        except OSError:
            # Process doesn't exist
            return False

    def get_process_info(self, pid: int) -> ProcessInfo | None:
        """Get information about a specific process.

        Args:
            pid: Process ID to get info for

        Returns:
            ProcessInfo object if process exists, None otherwise
        """
        if pid in self.processes:
            # Update status if needed
            current_status = "running" if self.is_running(pid) else "stopped"
            self.processes[pid].status = current_status
            return self.processes[pid]
        return None

    def get_info(self, pid: int | Path, use_cache: bool = True) -> ProcessInfo | None:
        """Get detailed information about a process, including CPU and memory usage.

        Args:
            pid: Process ID to get detailed info for or Path to project directory
            use_cache: Whether to use cached information if available and not expired

        Returns:
            ProcessInfo object with detailed metrics if process exists, None otherwise
        """
        if isinstance(pid, Path):
            # If it's a Path, read the PID from the project's PID file
            actual_pid = self._read_pid(pid)
            if actual_pid is None:
                return None
            pid = actual_pid

        if pid not in self.processes:
            return None

        # Check cache if enabled
        if use_cache and pid in self._info_cache:
            cached_info, timestamp = self._info_cache[pid]
            if datetime.datetime.now() - timestamp < self._cache_ttl:
                # Update status in cached info in case it changed
                current_status = "running" if self.is_running(pid) else "stopped"
                cached_info.status = current_status
                return cached_info

        try:
            # Get the process object using psutil
            proc = psutil.Process(pid)

            # Get CPU and memory usage
            cpu_percent = proc.cpu_percent(interval=0.1)
            memory_info = proc.memory_info()
            memory_mb = memory_info.rss / 1024 / 1024  # Convert bytes to MB

            # Update the existing ProcessInfo with current metrics
            process_info = self.processes[pid]
            process_info.cpu_percent = cpu_percent
            process_info.memory_mb = memory_mb

            # Update status as well
            current_status = "running" if self.is_running(pid) else "stopped"
            process_info.status = current_status

            # Cache the updated info
            self._info_cache[pid] = (process_info, datetime.datetime.now())

            return process_info

        except psutil.NoSuchProcess:
            # Process doesn't exist anymore, update status and return
            self.processes[pid].status = "stopped"
            # Cache the stopped status
            self._info_cache[pid] = (self.processes[pid], datetime.datetime.now())
            return self.processes[pid]
        except psutil.AccessDenied:
            # Access denied to get process info, return current info with warning
            self.logger.warning(
                f"Access denied when getting detailed info for process {pid}",
                extra={"process_id": pid},
            )
            # Still cache the info even if we can't get CPU/memory
            self._info_cache[pid] = (self.processes[pid], datetime.datetime.now())
            return self.processes[pid]
        except Exception as e:
            self.logger.error(
                f"Failed to get detailed info for process {pid} - Error: {e!s}",
                extra={"process_id": pid, "error": str(e)},
            )
            # Still cache the info even if there was an error
            self._info_cache[pid] = (self.processes[pid], datetime.datetime.now())
            return self.processes[pid]

    def list_processes(self) -> list[ProcessInfo]:
        """Get information about all managed processes.

        Returns:
            List of ProcessInfo objects for all managed processes
        """
        # Update statuses for all processes
        for pid in list(self.processes.keys()):
            current_status = "running" if self.is_running(pid) else "stopped"
            self.processes[pid].status = current_status

        return list(self.processes.values())

    def stop_all_processes(self, timeout: int = 5) -> bool:
        """Stop all managed processes.

        Args:
            timeout: Timeout in seconds to wait for graceful termination of each process

        Returns:
            True if all processes were stopped successfully, False otherwise
        """
        success = True
        pids = list(self.processes.keys())

        for pid in pids:
            if not self.stop_process(pid, timeout):
                success = False

        return success

    def cleanup_stopped_processes(self) -> None:
        """Remove information about processes that have stopped."""
        stopped_pids = [
            pid for pid in self.processes.keys() if not self.is_running(pid)
        ]
        for pid in stopped_pids:
            self._cleanup_process(pid)
            self.logger.debug(
                f"Cleaned up stopped process {pid}", extra={"process_id": pid}
            )

    def _cleanup_process(self, pid: int) -> None:
        """Internal method to clean up process information.

        Args:
            pid: Process ID to clean up
        """
        if pid in self.processes:
            del self.processes[pid]
        if pid in self._process_handles:
            del self._process_handles[pid]

    def _get_pid_file(self, project_path: str | Path) -> Path:
        """Get the path to the PID file for a specific project.

        Args:
            project_path: Path to the project directory

        Returns:
            Path object representing the PID file location
        """
        project_path = Path(project_path)
        # Use the project name as part of the PID file name to avoid conflicts
        project_name = project_path.name
        pid_filename = f"{project_name}.pid"
        return project_path / pid_filename

    def _read_pid(self, project_path: str | Path) -> int | None:
        """Read the PID from the PID file for a specific project.

        Args:
            project_path: Path to the project directory

        Returns:
            Process ID if found and valid, None otherwise
        """
        pid_file = self._get_pid_file(project_path)

        if not pid_file.exists():
            return None

        try:
            with open(pid_file) as f:
                pid_str = f.read().strip()
                if pid_str:
                    pid = int(pid_str)
                    return pid
        except (OSError, ValueError) as e:
            self.logger.warning(
                f"Failed to read PID from {pid_file}: {e!s}",
                extra={"pid_file": str(pid_file), "error": str(e)},
            )

        return None

    def _write_pid(self, project_path: str | Path, pid: int) -> bool:
        """Write the PID to the PID file for a specific project.

        Args:
            project_path: Path to the project directory
            pid: Process ID to write

        Returns:
            True if successful, False otherwise
        """
        pid_file = self._get_pid_file(project_path)

        try:
            with open(pid_file, "w") as f:
                f.write(str(pid))
            self.logger.debug(
                f"Written PID {pid} to {pid_file}",
                extra={"pid": pid, "pid_file": str(pid_file)},
            )
            return True
        except OSError as e:
            self.logger.error(
                f"Failed to write PID {pid} to {pid_file}: {e!s}",
                extra={"pid": pid, "pid_file": str(pid_file), "error": str(e)},
            )
            return False

    def start(
        self,
        project_path: str | Path,
        script: str = "main.py",
        detach: bool = True,
    ) -> int:
        """Start an expert process.

        Args:
            project_path: Path to the project directory
            script: Script to run (default: main.py)
            detach: Whether to run in detached mode

        Returns:
            Process ID of the started process
        """
        project_path = Path(project_path)

        # Read PID file to check if already running
        existing_pid = self._read_pid(project_path)
        if existing_pid and self.is_running(existing_pid):
            raise ProcessLookupError(f"Process already running with PID {existing_pid}")

        # Build command
        cmd = ["python", str(project_path / script)]

        # Add environment variables from .env file if it exists
        env = os.environ.copy()
        env_file = project_path / ".env"
        if env_file.exists():
            try:
                import dotenv

                dotenv.load_dotenv(env_file, override=True)
            except ImportError:
                # dotenv is optional, warn but continue
                self.logger.warning(
                    f"dotenv not installed, skipping .env file: {env_file}"
                )

        # Start the process
        process_info = self.start_process(
            command=cmd,
            working_directory=str(project_path),
            environment=env,
            wait_for_start=True,
        )

        if not process_info:
            raise ProcessError(f"Failed to start process for {project_path}")

        # Write PID to file
        self._write_pid(project_path, process_info.pid)

        return process_info.pid

    def stop(
        self,
        project_path: str | Path,
        timeout: int = 30,
        force: bool = False,
    ) -> bool:
        """Stop an expert process.

        Args:
            project_path: Path to the project directory
            timeout: Timeout in seconds to wait for graceful termination
            force: Whether to force kill the process

        Returns:
            True if process was stopped successfully, False otherwise
        """
        project_path = Path(project_path)

        # Read PID from file
        pid = self._read_pid(project_path)
        if not pid:
            raise ProcessError(f"No PID file found for {project_path}")

        if not self.is_running(pid):
            # Clean up stale PID file
            self._delete_pid(project_path)
            raise ProcessError(f"Process {pid} is not running")

        # Stop the process
        success = self.stop_process(pid, timeout)

        if success:
            # Clean up PID file
            self._delete_pid(project_path)

        return success

    def list_running(self, search_path: str | Path | None = None) -> list[ProcessInfo]:
        """List all running expert processes.

        Args:
            search_path: Optional path to limit search to specific directory

        Returns:
            List of ProcessInfo objects for running processes
        """
        if search_path:
            search_path = Path(search_path)
            # For this implementation, we'll check each PID file in the search path
            running_processes = []

            # Look for .pid files in the search path
            for pid_file in search_path.glob("*.pid"):
                try:
                    with open(pid_file) as f:
                        pid_str = f.read().strip()
                        if pid_str:
                            pid = int(pid_str)
                            if self.is_running(pid):
                                info = self.get_info(pid)
                                if info:
                                    running_processes.append(info)
                except (OSError, ValueError):
                    continue

            return running_processes
        else:
            # Return all managed processes that are running
            return [
                info for pid, info in self.processes.items() if self.is_running(pid)
            ]

    def _delete_pid(self, project_path: str | Path) -> bool:
        """Delete the PID file for a specific project.

        Args:
            project_path: Path to the project directory

        Returns:
            True if successful, False otherwise
        """
        pid_file = self._get_pid_file(project_path)

        if not pid_file.exists():
            return True  # File doesn't exist, so it's effectively deleted

        try:
            pid_file.unlink()
            self.logger.debug(
                f"Deleted PID file {pid_file}", extra={"pid_file": str(pid_file)}
            )
            return True
        except OSError as e:
            self.logger.error(
                f"Failed to delete PID file {pid_file}: {e!s}",
                extra={"pid_file": str(pid_file), "error": str(e)},
            )
            return False
