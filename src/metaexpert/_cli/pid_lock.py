"""Utility for PID file locking."""

import os
import signal
import subprocess
import sys
from pathlib import Path


class PidFileLock:
    """A context manager for managing PID files with file locking."""

    def __init__(self, pid_file_path: Path):
        self.pid_file_path = pid_file_path
        self.fd = None
        self.keep_file = False  # New flag

    def __enter__(self):
        self.pid_file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Use os.O_EXCL for exclusive creation. If the file exists, this will raise FileExistsError.
            self.fd = os.open(self.pid_file_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)

            if sys.platform != "win32":
                import fcntl

                # Acquire an exclusive lock on Unix-like systems
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except FileExistsError:
            raise RuntimeError(
                f"PID file '{self.pid_file_path}' is already locked."
            ) from None
        except BlockingIOError:
            # This can happen on Unix if flock fails even after O_EXCL (e.g., NFS issues)
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
            raise RuntimeError(
                f"PID file '{self.pid_file_path}' is already locked."
            ) from None

        # Do not write PID here. The caller will write the actual process PID.
        os.ftruncate(self.fd, 0)  # Clear the file content
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            os.close(self.fd)
            if not self.keep_file and self.pid_file_path.exists():
                self.pid_file_path.unlink()


def is_process_running(pid: int) -> bool:
    """Checks if a process with the given PID is currently running."""
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.WinDLL("kernel32")
            synchronize = 0x00100000
            process_query_information = 0x0400
            still_active = 259

            process_handle = kernel32.OpenProcess(
                process_query_information | synchronize, 0, pid
            )
            if process_handle:
                exit_code = ctypes.c_ulong()
                kernel32.GetExitCodeProcess(process_handle, ctypes.byref(exit_code))
                kernel32.CloseHandle(process_handle)
                return exit_code.value == still_active
            else:
                # Check if access was denied (e.g., for system processes)
                if kernel32.GetLastError() == 5:  # ERROR_ACCESS_DENIED
                    return True  # Assume it's running if access is denied
                return False
        except (OSError, AttributeError, ValueError):
            return False
    else:  # Unix-like systems
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def get_pid_from_file(pid_file_path: Path) -> int | None:
    """Reads and returns the PID from a file, returning None if not found or invalid."""
    if not pid_file_path.is_file():
        return None
    try:
        with pid_file_path.open() as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return None


def terminate_process(pid: int) -> None:
    """Terminates a process by PID, handling platform differences."""
    if sys.platform == "win32":
        result = subprocess.run(
            ["taskkill", "/F", "/PID", str(pid)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0 and "not found" not in result.stderr:
            raise OSError(f"taskkill failed: {result.stderr}")
        if "not found" in result.stderr:
            raise ProcessLookupError
    else:
        os.kill(pid, signal.SIGTERM)


def cleanup_pid_file(pid_file_path: Path) -> None:
    """Remove the PID file if it exists."""
    if pid_file_path.exists():
        pid_file_path.unlink()
