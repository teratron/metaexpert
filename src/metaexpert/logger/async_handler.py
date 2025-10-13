"""Asynchronous log handler that wraps another handler with fallback capability."""

import logging
import queue
import sys
import threading


class AsyncHandler(logging.Handler):
    """
    Asynchronous log handler that wraps a synchronous handler to prevent
    blocking the main thread. Implements fallback to stderr when primary
    logging target is unavailable or encounters I/O errors.
    """

    def __init__(self, handler: logging.Handler, max_queue_size: int = 10000, fallback_to_stderr: bool = True):
        """
        Initialize the async log handler.

        Args:
            handler: The synchronous handler to wrap (e.g., FileHandler).
            max_queue_size: The maximum size of the log queue. If the queue
                            is full, new log records will be dropped.
            fallback_to_stderr: Whether to fallback to stderr when primary handler fails
        """
        super().__init__()
        self.queue: queue.Queue[logging.LogRecord | None] = queue.Queue(
            maxsize=max_queue_size
        )
        self.handler = handler
        self.fallback_to_stderr = fallback_to_stderr
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
                self._emit_with_fallback(record)
            except queue.Empty:
                continue
            except Exception:
                # Cannot log the error here, as it might cause a loop.
                # Print to stderr instead.
                import traceback

                traceback.print_exc(file=sys.stderr)

    def _emit_with_fallback(self, record: logging.LogRecord) -> None:
        """Emit record with fallback to stderr if primary handler fails."""
        try:
            self.handler.emit(record)
        except Exception:
            if self.fallback_to_stderr:
                # Fallback to stderr when primary handler fails
                try:
                    # Format the record using the same formatter as the primary handler
                    formatted_msg = record.getMessage() if not hasattr(self.handler, 'formatter') or self.handler.formatter is None else self.handler.formatter.format(record)
                    sys.stderr.write(f"{formatted_msg}\n")
                    sys.stderr.flush()
                except Exception:
                    # If stderr also fails, at least try to print
                    print(f"Logger Error (fallback): {record.getMessage()}", file=sys.stderr)
            else:
                # Re-raise the exception if fallback is disabled
                raise

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
                # If we can't put the record in the queue, try fallback mechanism
                try:
                    self._emit_with_fallback(record)
                except Exception:
                    self.handleError(record)

    def close(self) -> None:
        """Close the handler and clean up resources."""
        # Signal the worker to shut down
        self.shutdown_event.set()
        # Add sentinel value to wake up worker if it's waiting on the queue
        try:
            self.queue.put(None, timeout=1.0)
        except queue.Full:
            pass
        # Wait for the worker thread to finish processing the queue
        self.worker_thread.join(timeout=2.0)
        # Close the wrapped handler
        try:
            self.handler.close()
        except Exception:
            if self.fallback_to_stderr:
                sys.stderr.write("Warning: Error closing primary handler\n")
        super().close()

    def set_formatter(self, fmt: logging.Formatter | None) -> None:
        """Set the formatter for the wrapped handler."""
        super().setFormatter(fmt)
        self.handler.setFormatter(fmt)
