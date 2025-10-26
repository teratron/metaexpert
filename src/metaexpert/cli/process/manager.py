"""Process manager for CLI applications.

This module provides a ProcessManager class for managing the lifecycle of CLI processes,
including starting, stopping, checking status, and retrieving process information.
"""

import os
import signal
import subprocess
import time
from pathlib import Path

from pydantic import BaseModel, Field

from metaexpert.logger import get_logger


class ProcessInfo(BaseModel):
    """Pydantic model for representing process information."""

    pid: int = Field(..., description="Process ID")
    command: str = Field(..., description="Command that started the process")
    start_time: float = Field(..., description="Timestamp when process started")
    status: str = Field(..., description="Current status of the process")
    working_directory: str = Field(..., description="Working directory of the process")
    environment: dict[str, str] = Field(
        default_factory=dict, description="Environment variables"
    )

    class Config:
        """Pydantic configuration for ProcessInfo."""

        arbitrary_types_allowed = True


class ProcessManager:
    """Manages the lifecycle of CLI processes."""

    def __init__(self, logger_name: str | None = None):
        """Initialize the ProcessManager.

        Args:
            logger_name: Optional name for the logger. If not provided, uses default logger.
        """
        self.logger = get_logger(logger_name or __name__)
        self.processes: dict[int, ProcessInfo] = {}
        self._process_handles: dict[int, subprocess.Popen] = {}

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
                command=" ".join(command),
                start_time=time.time(),
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

    def is_running(self, pid: int) -> bool:
        """Check if a process is currently running.

        Args:
            pid: Process ID to check

        Returns:
            True if process is running, False otherwise
        """
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
