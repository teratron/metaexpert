"""Contract test for trading exceptions in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import (
    TradingError,
    InsufficientFundsError,
    InvalidOrderError,
    OrderNotFoundError,
    MetaExpertError
)


def test_trading_error_inheritance():
    """Test that TradingError inherits from MetaExpertError.
    
    Given a TradingError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = TradingError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_insufficient_funds_error_creation():
    """Test that InsufficientFundsError can be created with available, required, and currency.
    
    Given available funds, required funds, and currency
    When InsufficientFundsError is created with the parameters
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    available = 100.0
    required = 150.0
    currency = "USDT"
    
    # When
    exception = InsufficientFundsError(available, required, currency)
    
    # Then
    assert exception.available == available
    assert exception.required == required
    assert exception.currency == currency
    assert "100.0" in str(exception)
    assert "150.0" in str(exception)
    assert "USDT" in str(exception)


def test_insufficient_funds_error_inheritance():
    """Test that InsufficientFundsError inherits from TradingError.
    
    Given an InsufficientFundsError instance
    When checking its type
    Then it should be an instance of TradingError
    """
    # Given
    exception = InsufficientFundsError(100.0, 150.0, "USDT")
    
    # When/Then
    assert isinstance(exception, TradingError)


def test_invalid_order_error_creation():
    """Test that InvalidOrderError can be created with order details.
    
    Given order details
    When InvalidOrderError is created with the details
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    order_details = {"symbol": "BTCUSDT", "side": "BUY", "quantity": 1.0}
    
    # When
    exception = InvalidOrderError(order_details)
    
    # Then
    assert exception.order_details == order_details
    assert "BTCUSDT" in str(exception)
    assert "BUY" in str(exception)


def test_invalid_order_error_inheritance():
    """Test that InvalidOrderError inherits from TradingError.
    
    Given an InvalidOrderError instance
    When checking its type
    Then it should be an instance of TradingError
    """
    # Given
    exception = InvalidOrderError({"symbol": "BTCUSDT", "side": "BUY"})
    
    # When/Then
    assert isinstance(exception, TradingError)


def test_order_not_found_error_creation():
    """Test that OrderNotFoundError can be created with order ID.
    
    Given an order ID
    When OrderNotFoundError is created with the ID
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    order_id = "123456789"
    
    # When
    exception = OrderNotFoundError(order_id)
    
    # Then
    assert exception.order_id == order_id
    assert "123456789" in str(exception)


def test_order_not_found_error_inheritance():
    """Test that OrderNotFoundError inherits from TradingError.
    
    Given an OrderNotFoundError instance
    When checking its type
    Then it should be an instance of TradingError
    """
    # Given
    exception = OrderNotFoundError("123456789")
    
    # When/Then
    assert isinstance(exception, TradingError)