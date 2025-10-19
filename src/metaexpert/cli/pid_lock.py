"""Utility for PID file locking."""

import os
import sys
from pathlib import Path

if sys.platform != "win32":
    import fcntl


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
                # Acquire an exclusive lock on Unix-like systems
                fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except FileExistsError:
            raise RuntimeError(f"PID file '{self.pid_file_path}' is already locked.")
        except BlockingIOError:
            # This can happen on Unix if flock fails even after O_EXCL (e.g., NFS issues)
            if self.fd is not None:
                os.close(self.fd)
                self.fd = None
            raise RuntimeError(f"PID file '{self.pid_file_path}' is already locked.")

        # Do not write PID here. The caller will write the actual process PID.
        os.ftruncate(self.fd, 0)  # Clear the file content
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd is not None:
            os.close(self.fd)
            if not self.keep_file and self.pid_file_path.exists():
                self.pid_file_path.unlink()
