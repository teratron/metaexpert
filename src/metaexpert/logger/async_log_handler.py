"""Simplified asynchronous log handler for non-blocking logging operations."""

import logging
import queue
import sys
import threading
from logging import StreamHandler


class AsyncLogHandler(logging.Handler):
    """Asynchronous log handler that doesn't block the main thread."""

    def __init__(self, max_queue_size: int = 10000) -> None:
        """Initialize the async log handler."""
        super().__init__()
        self.queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self.worker_thread: threading.Thread | None = None
        self.shutdown_event = threading.Event()
        self.sync_handler = StreamHandler(stream=sys.stdout)
        self._start_worker()

    def _start_worker(self) -> None:
        """Start the worker thread for processing log records."""
        self.worker_thread = threading.Thread(
            target=self._worker, daemon=True, name="AsyncLogWorker"
        )
        self.worker_thread.start()

    def _worker(self) -> None:
        """Worker thread function that processes log records from the queue."""
        while not self.shutdown_event.is_set():
            try:
                record = self.queue.get(timeout=0.1)
                if record is None:
                    break
                self.sync_handler.emit(record)
                self.queue.task_done()
            except queue.Empty:
                continue

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record asynchronously by adding it to the queue."""
        try:
            # Format the record before queuing
            formatted_record = self.format(record)
            record_copy = logging.LogRecord(
                record.name,
                record.levelno,
                record.pathname,
                record.lineno,
                formatted_record,
                record.args,
                record.exc_info,
                record.funcName,
                record.stack_info,
            )
            # Add the record to the queue
            self.queue.put_nowait(record_copy)
        except queue.Full:
            # Queue is full, drop the log record to prevent blocking
            sys.stderr.write("WARNING: Dropping log record due to full queue\n")
        except Exception:
            # Handle any other errors gracefully
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and clean up resources."""
        # Signal the worker thread to shut down
        self.shutdown_event.set()

        # Add sentinel value to wake up worker if it's waiting
        try:
            self.queue.put_nowait(None)
        except queue.Full:
            pass

        # Wait for worker thread to finish (with timeout)
        if self.worker_thread and self.worker_thread.is_alive():
            self.worker_thread.join(timeout=1.0)

        # Close the synchronous handler
        self.sync_handler.close()

        # Call parent close
        super().close()
