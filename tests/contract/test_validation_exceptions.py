"""Contract test for validation exceptions in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import (
    ValidationError,
    InvalidDataError,
    MissingDataError,
    MetaExpertError
)


def test_validation_error_inheritance():
    """Test that ValidationError inherits from MetaExpertError.
    
    Given a ValidationError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = ValidationError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_invalid_data_error_creation():
    """Test that InvalidDataError can be created with data and reason.
    
    Given invalid data and reason for validation failure
    When InvalidDataError is created with the parameters
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    data = {"invalid": "data"}
    reason = "Missing required fields"
    
    # When
    exception = InvalidDataError(data, reason)
    
    # Then
    assert exception.data == data
    assert exception.reason == reason
    assert "invalid" in str(exception)
    assert "data" in str(exception)
    assert "Missing required fields" in str(exception)


def test_invalid_data_error_inheritance():
    """Test that InvalidDataError inherits from ValidationError.
    
    Given an InvalidDataError instance
    When checking its type
    Then it should be an instance of ValidationError
    """
    # Given
    exception = InvalidDataError({"invalid": "data"}, "test reason")
    
    # When/Then
    assert isinstance(exception, ValidationError)


def test_missing_data_error_creation():
    """Test that MissingDataError can be created with field name.
    
    Given a field name
    When MissingDataError is created with the field name
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    field_name = "required_field"
    
    # When
    exception = MissingDataError(field_name)
    
    # Then
    assert exception.field_name == field_name
    assert "required_field" in str(exception)


def test_missing_data_error_inheritance():
    """Test that MissingDataError inherits from ValidationError.
    
    Given a MissingDataError instance
    When checking its type
    Then it should be an instance of ValidationError
    """
    # Given
    exception = MissingDataError("required_field")
    
    # When/Then
    assert isinstance(exception, ValidationError)