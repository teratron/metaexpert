"""Contract test for process exceptions in the MetaExpert library."""

import pytest
from metaexpert.core.exceptions import (
    ProcessError,
    InitializationError,
    ShutdownError,
    MetaExpertError
)


def test_process_error_inheritance():
    """Test that ProcessError inherits from MetaExpertError.
    
    Given a ProcessError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = ProcessError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_initialization_error_creation():
    """Test that InitializationError can be created with component name.
    
    Given a component name
    When InitializationError is created with the component name
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    component = "exchange_connector"
    
    # When
    exception = InitializationError(component)
    
    # Then
    assert exception.component == component
    assert "exchange_connector" in str(exception)


def test_initialization_error_inheritance():
    """Test that InitializationError inherits from ProcessError.
    
    Given an InitializationError instance
    When checking its type
    Then it should be an instance of ProcessError
    """
    # Given
    exception = InitializationError("exchange_connector")
    
    # When/Then
    assert isinstance(exception, ProcessError)


def test_shutdown_error_creation():
    """Test that ShutdownError can be created with component name.
    
    Given a component name
    When ShutdownError is created with the component name
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    component = "exchange_connector"
    
    # When
    exception = ShutdownError(component)
    
    # Then
    assert exception.component == component
    assert "exchange_connector" in str(exception)


def test_shutdown_error_inheritance():
    """Test that ShutdownError inherits from ProcessError.
    
    Given a ShutdownError instance
    When checking its type
    Then it should be an instance of ProcessError
    """
    # Given
    exception = ShutdownError("exchange_connector")
    
    # When/Then
    assert isinstance(exception, ProcessError)