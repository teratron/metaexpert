# src/metaexpert/cli/process/pid_lock.py
"""PID file locking implementation."""

# import fcntl # Only available on Unix-like systems
import os
import sys
from pathlib import Path
from typing import Optional


def is_pid_running(pid: int) -> bool:
    """
    Check if a process with the given PID is running.

    Args:
        pid: Process ID to check

    Returns:
        True if the process is running, False otherwise
    """
    try:
        # Use psutil if available for more accurate process checking
        import psutil

        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    except ImportError:
        # Fallback to os.kill approach for Unix-like systems
        if sys.platform == "win32":
            # On Windows, use psutil or assume the process exists
            # Since we don't have a direct equivalent to os.kill on Windows,
            # we return True to indicate the PID might be valid
            # In practice, we should use psutil on Windows too
            return True
        else:
            # On Unix-like systems, use os.kill with signal 0 to check if process exists
            try:
                os.kill(pid, 0)
                return True
            except OSError:
                return False


def check_pid_file_status(pid_file: Path) -> tuple[bool, Optional[int]]:
    """
    Check the status of a PID file.

    Args:
        pid_file: Path to the PID file

    Returns:
        A tuple containing (file_exists, pid_if_running_or_none)
        - file_exists: True if PID file exists
        - pid_if_running_or_none: PID if process is running, None otherwise
    """
    if not pid_file.exists():
        return False, None

    try:
        pid_content = pid_file.read_text().strip()
        pid = int(pid_content)
    except (ValueError, FileNotFoundError):
        return True, None  # File exists but doesn't contain a valid PID

    # Check if the process with this PID is running
    if is_pid_running(pid):
        return True, pid
    else:
        # PID file exists but process is not running (zombie PID file)
        return True, None


class PIDFileLock:
    """Context manager for PID file locking."""

    def __init__(self, pid_file: Path):
        self.pid_file = pid_file
        self.fd: Optional[int] = None
        self._locked = False

    def __enter__(self) -> "PIDFileLock":
        """Acquire lock."""
        self.pid_file.parent.mkdir(parents=True, exist_ok=True)

        # Open file for writing
        self.fd = os.open(self.pid_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

        # Try to acquire exclusive lock
        try:
            if sys.platform == "win32":
                self._lock_windows()
            else:
                self._lock_unix()

            self._locked = True
        except BlockingIOError:
            os.close(self.fd)
            self.fd = None
            raise RuntimeError(f"PID file {self.pid_file} is already locked")
        except RuntimeError as e:
            # Handle other runtime errors (like missing attributes) by cleaning up
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
            raise e

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Release lock."""
        if self.fd is not None:
            if self._locked:
                if sys.platform == "win32":
                    self._unlock_windows()
                else:
                    self._unlock_unix()

            os.close(self.fd)
            self.fd = None

    def _lock_unix(self) -> None:
        """Acquire lock on Unix systems."""
        import fcntl

        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _unlock_unix(self) -> None:
        """Release lock on Unix systems."""
        import fcntl

        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)

    def _lock_windows(self) -> None:
        """Acquire lock on Windows."""
        # On Windows, we use a different approach since msvcrt.locking may not be available
        # For Windows, we can use msvcrt.locking if available, otherwise we'll use file locking via win32 API
        # For now, we'll implement the basic msvcrt approach but handle the case where attributes don't exist
        import msvcrt
        
        if self.fd is not None:
            # Try to get the required attributes
            try:
                locking_func = getattr(msvcrt, 'locking')
                lk_nblck = getattr(msvcrt, 'LK_NBLCK')
            except AttributeError:
                # If any attribute is missing, raise an error
                raise RuntimeError("Windows file locking not available, msvcrt attributes missing")
            
            locking_func(self.fd, lk_nblck, 1)

    def _unlock_windows(self) -> None:
        """Release lock on Windows."""
        import msvcrt
        
        if self.fd is not None:
            # Try to get the required attributes
            try:
                locking_func = getattr(msvcrt, 'locking')
                lk_unlck = getattr(msvcrt, 'LK_UNLCK')
            except AttributeError:
                # If any attribute is missing, just pass since unlocking is less critical
                return
            
            locking_func(self.fd, lk_unlck, 1)
