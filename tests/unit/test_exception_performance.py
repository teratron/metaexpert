"""Performance tests for exception handling in the MetaExpert library."""

import time
import pytest
from src.metaexpert.exceptions import MetaExpertError


def test_exception_creation_performance():
    """Test that creating exceptions has minimal overhead.
    
    Given the need to create many exceptions
    When creating exceptions in a loop
    Then the performance should be acceptable
    """
    # Measure time to create 1000 exceptions
    start_time = time.time()
    
    for i in range(1000):
        error = MetaExpertError(f"Test error {i}")
        str(error)  # Force string conversion
    
    end_time = time.time()
    
    # Calculate average time per exception
    avg_time = (end_time - start_time) / 1000
    
    # Should be less than 1ms per exception (very generous threshold)
    assert avg_time < 0.001, f"Average time per exception: {avg_time * 1000:.2f}ms"


def test_exception_inheritance_performance():
    """Test that exception inheritance has minimal overhead.
    
    Given the need to check exception types
    When checking isinstance for many exceptions
    Then the performance should be acceptable
    """
    # Create an exception
    error = MetaExpertError("Test error")
    
    # Measure time to check isinstance 1000 times
    start_time = time.time()
    
    for i in range(1000):
        isinstance(error, MetaExpertError)
        isinstance(error, Exception)
    
    end_time = time.time()
    
    # Calculate average time per check
    avg_time = (end_time - start_time) / 2000  # 2000 total checks
    
    # Should be less than 1μs per check (very generous threshold)
    assert avg_time < 0.000001, f"Average time per isinstance check: {avg_time * 1000000:.2f}μs"


def test_exception_string_conversion_performance():
    """Test that string conversion of exceptions has minimal overhead.
    
    Given the need to convert exceptions to strings
    When converting many exceptions to strings
    Then the performance should be acceptable
    """
    # Create an exception
    error = MetaExpertError("Test error message that is somewhat long to test string conversion performance")
    
    # Measure time to convert to string 1000 times
    start_time = time.time()
    
    for i in range(1000):
        str(error)
    
    end_time = time.time()
    
    # Calculate average time per conversion
    avg_time = (end_time - start_time) / 1000
    
    # Should be less than 10μs per conversion (reasonable threshold)
    assert avg_time < 0.00001, f"Average time per string conversion: {avg_time * 1000000:.2f}μs"