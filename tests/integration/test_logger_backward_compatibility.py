"""Backward compatibility test for the enhanced logger module."""

import logging
from metaexpert.logger import setup_logger, get_logger


def test_backward_compatibility():
    """Test that the enhanced logger maintains backward compatibility.
    
    This test verifies that existing code using the original logger
    interface continues to work without modification.
    """
    # Test the original setup_logger function
    logger1 = setup_logger("test_logger_1", "INFO")
    assert logger1 is not None
    assert isinstance(logger1, logging.Logger)
    
    # Test the original get_logger function
    logger2 = get_logger("test_logger_2")
    assert logger2 is not None
    assert isinstance(logger2, logging.Logger)
    
    # Test that both functions return loggers with the same name
    logger3 = get_logger("test_logger_1")
    assert logger3 is logger1  # Should return the same cached instance
    
    # Test basic logging functionality
    logger1.info("Backward compatibility test message")
    logger2.warning("Another test message")
    
    print("Backward compatibility test passed!")


if __name__ == "__main__":
    test_backward_compatibility()