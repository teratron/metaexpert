"""Integration test for exception hierarchy in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import (
    MetaExpertError,
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError,
    APIError,
    AuthenticationError,
    RateLimitError,
    NetworkError,
    TradingError,
    InsufficientFundsError,
    InvalidOrderError,
    OrderNotFoundError,
    ValidationError,
    InvalidDataError,
    MissingDataError,
    MarketDataError,
    UnsupportedPairError,
    InvalidTimeframeError,
    ProcessError,
    InitializationError,
    ShutdownError
)


def test_exception_hierarchy_structure():
    """Test that the exception hierarchy is properly structured.
    
    Given the exception classes
    When checking their inheritance relationships
    Then they should form the correct hierarchy as defined in the specification
    """
    # Test configuration exception hierarchy
    assert issubclass(ConfigurationError, MetaExpertError)
    assert issubclass(InvalidConfigurationError, ConfigurationError)
    assert issubclass(MissingConfigurationError, ConfigurationError)
    
    # Test API exception hierarchy
    assert issubclass(APIError, MetaExpertError)
    assert issubclass(AuthenticationError, APIError)
    assert issubclass(RateLimitError, APIError)
    assert issubclass(NetworkError, APIError)
    
    # Test trading exception hierarchy
    assert issubclass(TradingError, MetaExpertError)
    assert issubclass(InsufficientFundsError, TradingError)
    assert issubclass(InvalidOrderError, TradingError)
    assert issubclass(OrderNotFoundError, TradingError)
    
    # Test validation exception hierarchy
    assert issubclass(ValidationError, MetaExpertError)
    assert issubclass(InvalidDataError, ValidationError)
    assert issubclass(MissingDataError, ValidationError)
    
    # Test market data exception hierarchy
    assert issubclass(MarketDataError, MetaExpertError)
    assert issubclass(UnsupportedPairError, MarketDataError)
    assert issubclass(InvalidTimeframeError, MarketDataError)
    
    # Test process exception hierarchy
    assert issubclass(ProcessError, MetaExpertError)
    assert issubclass(InitializationError, ProcessError)
    assert issubclass(ShutdownError, ProcessError)


def test_base_exception_attributes():
    """Test that the base exception has the correct attributes.
    
    Given a MetaExpertError instance
    When accessing its attributes
    Then it should have the correct message and args
    """
    # Given
    message = "Test error message"
    args = ("arg1", "arg2", 42)
    
    # When
    exception = MetaExpertError(message, *args)
    
    # Then
    assert exception.message == message
    assert exception.args == args


def test_derived_exception_attributes():
    """Test that derived exceptions have the correct attributes.
    
    Given derived exception instances
    When accessing their attributes
    Then they should have the correct specific attributes
    """
    # Test configuration exceptions
    invalid_config = InvalidConfigurationError("api_key", "invalid")
    assert invalid_config.config_key == "api_key"
    assert invalid_config.config_value == "invalid"
    
    missing_config = MissingConfigurationError("api_secret")
    assert missing_config.config_key == "api_secret"
    
    # Test API exceptions
    auth_error = AuthenticationError("binance")
    assert auth_error.exchange == "binance"
    
    rate_error = RateLimitError("binance", 60)
    assert rate_error.exchange == "binance"
    assert rate_error.retry_after == 60
    
    network_error = NetworkError("https://api.binance.com", "timeout")
    assert network_error.url == "https://api.binance.com"
    assert network_error.reason == "timeout"
    
    # Test trading exceptions
    funds_error = InsufficientFundsError(100.0, 150.0, "USDT")
    assert funds_error.available == 100.0
    assert funds_error.required == 150.0
    assert funds_error.currency == "USDT"
    
    order_error = InvalidOrderError({"symbol": "BTCUSDT"})
    assert order_error.order_details == {"symbol": "BTCUSDT"}
    
    not_found_error = OrderNotFoundError("12345")
    assert not_found_error.order_id == "12345"
    
    # Test validation exceptions
    data_error = InvalidDataError({"invalid": "data"}, "missing fields")
    assert data_error.data == {"invalid": "data"}
    assert data_error.reason == "missing fields"
    
    missing_error = MissingDataError("required_field")
    assert missing_error.field_name == "required_field"
    
    # Test market data exceptions
    pair_error = UnsupportedPairError("INVALIDPAIR")
    assert pair_error.pair == "INVALIDPAIR"
    
    timeframe_error = InvalidTimeframeError("invalid_timeframe")
    assert timeframe_error.timeframe == "invalid_timeframe"
    
    # Test process exceptions
    init_error = InitializationError("exchange_connector")
    assert init_error.component == "exchange_connector"
    
    shutdown_error = ShutdownError("exchange_connector")
    assert shutdown_error.component == "exchange_connector"