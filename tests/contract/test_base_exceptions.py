"""Contract test for base exceptions in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import MetaExpertError


def test_metaexpert_error_creation():
    """Test that MetaExpertError can be created with a message.
    
    Given a message for the exception
    When MetaExpertError is created with the message
    Then the exception should be created successfully with the correct message
    """
    # Given
    message = "Test error message"
    
    # When
    exception = MetaExpertError(message)
    
    # Then
    assert exception.message == message
    assert str(exception) == message


def test_metaexpert_error_inheritance():
    """Test that MetaExpertError inherits from Exception.
    
    Given a MetaExpertError instance
    When checking its type
    Then it should be an instance of Exception
    """
    # Given
    exception = MetaExpertError("Test error")
    
    # When/Then
    assert isinstance(exception, Exception)


def test_metaexpert_error_with_args():
    """Test that MetaExpertError can be created with additional arguments.
    
    Given a message and additional arguments
    When MetaExpertError is created with the message and arguments
    Then the exception should be created successfully with the correct message and args
    """
    # Given
    message = "Test error message"
    args = ("arg1", "arg2", 42)
    
    # When
    exception = MetaExpertError(message, *args)
    
    # Then
    assert exception.message == message
    assert exception.args == args