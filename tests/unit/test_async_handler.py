import logging
import time
import queue
from unittest.mock import Mock
import pytest
from metaexpert.logger.async_log_handler import AsyncLogHandler


@pytest.fixture
def mock_handler() -> Mock:
    """Fixture for a mock synchronous handler."""
    handler = Mock(spec=logging.Handler)
    handler.name = "mock_handler"
    return handler


@pytest.fixture
def async_handler(mock_handler: Mock) -> AsyncLogHandler:
    """Fixture for the AsyncLogHandler, wrapping the mock handler."""
    handler = AsyncLogHandler(handler=mock_handler)
    yield handler
    handler.close()


def test_async_handler_passes_record_to_wrapped_handler(
    async_handler: AsyncLogHandler, mock_handler: Mock
):
    """Test that a log record is passed to the wrapped handler."""
    log_record = logging.LogRecord(
        name="test_async",
        level=logging.INFO,
        pathname="/test/path.py",
        lineno=10,
        msg="Async test message",
        args=(),
        exc_info=None,
    )

    # Emit the record through the async handler
    async_handler.emit(log_record)

    # Give the worker thread a moment to process the queue
    time.sleep(0.2)

    # Assert that the mock handler's emit method was called with the record
    mock_handler.emit.assert_called_once_with(log_record)


def test_async_handler_full_queue_drops_records(async_handler: AsyncLogHandler, mock_handler: Mock):
    """Test that records are dropped when the queue is full."""
    # Set a very small queue size
    async_handler.queue = queue.Queue(maxsize=1)

    record1 = logging.LogRecord("test", logging.INFO, "", 0, "msg1", (), None)
    record2 = logging.LogRecord("test", logging.INFO, "", 0, "msg2", (), None)

    # Put one item, should be fine
    async_handler.emit(record1)

    # Put another item, should be dropped silently
    async_handler.emit(record2)

    time.sleep(0.2)

    # Only the first record should have been emitted
    mock_handler.emit.assert_called_once_with(record1)


# Note: Testing the non-blocking nature is complex in a unit test.
# The simple existence of the worker thread and queue is the primary evidence.
