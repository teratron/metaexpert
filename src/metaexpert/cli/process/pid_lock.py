# src/metaexpert/cli/process/pid_lock.py
"""PID file locking implementation."""

import fcntl
import os
import sys
from pathlib import Path
from typing import Optional


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
        fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _unlock_unix(self) -> None:
        """Release lock on Unix systems."""
        fcntl.flock(self.fd, fcntl.LOCK_UN)

    def _lock_windows(self) -> None:
        """Acquire lock on Windows."""
        import msvcrt

        msvcrt.locking(self.fd, msvcrt.LK_NBLCK, 1)

    def _unlock_windows(self) -> None:
        """Release lock on Windows."""
        import msvcrt

        msvcrt.locking(self.fd, msvcrt.LK_UNLCK, 1)
