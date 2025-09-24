"""Contract test for configuration exceptions in the MetaExpert library."""

import pytest
from metaexpert.core.exceptions import (
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError,
    MetaExpertError
)


def test_configuration_error_inheritance():
    """Test that ConfigurationError inherits from MetaExpertError.
    
    Given a ConfigurationError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = ConfigurationError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_invalid_configuration_error_creation():
    """Test that InvalidConfigurationError can be created with config key and value.
    
    Given a config key and value
    When InvalidConfigurationError is created with the key and value
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    config_key = "api_key"
    config_value = "invalid_key"
    
    # When
    exception = InvalidConfigurationError(config_key, config_value)
    
    # Then
    assert exception.config_key == config_key
    assert exception.config_value == config_value
    assert "api_key" in str(exception)
    assert "invalid_key" in str(exception)


def test_invalid_configuration_error_inheritance():
    """Test that InvalidConfigurationError inherits from ConfigurationError.
    
    Given an InvalidConfigurationError instance
    When checking its type
    Then it should be an instance of ConfigurationError
    """
    # Given
    exception = InvalidConfigurationError("test_key", "test_value")
    
    # When/Then
    assert isinstance(exception, ConfigurationError)


def test_missing_configuration_error_creation():
    """Test that MissingConfigurationError can be created with config key.
    
    Given a config key
    When MissingConfigurationError is created with the key
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    config_key = "api_key"
    
    # When
    exception = MissingConfigurationError(config_key)
    
    # Then
    assert exception.config_key == config_key
    assert "api_key" in str(exception)


def test_missing_configuration_error_inheritance():
    """Test that MissingConfigurationError inherits from ConfigurationError.
    
    Given a MissingConfigurationError instance
    When checking its type
    Then it should be an instance of ConfigurationError
    """
    # Given
    exception = MissingConfigurationError("test_key")
    
    # When/Then
    assert isinstance(exception, ConfigurationError)