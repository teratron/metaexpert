"""Asynchronous log handler for non-blocking logging operations."""

import logging
import queue
import threading
import time
import traceback
from typing import Optional
from logging import StreamHandler
import sys
import weakref


class AsyncLogHandler(logging.Handler):
    """Asynchronous log handler that doesn't block the main thread.
    
    This handler uses a queue and worker thread to process log records
    asynchronously, preventing logging operations from impacting
    application performance.
    """

    def __init__(self, max_queue_size: int = 10000) -> None:
        """Initialize the async log handler.

        Args:
            max_queue_size: Maximum number of log records to queue
        """
        super().__init__()
        # Performance optimization: Use deque for faster queue operations
        self.queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self.worker_thread: Optional[threading.Thread] = None
        self.shutdown_event = threading.Event()
        self.sync_handler = StreamHandler(stream=sys.stdout)
        # Performance optimization: Track queue size to prevent memory issues
        self.dropped_records = 0
        self.max_dropped_records_warning = 100
        self.start_worker()

    def start_worker(self) -> None:
        """Start the worker thread for processing log records."""
        try:
            self.worker_thread = threading.Thread(target=self._worker, daemon=True, name="AsyncLogWorker")
            self.worker_thread.start()
        except Exception as e:
            # Handle errors during worker thread creation
            self.handleError(logging.LogRecord(
                name="AsyncLogHandler",
                level=logging.ERROR,
                pathname=__file__,
                lineno=0,
                msg=f"Failed to start worker thread: {str(e)}",
                args=(),
                exc_info=sys.exc_info()
            ))

    def _worker(self) -> None:
        """Worker thread function that processes log records from the queue."""
        try:
            batch_size = 10  # Process records in batches for better performance
            while not self.shutdown_event.is_set():
                try:
                    records_batch = []
                    # Collect a batch of records
                    for _ in range(batch_size):
                        try:
                            # Non-blocking get with timeout
                            record = self.queue.get_nowait()
                            if record is None:
                                # Special sentinel value to indicate shutdown
                                self.queue.task_done()
                                return
                            records_batch.append(record)
                        except queue.Empty:
                            # No more records in queue, break batch collection
                            break
                    
                    # Process the batch
                    if records_batch:
                        for record in records_batch:
                            try:
                                self.sync_handler.emit(record)
                            except Exception as e:
                                # Log errors in the worker thread but don't crash the worker
                                error_record = logging.LogRecord(
                                    name="AsyncLogHandler.Worker",
                                    level=logging.ERROR,
                                    pathname=__file__,
                                    lineno=0,
                                    msg=f"Error processing log record in worker: {str(e)}",
                                    args=(),
                                    exc_info=sys.exc_info()
                                )
                                try:
                                    self.sync_handler.emit(error_record)
                                except:
                                    # If even error logging fails, print to stderr
                                    print(f"CRITICAL: Failed to log error: {str(e)}", file=sys.stderr)
                            finally:
                                self.queue.task_done()
                        
                    # If we didn't get a full batch, sleep briefly to avoid busy-waiting
                    if len(records_batch) < batch_size:
                        time.sleep(0.001)  # 1ms sleep
                        
                except queue.Empty:
                    # No records available, sleep briefly
                    time.sleep(0.001)  # 1ms sleep
                    continue
                except Exception as e:
                    # Handle other errors in the worker thread
                    error_msg = f"Unexpected error in worker thread: {str(e)}"
                    print(error_msg, file=sys.stderr)
                    traceback.print_exc()
                    # Continue the loop to avoid crashing the worker
                    
        except Exception as e:
            # Handle catastrophic errors in the worker
            error_msg = f"Catastrophic error in worker thread: {str(e)}"
            print(error_msg, file=sys.stderr)
            traceback.print_exc()

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record asynchronously by adding it to the queue.

        Args:
            record: The log record to emit
        """
        try:
            # Performance optimization: Drop records if queue is too full
            if self.queue.qsize() > self.queue.maxsize * 0.9:  # 90% full
                self.dropped_records += 1
                if self.dropped_records <= self.max_dropped_records_warning:
                    # Log warning for first few dropped records
                    warning_record = logging.LogRecord(
                        name="AsyncLogHandler",
                        level=logging.WARNING,
                        pathname=__file__,
                        lineno=0,
                        msg=f"Dropping log record due to high queue pressure ({self.queue.qsize()}/{self.queue.maxsize})",
                        args=(),
                        exc_info=None
                    )
                    # Send directly to sync handler to avoid recursion
                    try:
                        self.sync_handler.emit(warning_record)
                    except:
                        pass
                elif self.dropped_records == self.max_dropped_records_warning + 1:
                    # Log final warning when threshold exceeded
                    final_warning = logging.LogRecord(
                        name="AsyncLogHandler",
                        level=logging.WARNING,
                        pathname=__file__,
                        lineno=0,
                        msg=f"Further dropped record warnings suppressed (total dropped: {self.dropped_records})",
                        args=(),
                        exc_info=None
                    )
                    try:
                        self.sync_handler.emit(final_warning)
                    except:
                        pass
                return
            
            # Format the record before queuing to capture current time/state
            formatted_record = self.format(record)
            
            # Create a copy of the record with the formatted message
            record_copy = logging.LogRecord(
                record.name, record.levelno, record.pathname, record.lineno,
                formatted_record, record.args, record.exc_info, record.funcName,
                record.stack_info
            )
            record_copy.created = record.created
            record_copy.msecs = record.msecs
            record_copy.relativeCreated = record.relativeCreated
            record_copy.thread = record.thread
            record_copy.threadName = record.threadName
            record_copy.processName = record.processName
            record_copy.process = record.process
            
            # Add the record to the queue
            self.queue.put_nowait(record_copy)
        except queue.Full:
            # Queue is full, drop the log record to prevent blocking
            self.dropped_records += 1
            if self.dropped_records <= self.max_dropped_records_warning:
                try:
                    # Log that we're dropping records (to a different handler to avoid recursion)
                    drop_record = logging.LogRecord(
                        name="AsyncLogHandler",
                        level=logging.WARNING,
                        pathname=__file__,
                        lineno=0,
                        msg="Dropping log record due to full queue",
                        args=(),
                        exc_info=None
                    )
                    # Send directly to sync handler to avoid recursion
                    self.sync_handler.emit(drop_record)
                except:
                    # If even that fails, print to stderr
                    print("WARNING: Dropping log record due to full queue", file=sys.stderr)
        except Exception as e:
            # Handle any other errors gracefully
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and clean up resources."""
        try:
            # Signal the worker thread to shut down
            self.shutdown_event.set()
            
            # Add sentinel value to wake up worker if it's waiting
            try:
                self.queue.put_nowait(None)
            except queue.Full:
                pass
                
            # Wait for worker thread to finish (with timeout)
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker_thread.join(timeout=5.0)
                
            # Close the synchronous handler
            self.sync_handler.close()
            
            # Call parent close
            super().close()
            
        except Exception as e:
            # Handle errors during cleanup gracefully
            error_msg = f"Error closing AsyncLogHandler: {str(e)}"
            print(error_msg, file=sys.stderr)
            traceback.print_exc()


