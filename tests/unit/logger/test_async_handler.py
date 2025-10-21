"""Unit tests for AsyncHandler class in src/metaexpert/logger/async_handler.py"""

import logging
import tempfile
import threading
import time
from pathlib import Path

from metaexpert.logger.async_handler import AsyncHandler


class TestAsyncHandler:
    """Test suite for AsyncHandler class."""

    def test_async_handler_initialization(self):
        """Test AsyncHandler initialization."""
        # Create a basic handler to wrap
        file_handler = logging.StreamHandler()

        async_handler = AsyncHandler(file_handler, max_queue_size=5000)

        assert async_handler is not None
        assert async_handler.handler == file_handler
        assert async_handler.queue.maxsize == 5000
        assert isinstance(async_handler.worker_thread, threading.Thread)
        assert async_handler.worker_thread.daemon is True

    def test_async_handler_default_queue_size(self):
        """Test AsyncHandler with default queue size."""
        file_handler = logging.StreamHandler()

        async_handler = AsyncHandler(file_handler)

        assert async_handler.queue.maxsize == 10000  # Default max queue size

    def test_async_handler_emits_records(self):
        """Test that AsyncHandler properly emits log records."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "test_async_emit.log"

            # Create a file handler to wrap with AsyncHandler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter("%(message)s"))

            async_handler = AsyncHandler(file_handler)

            # Create a log record
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="",
                lineno=0,
                msg="Test async message",
                args=(),
                exc_info=None,
            )

            # Emit the record
            async_handler.emit(record)

            # Give some time for the async handler to process
            time.sleep(0.1)

            # Close the handler to ensure all records are processed
            async_handler.close()

            # Check if the message was written to the file
            assert log_file.exists()

            with open(log_file, encoding="utf-8") as f:
                content = f.read()

            assert "Test async message" in content

    def test_async_handler_queue_full(self):
        """Test behavior when the queue is full."""
        # Create a handler with a small queue
        file_handler = logging.StreamHandler()
        async_handler = AsyncHandler(file_handler, max_queue_size=1)

        # Fill the queue
        record1 = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="First message",
            args=(),
            exc_info=None,
        )

        record2 = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Second message",
            args=(),
            exc_info=None,
        )

        # Add first record to queue
        async_handler.emit(record1)

        # Try to add second record when queue might be full
        # This should not raise an exception
        async_handler.emit(record2)

        # Close the handler
        async_handler.close()

    def test_async_handler_worker_thread_shutdown(self):
        """Test that the worker thread shuts down properly."""
        file_handler = logging.StreamHandler()
        async_handler = AsyncHandler(file_handler)

        # Verify the thread is running
        assert async_handler.worker_thread.is_alive()

        # Close the handler which should shut down the thread
        async_handler.close()

        # Give time for the thread to finish
        async_handler.worker_thread.join(timeout=2.0)

        # Thread should no longer be alive
        assert not async_handler.worker_thread.is_alive()

    def test_async_handler_with_sentinel_value(self):
        """Test that the sentinel value properly stops the worker."""
        file_handler = logging.StreamHandler()
        async_handler = AsyncHandler(file_handler)

        # Verify the thread is running
        assert async_handler.worker_thread.is_alive()

        # Add sentinel value to queue to signal shutdown
        async_handler.queue.put(None)

        # Give time for the worker to process the sentinel and shut down
        time.sleep(0.1)

        # Close the handler to ensure proper cleanup
        async_handler.close()

        # Thread should no longer be alive after processing sentinel
        async_handler.worker_thread.join(timeout=2.0)
        assert not async_handler.worker_thread.is_alive()

    def test_async_handler_close_method(self):
        """Test the close method functionality."""
        file_handler = logging.StreamHandler()
        async_handler = AsyncHandler(file_handler)

        # Initially, shutdown event should not be set
        assert not async_handler.shutdown_event.is_set()

        # Call close method
        async_handler.close()

        # Shutdown event should now be set
        assert async_handler.shutdown_event.is_set()

    def test_async_handler_set_formatter(self):
        """Test that set_formatter method works correctly."""
        file_handler = logging.StreamHandler()
        async_handler = AsyncHandler(file_handler)

        # Create a new formatter
        new_formatter = logging.Formatter("NEW FORMAT: %(message)s")

        # Set the new formatter
        async_handler.set_formatter(new_formatter)

        # Check that the wrapped handler also got the new formatter
        assert file_handler.formatter._fmt == "NEW FORMAT: %(message)s"

        # Close the handler
        async_handler.close()
