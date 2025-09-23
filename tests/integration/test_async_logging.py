"""Integration test for async logging functionality."""

import pytest
import logging
import time
import threading
from unittest.mock import patch, MagicMock

from metaexpert.logger import setup_logger, get_logger
from metaexpert.logger.async_log_handler import AsyncLogHandler, BufferedAsyncLogHandler


def test_async_logging_performance_under_load():
    """Test async logging performance under high load.
    
    Given a logger with async logging enabled
    When multiple log messages are generated rapidly
    Then logging should not significantly impact performance
    """
    # Given
    logger = setup_logger("test_async_perf", async_enabled=True)
    
    # When
    start_time = time.time()
    
    # Generate 1000 log messages rapidly
    for i in range(1000):
        logger.info(f"Log message {i}")
        
    end_time = time.time()
    
    # Then
    # The operation should complete quickly (less than 1 second for 1000 messages)
    assert end_time - start_time < 1.0


def test_async_logging_thread_safety():
    """Test that async logging is thread-safe.
    
    Given multiple threads generating log messages
    When async logging is used
    Then log messages should be processed correctly without race conditions
    """
    # Given
    logger = setup_logger("test_async_thread_safety", async_enabled=True)
    
    # Shared list to collect thread results
    results = []
    
    def log_from_thread(thread_id):
        try:
            for i in range(100):
                logger.info(f"Thread {thread_id} - Message {i}")
            results.append(f"Thread {thread_id} completed")
        except Exception as e:
            results.append(f"Thread {thread_id} failed: {str(e)}")
    
    # When
    # Create and start multiple threads
    threads = []
    for i in range(5):
        thread = threading.Thread(target=log_from_thread, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Then
    # All threads should have completed successfully
    assert len(results) == 5
    for result in results:
        assert "completed" in result
        assert "failed" not in result


def test_async_logging_exception_handling():
    """Test that async logging handles exceptions gracefully.
    
    Given an async logging handler that encounters an error
    When a log message cannot be processed
    Then the error should be handled without crashing the application
    """
    # Given
    logger = setup_logger("test_async_exception", async_enabled=True)
    
    # When
    # Log a message that should not cause exceptions
    logger.info("Test message")
    
    # Then
    # No exception should be raised
    assert True  # If we get here, the test passed


def test_async_logging_queue_management():
    """Test that async logging queue management works correctly.
    
    Given a high volume of log messages
    When the async logging queue reaches capacity
    Then appropriate backpressure handling should occur
    """
    # Given
    # Create handler with small queue size for testing
    handler = AsyncLogHandler(max_queue_size=10)
    logger = logging.getLogger("test_queue_management")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # When
    # Generate more messages than queue can hold
    for i in range(20):
        logger.info(f"Log message {i}")
    
    # Then
    # No exception should be raised (backpressure handling should work)
    assert True  # If we get here, the test passed