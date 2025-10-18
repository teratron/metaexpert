"""Fallback stderr handler and disk space monitoring for the MetaExpert logging system.

This module contains handlers that can be used as fallbacks when
primary logging mechanisms fail, such as when disk is full or
file permissions are insufficient.
"""

import logging
import shutil
import sys
from logging import StreamHandler
from pathlib import Path


class StderrFallbackHandler(StreamHandler):
    """A logging handler that writes to stderr as a fallback mechanism."""

    def __init__(self):
        # Initialize with stderr as the stream
        super().__init__(stream=sys.stderr)

        # Set a simple formatter for stderr output
        formatter = logging.Formatter(
            fmt="%(levelname)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.setFormatter(formatter)

        # By default, this handler logs WARNING and above to stderr
        # This is meant to be used as a fallback for important messages
        self.setLevel(logging.WARNING)

    def emit(self, record):
        """Emit a log record to stderr.

        This implementation ensures that even if other handlers fail,
        critical messages still make it to the user via stderr.
        """
        try:
            # Call the parent emit method to handle the record
            super().emit(record)
        except Exception:
            # If we can't write to stderr either, we're in serious trouble
            # but at least try to handle the error gracefully
            self.handleError(record)

    def should_use_fallback(self, original_handlers_status):
        """Determine if the fallback handler should be activated.

        Args:
            original_handlers_status: A dict indicating the status of primary handlers

        Returns:
            bool: True if fallback should be used
        """
        # Activate fallback if any primary handler has failed
        for status in original_handlers_status.values():
            if not status:  # If any handler failed
                return True
        return False


def check_disk_space(path, required_space_mb=10):
    """Check if there's enough disk space at the given path.

    Args:
        path: Path to check disk space for
        required_space_mb: Required space in MB

    Returns:
        bool: True if there's enough space, False otherwise
    """
    try:
        # Get the directory if path is a file
        if not Path(path).is_dir():
            path = Path(path).parent

        # Get disk usage statistics
        _total, _used, free = shutil.disk_usage(path)
        free_mb = free / (1024 * 1024)

        return free_mb >= required_space_mb
    except Exception:
        # If we can't check the disk space, assume there's enough
        # This prevents the logging system from failing due to disk check errors
        return True


class SafeFileHandler(logging.FileHandler):
    """A file handler that falls back to stderr if file writing fails."""

    def __init__(
        self, filename, mode="a", encoding=None, delay=False, min_free_space_mb=10
    ):
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)

        # Store minimum free space requirement
        self.min_free_space_mb = min_free_space_mb

        # Create a fallback handler
        self.fallback_handler = StderrFallbackHandler()

        # Set the same formatter as the file handler
        self.fallback_handler.setFormatter(self.formatter)

    def emit(self, record):
        """Emit a log record, with fallback to stderr if file writing fails."""
        # Check disk space before attempting to write
        if not check_disk_space(
            self.baseFilename, required_space_mb=self.min_free_space_mb
        ):
            # Not enough disk space, use fallback immediately
            try:
                self.fallback_handler.emit(record)
            except Exception:
                self.handleError(record)
            return

        try:
            # Try to emit to file first
            super().emit(record)
        except Exception:
            # If file writing fails (could be due to permissions, disk full, etc.),
            # use the fallback handler
            try:
                self.fallback_handler.emit(record)
            except Exception:
                # If both fail, use the error handling mechanism
                self.handleError(record)


class DiskSpaceMonitoringFileHandler(logging.FileHandler):
    """A file handler that monitors disk space and switches to console when low."""

    def __init__(
        self,
        filename,
        console_handler=None,
        mode="a",
        encoding=None,
        delay=False,
        low_space_threshold_mb=100,
    ):
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)

        # Store the low space threshold
        self.low_space_threshold_mb = low_space_threshold_mb

        # Store a reference to the console handler to switch to when needed
        self.console_handler = console_handler

        # Flag to track if we've switched to console-only mode
        self._using_console_only = False

    def emit(self, record):
        """Emit a log record, switching to console if disk space is low."""
        # Check if we should switch to console-only mode
        if not self._using_console_only:
            if not check_disk_space(
                self.baseFilename, required_space_mb=self.low_space_threshold_mb
            ):
                self._using_console_only = True
                # Log a warning that we're switching to console-only mode
                warning_record = logging.LogRecord(
                    name=record.name,
                    level=logging.WARNING,
                    pathname=record.pathname,
                    lineno=record.lineno,
                    msg="Disk space low - switching to console-only logging mode",
                    args=(),
                    exc_info=None,
                )
                # Log the warning to console
                if self.console_handler:
                    self.console_handler.emit(warning_record)

        # If we're in console-only mode, send to console instead of file
        if self._using_console_only and self.console_handler:
            try:
                self.console_handler.emit(record)
            except Exception:
                # If console logging fails, handle the error
                self.handleError(record)
        else:
            # Otherwise, write to the file as normal
            try:
                super().emit(record)
            except Exception:
                # If file writing fails, use the error handling mechanism
                self.handleError(record)