class BufferedAsyncLogHandler(AsyncLogHandler):
    """Buffered async log handler that batches log records for efficiency."""

    def __init__(self, max_queue_size: int = 10000, buffer_size: int = 100, 
                 flush_interval: float = 1.0) -> None:
        """Initialize the buffered async log handler.

        Args:
            max_queue_size: Maximum number of log records to queue
            buffer_size: Number of records to buffer before flushing
            flush_interval: Time interval (seconds) to flush buffered records
        """
        try:
            super().__init__(max_queue_size)
            self.buffer_size = buffer_size
            self.flush_interval = flush_interval
            self.buffer: list = []
            self.last_flush = time.time()
            # Performance optimization: Timer for periodic flushing
            self.flush_timer: Optional[threading.Timer] = None
        except Exception as e:
            # Handle initialization errors
            error_msg = f"Error initializing BufferedAsyncLogHandler: {str(e)}"
            print(error_msg, file=sys.stderr)
            traceback.print_exc()
            raise

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record by buffering it.

        Args:
            record: The log record to emit
        """
        try:
            # Add record to buffer
            self.buffer.append(record)
            
            # Schedule flush if buffer is full
            if len(self.buffer) >= self.buffer_size:
                self._schedule_flush()
            else:
                # Ensure periodic flush is scheduled
                self._ensure_flush_timer()
        except Exception as e:
            # Handle errors in emit gracefully
            self.handleError(record)

    def _schedule_flush(self) -> None:
        """Schedule buffer flush immediately."""
        try:
            # Cancel any existing timer
            if self.flush_timer:
                self.flush_timer.cancel()
                
            # Flush immediately
            self._flush_buffer()
        except Exception as e:
            # Handle flush scheduling errors
            error_msg = f"Error scheduling buffer flush: {str(e)}"
            print(error_msg, file=sys.stderr)

    def _ensure_flush_timer(self) -> None:
        """Ensure periodic flush timer is running."""
        try:
            # If no timer is running and buffer has data, schedule one
            if not self.flush_timer and self.buffer:
                current_time = time.time()
                if current_time - self.last_flush >= self.flush_interval:
                    # Flush immediately if enough time has passed
                    self._flush_buffer()
                else:
                    # Schedule flush for later
                    delay = self.flush_interval - (current_time - self.last_flush)
                    self.flush_timer = threading.Timer(delay, self._flush_buffer)
                    self.flush_timer.daemon = True
                    self.flush_timer.start()
        except Exception as e:
            # Handle timer scheduling errors
            error_msg = f"Error ensuring flush timer: {str(e)}"
            print(error_msg, file=sys.stderr)

    def _flush_buffer(self) -> None:
        """Flush the buffered log records."""
        try:
            # Cancel any pending timer
            if self.flush_timer:
                self.flush_timer.cancel()
                self.flush_timer = None
                
            if not self.buffer:
                return
                
            # Process all buffered records
            for record in self.buffer:
                super().emit(record)
                
            # Clear buffer and update flush time
            self.buffer.clear()
            self.last_flush = time.time()
            
        except Exception as e:
            # Handle errors during buffer flush
            error_msg = f"Error flushing buffer: {str(e)}"
            print(error_msg, file=sys.stderr)
            traceback.print_exc()
            # Clear buffer even if there was an error
            self.buffer.clear()
            # Re-raise to notify caller
            raise
            
    def close(self) -> None:
        """Close the handler and clean up resources."""
        try:
            # Cancel any pending timer
            if self.flush_timer:
                self.flush_timer.cancel()
                
            # Flush any remaining buffered records
            if self.buffer:
                self._flush_buffer()
                
            # Call parent close
            super().close()
            
        except Exception as e:
            # Handle errors during cleanup
            error_msg = f"Error closing BufferedAsyncLogHandler: {str(e)}"
            print(error_msg, file=sys.stderr)