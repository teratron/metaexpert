"""Acceptance tests for async logging in the MetaExpert logging system."""

import time
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
import pytest

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


class TestAsyncLoggingAcceptance:
    """Acceptance tests for user story 5: High-Performance Asynchronous Logging."""
    
    def test_main_trading_thread_not_blocked_by_logging(self):
        """Verify main trading thread is not blocked by logging (acceptance scenario 1)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a logger with async enabled
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="blocking_test.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=True  # This adds some processing overhead
            )
            
            logger = MetaLogger(config=config)
            
            # Simulate trading operations that generate many logs
            def simulate_trading_operation(operation_id):
                """Simulate a trading operation that needs to log frequently."""
                start_time = time.time()
                
                # Perform trading logic (simulated)
                for step in range(10):
                    # Log at each step of the trading operation
                    logger.info(f"Trading operation {operation_id}, step {step}",
                               operation_id=operation_id,
                               step=step,
                               expert_name="BlockingTestExpert",
                               symbol="BLOCK")
                    
                    # Simulate some trading logic processing
                    time.sleep(0.001)  # 1ms of "processing" time per step
                
                end_time = time.time()
                return end_time - start_time  # Return duration of the operation
            
            # Run multiple trading operations concurrently
            num_operations = 10
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_operations) as executor:
                futures = [
                    executor.submit(simulate_trading_operation, i) 
                    for i in range(num_operations)
                ]
                
                # Collect durations for each operation
                durations = [future.result() for future in futures]
            
            total_time = time.time() - start_time
            
            # Calculate average operation duration
            avg_duration = sum(durations) / len(durations)
            
            print(f"Blocking test results:")
            print(f"  Total time for {num_operations} operations: {total_time:.3f}s")
            print(f"  Average operation duration: {avg_duration:.3f}s ({avg_duration*1000:.1f}ms)")
            print(f"  Each operation does 10 log calls with 1ms processing each")
            
            # If logging was blocking, each operation would take at least 10ms 
            # (10 steps * 1ms processing each), plus logging time.
            # With async logging, the logging calls should return immediately,
            # so operations should complete mostly based on their processing time.
            expected_min_duration_per_operation = 0.01  # 10 steps * 1ms = 10ms = 0.01s
            blocking_threshold = expected_min_duration_per_operation * 0.8  # 80% of expected processing time
            
            # The key test: operations should not be significantly delayed by logging
            # If logging was blocking, we'd expect to see operations taking much longer
            assert avg_duration < expected_min_duration_per_operation * 2, \
                f"Operations taking too long ({avg_duration*1000:.1f}ms), " \
                f"indicating logging may be blocking the main thread"
            
            # Wait a bit for async logging to finish writing to files
            time.sleep(0.5)
            
            # Verify that log entries were created and written to the file
            log_path = os.path.join(temp_dir, "blocking_test.log")
            assert os.path.exists(log_path)
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should contain log entries from all operations
            for i in range(num_operations):
                assert f"Trading operation {i}," in content
            
            print(f"  Verified {content.count('Trading operation')} log entries were written")
    
    def test_async_logging_does_not_block_main_execution(self):
        """Additional test to ensure async logging doesn't block main execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test with async enabled
            async_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="non_blocking_async_test.log",
                enable_async=True,
                log_level="INFO"
            )
            
            async_logger = MetaLogger(config=async_config)
            
            # Record time for many log calls
            start_time = time.perf_counter()
            for i in range(500):
                async_logger.info(f"Async message {i}", iteration=i)
            async_time = time.perf_counter() - start_time
            
            # Wait for async processing to complete
            time.sleep(0.5)
            
            # Check with async disabled for comparison
            sync_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="non_blocking_sync_test.log",
                enable_async=False,
                log_level="INFO"
            )
            
            sync_logger = MetaLogger(config=sync_config)
            
            start_time = time.perf_counter()
            for i in range(500):
                sync_logger.info(f"Sync message {i}", iteration=i)
            sync_time = time.perf_counter() - start_time
            
            print(f"Non-blocking test:")
            print(f"  Async logging time (main thread): {async_time*1000:.2f}ms for 500 calls")
            print(f"  Sync logging time (main thread): {sync_time*1000:.2f}ms for 500 calls")
            
            # The async version should appear much faster to the main thread
            # since it doesn't wait for the actual file I/O to complete
            if sync_time > 0:  # Avoid division by zero
                speedup_ratio = sync_time / async_time if async_time > 0 else float('inf')
                print(f"  Speedup ratio (sync/async): {speedup_ratio:.2f}x")
            
            # Most importantly, the async calls should return very quickly to the main thread
            avg_async_time_per_call_ms = (async_time * 1000) / 500
            assert avg_async_time_per_call_ms < 10.0, \
                f"Async calls taking too long ({avg_async_time_per_call_ms:.2f}ms avg), " \
                f"should be under 10ms"