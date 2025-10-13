"""
Performance benchmarking script for logger throughput testing.
This script tests the logger's performance under high-frequency logging scenarios.
"""

import os
import tempfile
import time

from metaexpert.logger import MetaLogger


def benchmark_logger_throughput(num_messages=10000, message_size=100):
    """
    Benchmark the logger's throughput by logging a specified number of messages.

    Args:
        num_messages: Number of log messages to generate
        message_size: Size of each log message in characters

    Returns:
        dict: Performance metrics including time taken, throughput, etc.
    """
    # Create temporary log file
    temp_dir = tempfile.mkdtemp()
    log_file = os.path.join(temp_dir, "benchmark.log")
    
    # Initialize logger
    logger = MetaLogger(
        log_level="INFO",
        log_file="benchmark.log",
        trade_log_file="benchmark_trade.log",
        error_log_file="benchmark_error.log",
        log_to_console=False,
        structured_logging=True,  # Using structured logging for more realistic test
        async_logging=True,  # Enable async logging for performance
    )
    
    # Generate test message
    test_message = "A" * message_size
    
    # Start timing
    start_time = time.time()
    
    # Log the specified number of messages
    main_logger = logger.get_main_logger()
    for i in range(num_messages):
        main_logger.info(f"Test message {i}", 
                        message_id=i, 
                        test_data=test_message,
                        iteration=i)

    # End timing
    end_time = time.time()
    
    # Calculate metrics
    elapsed_time = end_time - start_time
    throughput = num_messages / elapsed_time if elapsed_time > 0 else float('inf')
    
    # Cleanup
    logger.shutdown()
    # Note: In a real scenario, we'd delete the temp files, but we'll leave them
    # for manual verification
    
    return {
        "num_messages": num_messages,
        "message_size": message_size,
        "elapsed_time": elapsed_time,
        "throughput": throughput,  # messages per second
        "avg_time_per_message": elapsed_time / num_messages if num_messages > 0 else 0,
        "test_completed": True
    }


def run_performance_tests():
    """Run various performance tests on the logger."""
    test_results = []
    
    # Test 1: Basic throughput test
    print("Running basic throughput test...")
    result1 = benchmark_logger_throughput(num_messages=1000, message_size=50)
    test_results.append(("Basic throughput (1000 messages)", result1))
    print(f"Completed: {result1['throughput']:.2f} messages/sec")
    
    # Test 2: High frequency test to meet requirement of 10,000 msg/sec
    print("Running high-frequency test...")
    result2 = benchmark_logger_throughput(num_messages=10000, message_size=100)
    test_results.append(("High frequency (10000 messages)", result2))
    print(f"Completed: {result2['throughput']:.2f} messages/sec")
    
    # Test 3: Large message test
    print("Running large message test...")
    result3 = benchmark_logger_throughput(num_messages=1000, message_size=500)
    test_results.append(("Large messages (500 chars)", result3))
    print(f"Completed: {result3['throughput']:.2f} messages/sec")
    
    return test_results


def verify_performance_requirements(results):
    """Verify the results against the required performance standards."""
    print("\n" + "="*50)
    print("PERFORMANCE REQUIREMENT VERIFICATION")
    print("="*50)
    
    # Requirement: Handle at least 10,000 messages per second
    high_freq_result = None
    for name, result in results:
        if "High frequency" in name:
            high_freq_result = result
            break
    
    if high_freq_result:
        print(f"High frequency test throughput: {high_freq_result['throughput']:.2f} messages/sec")
        if high_freq_result['throughput'] >= 10000:
            print("✅ PASSED: Meets 10,000 messages per second requirement")
        else:
            print("❌ FAILED: Does not meet 10,000 messages per second requirement")
    
    # Print all results for reference
    print("\nDetailed Results:")
    for test_name, result in results:
        print(f"- {test_name}: {result['throughput']:.2f} msg/sec")


if __name__ == "__main__":
    print("Starting logger performance benchmarking...")
    results = run_performance_tests()
    verify_performance_requirements(results)
    print("\nPerformance benchmarking complete.")