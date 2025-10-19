"""Asynchronous file handler for the MetaExpert logging system.

This module contains the asynchronous file handler that uses a queue
to buffer log entries and a background thread to write them to files,
preventing blocking of the main application thread.
"""

import logging
import queue
import threading
from logging.handlers import RotatingFileHandler


class AsyncFileHandler(logging.Handler):
    """Asynchronous file handler that queues log records for background writing."""

    def __init__(
        self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, encoding="utf-8"
    ):
        super().__init__()

        # Initialize the underlying synchronous handler
        self.sync_handler = RotatingFileHandler(
            filename, maxBytes=max_bytes, backupCount=backup_count, encoding=encoding
        )

        # Create a queue for log records
        self.log_queue = queue.Queue()

        # Flag to control the background thread
        self._stop_thread = False

        # Start the background thread
        self._worker_thread = threading.Thread(target=self._process_logs, daemon=True)
        self._worker_thread.start()

    def emit(self, record):
        """Add a log record to the queue for asynchronous processing."""
        try:
            # Add the record to the queue
            # Use a timeout to avoid blocking indefinitely if the queue is full
            self.log_queue.put(record, block=False)
        except queue.Full:
            # If queue is full, fall back to synchronous logging
            # This is a safety mechanism to prevent record loss
            self.sync_handler.emit(record)

    def _process_logs(self):
        """Background thread function that processes log records from the queue."""
        while not self._stop_thread:
            try:
                # Get a record from the queue with timeout
                record = self.log_queue.get(timeout=1)

                # Process the record using the synchronous handler
                self.sync_handler.emit(record)

                # Mark the task as done
                self.log_queue.task_done()
            except queue.Empty:
                # Queue was empty, continue to next iteration
                continue
            except Exception:
                # If there's an error processing a record, handle_error
                self.handleError(record)

    def close(self):
        """Close the handler and stop the background thread."""
        # Wait for all items in the queue to be processed
        self.log_queue.join()

        # Stop the background thread
        self._stop_thread = True

        # Close the underlying synchronous handler
        self.sync_handler.close()

        # Wait for the worker thread to finish
        if self._worker_thread.is_alive():
            self._worker_thread.join(timeout=2)  # Wait up to 2 seconds

        super().close()


class AsyncExpertFileHandler(AsyncFileHandler):
    """Asynchronous file handler for expert.log - captures most log messages."""

    def __init__(
        self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, encoding="utf-8"
    ):
        super().__init__(
            filename, max_bytes=max_bytes, backup_count=backup_count, encoding=encoding
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Expert log captures all messages except those specifically
        designated for trades or errors logs.
        """
        # Check if this is a trade-specific message (has 'category' field set to 'trade')
        if hasattr(record, "structlog_event_dict"):
            # If structlog_event_dict exists, check for trade category
            if (
                hasattr(record, "__dict__")
                and "category" in record.__dict__
                and record.__dict__.get("category") == "trade"
            ):
                return False  # Don't log trade messages to expert.log
        elif (
            hasattr(record, "__dict__")
            and "trade" in getattr(record, "getMessage", lambda: "")().lower()
        ):
            # Fallback: if it's a trade-related message, don't log to expert.log
            return False

        return True  # Log everything else to expert.log


class AsyncTradesFileHandler(AsyncFileHandler):
    """Asynchronous file handler for trades.log - captures only trade-related messages."""

    def __init__(
        self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, encoding="utf-8"
    ):
        super().__init__(
            filename, max_bytes=max_bytes, backup_count=backup_count, encoding=encoding
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Trades log captures only messages specifically related to trades.
        """
        # Check if this is a trade-specific message (has 'category' field set to 'trade')
        if hasattr(record, "structlog_event_dict"):
            # If structlog_event_dict exists, check for trade category
            if (
                hasattr(record, "__dict__")
                and "category" in record.__dict__
                and record.__dict__.get("category") == "trade"
            ):
                return True

        # Also check if the logger name is related to trading
        if hasattr(record, "name") and "trade" in record.name.lower():
            return True

        # Check if message contains trade-related terms
        if hasattr(record, "getMessage"):
            msg = record.getMessage().lower()
            if any(
                term in msg for term in ["trade", "order", "buy", "sell", "transaction"]
            ):
                return True

        return False


class AsyncErrorsFileHandler(AsyncFileHandler):
    """Asynchronous file handler for errors.log - captures only error and critical messages."""

    def __init__(
        self, filename, max_bytes=10 * 1024 * 1024, backup_count=5, encoding="utf-8"
    ):
        super().__init__(
            filename, max_bytes=max_bytes, backup_count=backup_count, encoding=encoding
        )

    def filter(self, record):
        """
        Determine if a record should be handled by this handler.

        Errors log captures only ERROR and CRITICAL level messages.
        """
        # Only log ERROR and CRITICAL level messages
        return record.levelno >= logging.ERROR
