"""Unit tests for asynchronous logging in the MetaExpert logging system."""

import time
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration
from src.metaexpert.logger.handlers.async_file import AsyncFileHandler


class TestAsyncLogging:
    """Test cases for asynchronous logging functionality."""
    
    def test_async_file_handler_initialization(self):
        """Test that AsyncFileHandler initializes correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "async_test.log")
            handler = AsyncFileHandler(log_file)
            
            # Verify handler was created
            assert handler is not None
            assert handler.sync_handler is not None
            
            # Verify the worker thread started
            assert handler._worker_thread is not None
            assert handler._worker_thread.is_alive()
            
            # Close the handler to clean up
            handler.close()
    
    def test_async_file_handler_emit(self):
        """Test that AsyncFileHandler can emit log records."""
        import logging
        
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "async_emit_test.log")
            handler = AsyncFileHandler(log_file)
            
            # Create a mock log record
            record = logging.LogRecord(
                name="test",
                level=logging.INFO,
                pathname="",
                lineno=0,
                msg="Async test message",
                args=(),
                exc_info=None
            )
            
            # Emit the record (this adds it to the queue)
            handler.emit(record)
            
            # Wait a bit for the worker thread to process
            time.sleep(0.1)
            
            # Close the handler to ensure all records are processed
            handler.close()
            
            # Verify the log file was created and contains the message
            assert os.path.exists(log_file)
            
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Async test message" in content
    
    def test_async_logging_enabled(self):
        """Test that async logging works when enabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="async_enabled_test.log",
                enable_async=True,
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Log a message
            logger.info("Async logging test message", test_field="async_value")
            
            # Give the async worker time to process
            time.sleep(0.1)
            
            # Check that the log file was created
            log_path = os.path.join(temp_dir, "async_enabled_test.log")
            assert os.path.exists(log_path)
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Async logging test message" in content
            assert "async_value" in content
    
    def test_async_logging_disabled(self):
        """Test that non-async logging still works when disabled."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="async_disabled_test.log",
                enable_async=False,  # Explicitly disabled
                log_level="INFO"
            )
            
            logger = MetaLogger(config=config)
            
            # Log a message
            logger.info("Sync logging test message", test_field="sync_value")
            
            # The message should be written immediately
            log_path = os.path.join(temp_dir, "async_disabled_test.log")
            assert os.path.exists(log_path)
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "Sync logging test message" in content
            assert "sync_value" in content
    
    def test_async_vs_sync_behavior_difference(self):
        """Test the behavior difference between async and sync logging."""
        import time
        import threading
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create logs in both configurations
            async_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="async_timing_test.log",
                enable_async=True,
                log_level="INFO"
            )
            
            sync_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="sync_timing_test.log",
                enable_async=False,
                log_level="INFO"
            )
            
            async_logger = MetaLogger(config=async_config)
            sync_logger = MetaLogger(config=sync_config)
            
            # Time how long it takes to log many messages with async
            start_time = time.time()
            for i in range(100):
                async_logger.info(f"Async message {i}")
            async_time = time.time() - start_time
            
            # Time how long it takes to log many messages with sync
            start_time = time.time()
            for i in range(100):
                sync_logger.info(f"Sync message {i}")
            sync_time = time.time() - start_time
            
            # The async approach should generally be faster for the calling thread
            # since it just puts messages on a queue rather than performing I/O
            print(f"Async time for 100 messages: {async_time:.4f}s")
            print(f"Sync time for 100 messages: {sync_time:.4f}s")
            
            # Both should have created their files
            async_log_path = os.path.join(temp_dir, "async_timing_test.log")
            sync_log_path = os.path.join(temp_dir, "sync_timing_test.log")
            
            # Wait a bit for async processing to finish
            time.sleep(0.5)
            
            assert os.path.exists(async_log_path)
            assert os.path.exists(sync_log_path)
    
    def test_async_handler_thread_safety(self):
        """Test that async handler works with multiple threads."""
        import threading
        import time
        
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "async_thread_test.log")
            handler = AsyncFileHandler(log_file)
            
            def log_from_thread(thread_id):
                import logging
                for i in range(10):
                    record = logging.LogRecord(
                        name="test",
                        level=logging.INFO,
                        pathname="",
                        lineno=0,
                        msg=f"Thread {thread_id}, message {i}",
                        args=(),
                        exc_info=None
                    )
                    handler.emit(record)
            
            # Create multiple threads that will emit log records
            threads = []
            for thread_id in range(5):
                thread = threading.Thread(target=log_from_thread, args=(thread_id,))
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            # Wait for the async handler to process all messages
            time.sleep(0.5)
            
            # Close the handler to ensure all records are processed
            handler.close()
            
            # Verify the log file was created and contains messages from all threads
            assert os.path.exists(log_file)
            
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should contain messages from all threads
            for thread_id in range(5):
                assert f"Thread {thread_id}, message" in content