"""Performance checks for the MetaExpert logging system to ensure 10ms latency requirement."""

import statistics
import tempfile
import time

from src.metaexpert.logger import MetaLogger
from src.metaexpert.logger.config import LogConfiguration


def check_performance_latency(config: LogConfiguration, num_logs: int = 1000) -> dict:
    """Check the performance of the logging system.

    Args:
        config: The LogConfiguration to test
        num_logs: Number of log messages to write for testing

    Returns:
        A dictionary with performance metrics
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a logger with the given configuration
        config.log_directory = temp_dir
        logger = MetaLogger(config=config)

        # Record start time
        start_time = time.perf_counter()

        # Record individual log times to measure latency
        log_times = []

        for i in range(num_logs):
            log_start = time.perf_counter()
            logger.info(
                f"Performance test message {i}",
                iteration=i,
                expert_name="PerformanceTest",
                symbol="PERF",
            )
            log_end = time.perf_counter()

            # Calculate time taken for this single log operation (in milliseconds)
            log_time_ms = (log_end - log_start) * 1000
            log_times.append(log_time_ms)

        end_time = time.perf_counter()

        # Calculate total time and average time per log
        total_time = (end_time - start_time) * 1000  # in milliseconds
        avg_time = total_time / num_logs
        median_time = statistics.median(log_times)
        max_time = max(log_times)

        # Calculate percentage of operations under 10ms
        under_10ms_count = sum(1 for t in log_times if t <= 10.0)
        percent_under_10ms = (under_10ms_count / len(log_times)) * 100

        return {
            "total_time_ms": total_time,
            "num_logs": num_logs,
            "avg_time_per_log_ms": avg_time,
            "median_time_ms": median_time,
            "max_time_ms": max_time,
            "log_times": log_times,
            "percent_under_10ms": percent_under_10ms,
            "p95_time_ms": sorted(log_times)[int(0.95 * len(log_times))]
            if log_times
            else 0,
            "p99_time_ms": sorted(log_times)[int(0.99 * len(log_times))]
            if log_times
            else 0,
        }


def validate_performance_requirements(
    metrics: dict, avg_threshold_ms: float = 10.0, p95_threshold_ms: float = 10.0
) -> tuple[bool, list[str]]:
    """Validate if the performance metrics meet the requirements.

    Args:
        metrics: Performance metrics from check_performance_latency
        avg_threshold_ms: Average time threshold in milliseconds
        p95_threshold_ms: 95th percentile threshold in milliseconds

    Returns:
        A tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Check if the average time is under the threshold
    if metrics["avg_time_per_log_ms"] > avg_threshold_ms:
        issues.append(
            f"Average log time ({metrics['avg_time_per_log_ms']:.2f}ms) "
            f"exceeds threshold ({avg_threshold_ms}ms)"
        )

    # Check if the p95 time is under the threshold
    if metrics["p95_time_ms"] > p95_threshold_ms:
        issues.append(
            f"95th percentile log time ({metrics['p95_time_ms']:.2f}ms) "
            f"exceeds threshold ({p95_threshold_ms}ms)"
        )

    # Check if less than 95% of operations are under 10ms
    if metrics["percent_under_10ms"] < 95:
        issues.append(
            f"Only {metrics['percent_under_10ms']:.2f}% of operations "
            f"are under 10ms (requirement: >=95%)"
        )

    # Check if any individual operation took more than 50ms (as a sanity check)
    if metrics["max_time_ms"] > 50:
        issues.append(
            f"Maximum log time ({metrics['max_time_ms']:.2f}ms) "
            f"exceeds reasonable threshold (50ms)"
        )

    return len(issues) == 0, issues


# Test function for use in performance validation
def run_performance_check():
    """Run the performance check for async logging."""
    print("Testing asynchronous logging performance...")

    # Test with async enabled
    async_config = LogConfiguration(
        enable_async=True,
        log_level="INFO",
        enable_structured_logging=False,  # Disabling structured logging for performance test
    )

    # Test with a smaller number of logs first to verify the approach
    async_metrics = check_performance_latency(async_config, num_logs=100)

    print("Asynchronous logging metrics:")
    print(
        f"  Total time: {async_metrics['total_time_ms']:.2f}ms for {async_metrics['num_logs']} logs"
    )
    print(f"  Average time per log: {async_metrics['avg_time_per_log_ms']:.2f}ms")
    print(f"  Median time per log: {async_metrics['median_time_ms']:.2f}ms")
    print(f"  95th percentile time: {async_metrics['p95_time_ms']:.2f}ms")
    print(f"  99th percentile time: {async_metrics['p99_time_ms']:.2f}ms")
    print(f"  Max time: {async_metrics['max_time_ms']:.2f}ms")
    print(f"  Percent under 10ms: {async_metrics['percent_under_10ms']:.2f}%")

    # Validate that the async logging meets requirements
    is_valid, issues = validate_performance_requirements(async_metrics)

    if is_valid:
        print("✓ Asynchronous logging meets performance requirements!")
    else:
        print("✗ Asynchronous logging does NOT meet performance requirements:")
        for issue in issues:
            print(f"  - {issue}")

    # Test with async disabled for comparison
    print("\nTesting synchronous logging performance for comparison...")
    sync_config = LogConfiguration(
        enable_async=False, log_level="INFO", enable_structured_logging=False
    )

    sync_metrics = check_performance_latency(sync_config, num_logs=100)

    print("Synchronous logging metrics:")
    print(f"  Average time per log: {sync_metrics['avg_time_per_log_ms']:.2f}ms")
    print(f"  95th percentile time: {sync_metrics['p95_time_ms']:.2f}ms")
    print(f"  Percent under 10ms: {sync_metrics['percent_under_10ms']:.2f}%")

    return async_metrics, sync_metrics


if __name__ == "__main__":
    run_performance_check()
