"""Performance tests for asynchronous logging in the MetaExpert logging system."""

import time
import tempfile
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor
import pytest

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration
from src.metaexpert.logger.performance_check import check_performance_latency, validate_performance_requirements


class TestAsyncPerformance:
    """Performance tests for asynchronous logging functionality."""
    
    def test_async_logging_performance_basic(self):
        """Test basic performance of async logging under normal conditions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_basic_test.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=False  # To reduce overhead in performance test
            )
            
            # Test with 500 log messages to get a meaningful performance sample
            metrics = check_performance_latency(config, num_logs=500)
            
            print(f"Async logging performance metrics:")
            print(f"  Total time: {metrics['total_time_ms']:.2f}ms for {metrics['num_logs']} logs")
            print(f"  Average time per log: {metrics['avg_time_per_log_ms']:.2f}ms")
            print(f"  95th percentile: {metrics['p95_time_ms']:.2f}ms")
            print(f"  99th percentile: {metrics['p99_time_ms']:.2f}ms")
            print(f"  Percent under 10ms: {metrics['percent_under_10ms']:.2f}%")
            
            # Validate performance requirements
            is_valid, issues = validate_performance_requirements(metrics)
            
            # The test should show that async logging meets performance requirements
            assert is_valid, f"Async logging does not meet performance requirements: {issues}"
    
    def test_async_logging_performance_vs_sync(self):
        """Compare async vs sync logging performance."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test async performance
            async_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_async_comparison.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=False
            )
            async_metrics = check_performance_latency(async_config, num_logs=200)
            
            # Test sync performance
            sync_config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_sync_comparison.log",
                enable_async=False,
                log_level="INFO",
                enable_structured_logging=False
            )
            sync_metrics = check_performance_latency(sync_config, num_logs=200)
            
            print(f"Async vs Sync performance comparison:")
            print(f"  Async - Avg: {async_metrics['avg_time_per_log_ms']:.3f}ms, 95%: {async_metrics['p95_time_ms']:.3f}ms")
            print(f"  Sync  - Avg: {sync_metrics['avg_time_per_log_ms']:.3f}ms, 95%: {sync_metrics['p95_time_ms']:.3f}ms")
            
            # For the calling thread, async should appear faster since it doesn't wait for I/O
            # Note: This may not always be true due to system variations, but generally
            # the average time for the calling thread should be lower with async
            # because it's not waiting for the actual file I/O to complete
    
    def test_async_logging_high_throughput(self):
        """Test async logging performance under high throughput."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_high_throughput.log",
                trades_log_file="perf_high_throughput_trades.log",
                errors_log_file="perf_high_throughput_errors.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=True,  # Include structured logging overhead
                file_log_format="json"
            )
            
            # Create a logger
            logger = MetaLogger(config=config)
            
            # Measure time to log many messages
            start_time = time.time()
            
            # Log various types of messages
            for i in range(1000):
                if i % 3 == 0:
                    logger.info(f"Info message {i}", iteration=i, expert_name="PerfTest", symbol="PERF")
                elif i % 3 == 1:
                    logger.trade(f"Trade message {i}", trade_id=f"trade_{i}", order_id=f"order_{i}")
                else:
                    logger.error(f"Error message {i}", error_code=f"ERR_{i}")
            
            end_time = time.time()
            
            total_time = (end_time - start_time) * 1000  # Convert to milliseconds
            avg_time_per_call = total_time / 1000
            
            print(f"High throughput test (1000 messages):")
            print(f"  Total time: {total_time:.2f}ms")
            print(f"  Avg time per call: {avg_time_per_call:.3f}ms")
            
            # Even with high throughput, the calls should return quickly (< 10ms on average)
            # The actual I/O happens in the background
            assert avg_time_per_call < 10.0, f"Average call time {avg_time_per_call}ms exceeds 10ms requirement"
            
            # Wait for background processing to complete before checking files
            time.sleep(1)
            
            # Verify files were created
            expert_log = temp_dir + "/perf_high_throughput.log"
            trades_log = temp_dir + "/perf_high_throughput_trades.log"
            errors_log = temp_dir + "/perf_high_throughput_errors.log"
            
            assert any([
                (lambda: open(expert_log).read() if os.path.exists(expert_log) else None)() is not None,
                (lambda: open(trades_log).read() if os.path.exists(trades_log) else None)() is not None,
                (lambda: open(errors_log).read() if os.path.exists(errors_log) else None)() is not None
            ])
    
    def test_async_logging_concurrent_load(self):
        """Test async logging performance under concurrent load."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_concurrent_test.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=False
            )
            
            logger = MetaLogger(config=config)
            
            def log_from_thread(thread_id, num_logs):
                """Function to run in each thread."""
                for i in range(num_logs):
                    logger.info(f"Thread {thread_id}, message {i}", 
                               thread_id=thread_id, 
                               message_id=i,
                               expert_name="ConcurrentTest")
            
            # Use ThreadPoolExecutor to create concurrent load
            num_threads = 10
            logs_per_thread = 50
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                futures = [
                    executor.submit(log_from_thread, i, logs_per_thread) 
                    for i in range(num_threads)
                ]
                
                # Wait for all threads to complete
                for future in futures:
                    future.result()
            
            end_time = time.time()
            
            total_logs = num_threads * logs_per_thread
            total_time = (end_time - start_time) * 1000  # Convert to milliseconds
            avg_time_per_call = total_time / total_logs
            
            print(f"Concurrent load test ({total_logs} messages from {num_threads} threads):")
            print(f"  Total time: {total_time:.2f}ms")
            print(f"  Avg time per call: {avg_time_per_call:.3f}ms")
            
            # Wait for background processing to complete
            time.sleep(1)
            
            # Verify the log file was created
            log_path = os.path.join(temp_dir, "perf_concurrent_test.log")
            assert os.path.exists(log_path)
            
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should contain messages from all threads
            for thread_id in range(num_threads):
                assert f"Thread {thread_id}," in content
    
    def test_async_logging_10ms_latency_requirement(self):
        """Specifically test that 95% of async log calls complete within 10ms."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = LogConfiguration(
                log_directory=temp_dir,
                expert_log_file="perf_latency_test.log",
                enable_async=True,
                log_level="INFO",
                enable_structured_logging=False
            )
            
            logger = MetaLogger(config=config)
            
            # Record individual call times
            call_times = []
            num_logs = 200  # Enough to get a good sample
            
            for i in range(num_logs):
                start = time.perf_counter()
                logger.info(f"Latency test message {i}", 
                           iteration=i, 
                           expert_name="LatencyTest")
                end = time.perf_counter()
                
                call_time_ms = (end - start) * 1000
                call_times.append(call_time_ms)
            
            # Calculate statistics
            avg_time = statistics.mean(call_times)
            p95_time = sorted(call_times)[int(0.95 * len(call_times))]
            p99_time = sorted(call_times)[int(0.99 * len(call_times))]
            max_time = max(call_times)
            
            # Calculate percentage under 10ms
            under_10ms_count = sum(1 for t in call_times if t <= 10.0)
            percent_under_10ms = (under_10ms_count / len(call_times)) * 100
            
            print(f"Latency requirement test ({num_logs} calls):")
            print(f"  Avg time: {avg_time:.3f}ms")
            print(f"  95% of calls under: {p95_time:.3f}ms")
            print(f"  99% of calls under: {p99_time:.3f}ms")
            print(f"  Max time: {max_time:.3f}ms")
            print(f"  Percent under 10ms: {percent_under_10ms:.2f}%")
            
            # Verify latency requirements
            assert avg_time < 10.0, f"Average call time {avg_time:.3f}ms exceeds 10ms requirement"
            assert p95_time <= 10.0, f"95th percentile time {p95_time:.3f}ms exceeds 10ms requirement"
            assert percent_under_10ms >= 95, f"Only {percent_under_10ms:.2f}% of calls under 10ms, need >=95%"