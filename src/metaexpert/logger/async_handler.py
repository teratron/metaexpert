"""Asynchronous log handler that wraps another handler."""

import logging
import queue
import sys
import threading


class AsyncHandler(logging.Handler):
    """
    Asynchronous log handler that wraps a synchronous handler to prevent
    blocking the main thread.
    """

    def __init__(self, handler: logging.Handler, max_queue_size: int = 10000):
        """
        Initialize the async log handler.

        Args:
            handler: The synchronous handler to wrap (e.g., FileHandler).
            max_queue_size: The maximum size of the log queue. If the queue
                            is full, new log records will be dropped.
        """
        super().__init__()
        self.queue: queue.Queue[logging.LogRecord | None] = queue.Queue(
            maxsize=max_queue_size
        )
        self.handler = handler
        self.shutdown_event = threading.Event()
        self.worker_thread = threading.Thread(
            target=self._worker, daemon=True, name=f"AsyncLogWorker-{handler.name}"
        )
        self.worker_thread.start()

    def _worker(self) -> None:
        """Worker thread that processes log records from the queue."""
        while not self.shutdown_event.is_set():
            try:
                record = self.queue.get(timeout=0.1)
                if record is None:  # Sentinel value received
                    break
                self.handler.emit(record)
            except queue.Empty:
                continue
            except Exception:
                # Cannot log the error here, as it might cause a loop.
                # Print to stderr instead.
                import traceback

                traceback.print_exc(file=sys.stderr)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record asynchronously by adding it to the queue.
        If the queue is full, the record is dropped.
        """
        if not self.shutdown_event.is_set():
            try:
                self.queue.put_nowait(record)
            except queue.Full:
                # The queue is full, so we drop the record.
                # This is a design choice to prevent the application from blocking.
                pass
            except Exception:
                self.handleError(record)

    def close(self) -> None:
        """Close the handler and clean up resources."""
        # Signal the worker to shut down
        self.shutdown_event.set()
        # Add sentinel value to wake up worker if it's waiting on the queue
        self.queue.put(None)
        # Wait for the worker thread to finish processing the queue
        self.worker_thread.join()
        # Close the wrapped handler
        self.handler.close()
        super().close()

    def set_formatter(self, fmt: logging.Formatter | None) -> None:
        """Set the formatter for the wrapped handler."""
        super().setFormatter(fmt)
        self.handler.setFormatter(fmt)
