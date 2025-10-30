"""Metrics and monitoring for MetaExpert logger."""

import threading
import time
from dataclasses import dataclass, field
from typing import Any

from metaexpert.logger.constants import (
    LOG_SIZE_WARNING_THRESHOLD_BYTES,
    SLOW_OPERATION_THRESHOLD_MS,
)


@dataclass
class LoggingMetrics:
    """Metrics for logging performance and usage."""

    # Basic counters
    log_calls_total: int = 0
    bytes_written_total: int = 0
    errors_total: int = 0
    warnings_total: int = 0

    # Performance metrics
    total_processing_time_ms: float = 0.0
    slow_operations_count: int = 0
    average_processing_time_ms: float = 0.0

    # Event type counters
    trade_events_total: int = 0
    error_events_total: int = 0
    debug_events_total: int = 0
    info_events_total: int = 0
    warning_events_total: int = 0
    critical_events_total: int = 0

    # File metrics
    files_rotated_total: int = 0
    max_file_size_reached_count: int = 0

    # Thread safety
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def increment_counter(self, counter_name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        with self._lock:
            current_value = getattr(self, counter_name, 0)
            setattr(self, counter_name, current_value + value)

    def record_timing(self, duration_ms: float) -> None:
        """Record timing metric."""
        with self._lock:
            self.log_calls_total += 1
            self.total_processing_time_ms += duration_ms
            self.average_processing_time_ms = (
                self.total_processing_time_ms / self.log_calls_total
            )

            if duration_ms > SLOW_OPERATION_THRESHOLD_MS:
                self.slow_operations_count += 1

    def record_bytes_written(self, bytes_count: int) -> None:
        """Record bytes written metric."""
        with self._lock:
            self.bytes_written_total += bytes_count
            if bytes_count > LOG_SIZE_WARNING_THRESHOLD_BYTES:
                self.max_file_size_reached_count += 1

    def record_event_type(self, event_type: str, level: str) -> None:
        """Record event type and level metrics."""
        with self._lock:
            if event_type == "trade":
                self.trade_events_total += 1

            level_counter_map = {
                "debug": "debug_events_total",
                "info": "info_events_total",
                "warning": "warning_events_total",
                "error": "error_events_total",
                "critical": "critical_events_total",
            }

            if level.lower() in level_counter_map:
                counter_name = level_counter_map[level.lower()]
                current_value = getattr(self, counter_name, 0)
                setattr(self, counter_name, current_value + 1)

            if level.lower() in ("error", "critical"):
                self.error_events_total += 1

    def record_error(self) -> None:
        """Record an error occurrence."""
        with self._lock:
            self.errors_total += 1

    def record_warning(self) -> None:
        """Record a warning occurrence."""
        with self._lock:
            self.warnings_total += 1

    def record_file_rotation(self) -> None:
        """Record a file rotation event."""
        with self._lock:
            self.files_rotated_total += 1

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of all metrics."""
        with self._lock:
            return {
                "total_log_calls": self.log_calls_total,
                "total_bytes_written": self.bytes_written_total,
                "total_errors": self.errors_total,
                "total_warnings": self.warnings_total,
                "slow_operations": self.slow_operations_count,
                "average_processing_time_ms": round(self.average_processing_time_ms, 2),
                "trade_events": self.trade_events_total,
                "error_events": self.error_events_total,
                "events_by_level": {
                    "debug": self.debug_events_total,
                    "info": self.info_events_total,
                    "warning": self.warning_events_total,
                    "error": self.error_events_total,
                    "critical": self.critical_events_total,
                },
                "files_rotated": self.files_rotated_total,
                "max_size_warnings": self.max_file_size_reached_count,
            }


# Global metrics instance
_global_metrics = LoggingMetrics()


def get_metrics() -> LoggingMetrics:
    """Get the global metrics instance."""
    return _global_metrics


def reset_metrics() -> None:
    """Reset all metrics to zero."""
    global _global_metrics
    _global_metrics = LoggingMetrics()


class MetricsContext:
    """Context manager for automatic metrics collection."""

    def __init__(self, operation_name: str = "log_processing"):
        self.operation_name = operation_name
        self.start_time: float = 0.0
        self.metrics = get_metrics()

    def __enter__(self) -> "MetricsContext":
        """Start timing and increment counter."""
        self.start_time = time.perf_counter()
        self.metrics.increment_counter("log_calls_total")
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Record timing and handle errors."""
        duration_ms = (time.perf_counter() - self.start_time) * 1000
        self.metrics.record_timing(duration_ms)

        if exc_type is not None:
            self.metrics.record_error()
        elif duration_ms > SLOW_OPERATION_THRESHOLD_MS:
            self.metrics.record_warning()
