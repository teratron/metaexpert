"""Contract test for API exceptions in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
    MetaExpertError
)


def test_api_error_inheritance():
    """Test that APIError inherits from MetaExpertError.
    
    Given an APIError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = APIError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_authentication_error_creation():
    """Test that AuthenticationError can be created with exchange name.
    
    Given an exchange name
    When AuthenticationError is created with the exchange name
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    exchange = "binance"
    
    # When
    exception = AuthenticationError(exchange)
    
    # Then
    assert exception.exchange == exchange
    assert "binance" in str(exception)


def test_authentication_error_inheritance():
    """Test that AuthenticationError inherits from APIError.
    
    Given an AuthenticationError instance
    When checking its type
    Then it should be an instance of APIError
    """
    # Given
    exception = AuthenticationError("binance")
    
    # When/Then
    assert isinstance(exception, APIError)


def test_rate_limit_error_creation():
    """Test that RateLimitError can be created with exchange name and retry_after.
    
    Given an exchange name and optional retry_after value
    When RateLimitError is created with the parameters
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    exchange = "binance"
    retry_after = 60
    
    # When
    exception = RateLimitError(exchange, retry_after)
    
    # Then
    assert exception.exchange == exchange
    assert exception.retry_after == retry_after
    assert "binance" in str(exception)
    assert "60" in str(exception)


def test_rate_limit_error_inheritance():
    """Test that RateLimitError inherits from APIError.
    
    Given a RateLimitError instance
    When checking its type
    Then it should be an instance of APIError
    """
    # Given
    exception = RateLimitError("binance")
    
    # When/Then
    assert isinstance(exception, APIError)


def test_network_error_creation():
    """Test that NetworkError can be created with URL and reason.
    
    Given a URL and optional reason
    When NetworkError is created with the parameters
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    url = "https://api.binance.com"
    reason = "Connection timeout"
    
    # When
    exception = NetworkError(url, reason)
    
    # Then
    assert exception.url == url
    assert exception.reason == reason
    assert "api.binance.com" in str(exception)
    assert "Connection timeout" in str(exception)


def test_network_error_inheritance():
    """Test that NetworkError inherits from APIError.
    
    Given a NetworkError instance
    When checking its type
    Then it should be an instance of APIError
    """
    # Given
    exception = NetworkError("https://api.binance.com")
    
    # When/Then
    assert isinstance(exception, APIError)