"""Performance monitoring and metrics for the enhanced logging system."""

import time
import logging
from typing import Dict, Any, Optional
from collections import defaultdict
from threading import Lock


class PerformanceMonitor:
    """Monitor and track performance metrics for logging operations."""

    def __init__(self) -> None:
        """Initialize the performance monitor."""
        self.metrics: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.lock = Lock()
        self.logger = logging.getLogger("metaexpert.logger.performance")

    def start_operation(self, operation_name: str) -> str:
        """Start timing an operation.

        Args:
            operation_name: Name of the operation to track

        Returns:
            Operation ID for later completion tracking
        """
        operation_id = f"{operation_name}_{int(time.time() * 1000000)}"
        
        with self.lock:
            self.metrics[operation_id] = {
                "operation": operation_name,
                "start_time": time.time(),
                "end_time": None,
                "duration": None,
                "success": None
            }
            
        return operation_id

    def end_operation(self, operation_id: str, success: bool = True) -> None:
        """End timing an operation.

        Args:
            operation_id: ID of the operation to complete
            success: Whether the operation succeeded
        """
        end_time = time.time()
        
        with self.lock:
            if operation_id in self.metrics:
                metric = self.metrics[operation_id]
                metric["end_time"] = end_time
                metric["duration"] = end_time - metric["start_time"]
                metric["success"] = success
                
                # Log performance warning if operation took too long
                if metric["duration"] > 0.01:  # 10ms threshold
                    self.logger.warning(
                        "Slow operation detected: %s took %.2fms", 
                        metric["operation"], 
                        metric["duration"] * 1000
                    )

    def record_metric(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a custom metric.

        Args:
            metric_name: Name of the metric
            value: Value of the metric
            tags: Optional tags for the metric
        """
        # For simplicity, we'll just log the metric
        # In a real implementation, this would store metrics for aggregation
        tag_str = ""
        if tags:
            tag_str = " " + " ".join([f"{k}={v}" for k, v in tags.items()])
            
        self.logger.info("Metric recorded: %s=%.2f%s", metric_name, value, tag_str)

    def get_performance_report(self) -> Dict[str, Any]:
        """Get a performance report.

        Returns:
            Dictionary with performance metrics
        """
        with self.lock:
            # Calculate aggregate metrics
            completed_operations = [
                m for m in self.metrics.values() 
                if m["end_time"] is not None
            ]
            
            if not completed_operations:
                return {"message": "No completed operations to report"}
                
            total_operations = len(completed_operations)
            successful_operations = sum(1 for m in completed_operations if m["success"])
            failed_operations = total_operations - successful_operations
            
            durations = [m["duration"] for m in completed_operations if m["duration"] is not None]
            if not durations:
                return {"message": "No duration data available"}
                
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            # Group by operation type
            operation_stats = defaultdict(list)
            for m in completed_operations:
                operation_stats[m["operation"]].append(m["duration"])
                
            operation_summary = {}
            for op_name, durations in operation_stats.items():
                operation_summary[op_name] = {
                    "count": len(durations),
                    "avg_duration_ms": (sum(durations) / len(durations)) * 1000,
                    "min_duration_ms": min(durations) * 1000,
                    "max_duration_ms": max(durations) * 1000
                }
            
            return {
                "total_operations": total_operations,
                "successful_operations": successful_operations,
                "failed_operations": failed_operations,
                "success_rate": successful_operations / total_operations if total_operations > 0 else 0,
                "average_duration_ms": avg_duration * 1000,
                "min_duration_ms": min_duration * 1000,
                "max_duration_ms": max_duration * 1000,
                "operation_summary": operation_summary
            }


# Global performance monitor instance
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance.

    Returns:
        PerformanceMonitor instance
    """
    return _performance_monitor


def start_operation(operation_name: str) -> str:
    """Start timing an operation.

    Args:
        operation_name: Name of the operation to track

    Returns:
        Operation ID for later completion tracking
    """
    return _performance_monitor.start_operation(operation_name)


def end_operation(operation_id: str, success: bool = True) -> None:
    """End timing an operation.

    Args:
        operation_id: ID of the operation to complete
        success: Whether the operation succeeded
    """
    _performance_monitor.end_operation(operation_id, success)


def record_metric(metric_name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
    """Record a custom metric.

    Args:
        metric_name: Name of the metric
        value: Value of the metric
        tags: Optional tags for the metric
    """
    _performance_monitor.record_metric(metric_name, value, tags)


def get_performance_report() -> Dict[str, Any]:
    """Get a performance report.

    Returns:
        Dictionary with performance metrics
    """
    return _performance_monitor.get_performance_report()


class PerformanceTimer:
    """Context manager for timing operations."""

    def __init__(self, operation_name: str) -> None:
        """Initialize the performance timer.

        Args:
            operation_name: Name of the operation to time
        """
        self.operation_name = operation_name
        self.operation_id: Optional[str] = None

    def __enter__(self) -> "PerformanceTimer":
        """Start timing the operation."""
        self.operation_id = start_operation(self.operation_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """End timing the operation."""
        if self.operation_id:
            success = exc_type is None
            end_operation(self.operation_id, success)


# Convenience function for timing operations
def time_operation(operation_name: str):
    """Decorator to time an operation.

    Args:
        operation_name: Name of the operation to time

    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with PerformanceTimer(operation_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator