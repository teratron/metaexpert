"""Performance monitoring test for the enhanced logging system."""

import time
from metaexpert.logger.performance_monitor import (
    PerformanceMonitor, 
    start_operation, 
    end_operation, 
    record_metric, 
    get_performance_report,
    PerformanceTimer,
    time_operation
)


def test_performance_monitor_basic() -> None:
    """Test basic performance monitoring functionality."""
    # Create a performance monitor
    monitor = PerformanceMonitor()
    
    # Start an operation
    op_id = monitor.start_operation("test_operation")
    assert op_id is not None
    assert op_id.startswith("test_operation_")
    
    # Wait a bit to simulate work
    time.sleep(0.001)  # 1ms
    
    # End the operation
    monitor.end_operation(op_id, success=True)
    
    # Check that metrics were recorded
    report = monitor.get_performance_report()
    assert "total_operations" in report
    assert report["total_operations"] >= 1


def test_performance_monitor_decorator() -> None:
    """Test performance monitoring with decorator."""
    
    @time_operation("decorated_test")
    def slow_function() -> int:
        """A slow function to test timing."""
        time.sleep(0.001)  # 1ms
        return 42
    
    # Call the function
    result = slow_function()
    assert result == 42
    
    # Check that metrics were recorded
    report = get_performance_report()
    assert "total_operations" in report


def test_performance_monitor_context_manager() -> None:
    """Test performance monitoring with context manager."""
    
    # Use context manager to time an operation
    with PerformanceTimer("context_test"):
        time.sleep(0.001)  # 1ms
        result = 42 * 2
        
    assert result == 84
    
    # Check that metrics were recorded
    report = get_performance_report()
    assert "total_operations" in report


def test_performance_monitor_metrics() -> None:
    """Test custom metric recording."""
    
    # Record some metrics
    record_metric("test_metric", 42.5)
    record_metric("another_metric", 100, {"tag": "value"})
    
    # The metrics should be recorded (we can't easily test the logging output)
    # but we can at least verify the function doesn't crash


def test_performance_monitor_error_handling() -> None:
    """Test performance monitoring error handling."""
    
    # Test with invalid operation ID
    monitor = PerformanceMonitor()
    monitor.end_operation("invalid_id", success=True)
    
    # Should not crash
    
    # Test getting report with no data
    empty_monitor = PerformanceMonitor()
    report = empty_monitor.get_performance_report()
    assert "message" in report
    assert "No completed operations" in report["message"] or "No duration data" in report["message"]


if __name__ == "__main__":
    test_performance_monitor_basic()
    test_performance_monitor_decorator()
    test_performance_monitor_context_manager()
    test_performance_monitor_metrics()
    test_performance_monitor_error_handling()
    print("All performance monitoring tests passed!")