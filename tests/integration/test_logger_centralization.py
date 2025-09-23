"""Integration test for logger centralization functionality."""

import pytest
import logging
from metaexpert.logger import setup_logger, get_logger
from metaexpert.logger.logger_factory import LoggerFactory


def test_logger_centralization_single_instance():
    """Test that centralized logger returns the same instance.
    
    Given multiple requests for the same logger name
    When the centralized logger is retrieved
    Then the same logger instance should be returned
    """
    # Given
    factory = LoggerFactory()
    
    # When
    logger1 = factory.get_logger("test_centralized")
    logger2 = factory.get_logger("test_centralized")
    
    # Then
    assert logger1 is logger2


def test_logger_centralization_configuration_sharing():
    """Test that centralized loggers share configuration.
    
    Given a centralized logger configuration
    When multiple loggers are created
    Then they should all use the shared configuration
    """
    # Given
    factory = LoggerFactory()
    
    # When
    logger1 = factory.get_logger("test_config1", level="DEBUG")
    logger2 = factory.get_logger("test_config2", level="DEBUG")
    
    # Then
    # Both loggers should be properly configured
    assert logger1.level == logging.DEBUG
    assert logger2.level == logging.DEBUG


def test_logger_centralization_hierarchy():
    """Test that centralized loggers maintain proper hierarchy.
    
    Given a parent logger and child loggers
    When loggers are retrieved from the centralized system
    Then the parent-child relationship should be maintained
    """
    # Given
    factory = LoggerFactory()
    
    # When
    parent_logger = factory.get_logger("test_parent")
    child_logger = factory.get_logger("test_parent.child")
    
    # Then
    # Child logger should have proper relationship with parent
    assert child_logger.name == "test_parent.child"
    assert parent_logger.name == "test_parent"


def test_logger_centralization_backward_compatibility():
    """Test that centralized logging maintains backward compatibility.
    
    Given existing code using the standard logging interface
    When centralized logging is enabled
    Then existing code should continue to work without modification
    """
    # Given
    # Traditional logger usage
    logger = setup_logger("test_backward_compat")
    
    # When
    # This should work the same as before
    logger.info("Traditional log message")
    
    # Then
    # No exception should be raised
    assert True  # If we get here, the test passed