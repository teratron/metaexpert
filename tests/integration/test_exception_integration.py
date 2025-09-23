"""Integration test for exception handling in existing components."""

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


def test_exception_integration_with_metaexpert():
    """Test that exceptions integrate properly with MetaExpert core.
    
    Given a MetaExpert instance
    When exceptions are raised during operation
    Then they should be handled properly according to the exception hierarchy
    """
    # Test that we can import and use the exceptions
    try:
        raise MetaExpertError("Test MetaExpert error")
    except MetaExpertError as e:
        assert str(e) == "Test MetaExpert error"
    
    # Test configuration exceptions
    try:
        raise InvalidConfigurationError("api_key", "invalid_value")
    except InvalidConfigurationError as e:
        assert e.config_key == "api_key"
        assert e.config_value == "invalid_value"
        assert "api_key" in str(e)
        assert "invalid_value" in str(e)
    
    # Test that they integrate with standard exception handling
    try:
        raise MetaExpertError("Test error")
    except Exception as e:
        assert isinstance(e, MetaExpertError)


def test_exception_integration_with_exchange_modules():
    """Test that exceptions integrate properly with exchange modules.
    
    Given exchange modules
    When exceptions are raised during API interactions
    Then they should be handled properly according to the exception hierarchy
    """
    # Test API exceptions
    try:
        raise AuthenticationError("binance")
    except AuthenticationError as e:
        assert e.exchange == "binance"
        assert "binance" in str(e)
    
    try:
        raise RateLimitError("binance", 60)
    except RateLimitError as e:
        assert e.exchange == "binance"
        assert e.retry_after == 60
        assert "binance" in str(e)
        assert "60" in str(e)
    
    try:
        raise NetworkError("https://api.binance.com", "timeout")
    except NetworkError as e:
        assert e.url == "https://api.binance.com"
        assert e.reason == "timeout"
        assert "api.binance.com" in str(e)
        assert "timeout" in str(e)


def test_exception_integration_with_trading_modules():
    """Test that exceptions integrate properly with trading modules.
    
    Given trading modules
    When exceptions are raised during trading operations
    Then they should be handled properly according to the exception hierarchy
    """
    # Test trading exceptions
    try:
        raise InsufficientFundsError(100.0, 150.0, "USDT")
    except InsufficientFundsError as e:
        assert e.available == 100.0
        assert e.required == 150.0
        assert e.currency == "USDT"
        assert "100.0" in str(e)
        assert "150.0" in str(e)
        assert "USDT" in str(e)
    
    try:
        raise InvalidOrderError({"symbol": "BTCUSDT", "side": "BUY"})
    except InvalidOrderError as e:
        assert e.order_details == {"symbol": "BTCUSDT", "side": "BUY"}
        assert "BTCUSDT" in str(e)
        assert "BUY" in str(e)
    
    try:
        raise OrderNotFoundError("123456789")
    except OrderNotFoundError as e:
        assert e.order_id == "123456789"
        assert "123456789" in str(e)


def test_exception_integration_with_configuration_modules():
    """Test that exceptions integrate properly with configuration modules.
    
    Given configuration modules
    When exceptions are raised during configuration processing
    Then they should be handled properly according to the exception hierarchy
    """
    # Test configuration exceptions
    try:
        raise MissingConfigurationError("api_key")
    except MissingConfigurationError as e:
        assert e.config_key == "api_key"
        assert "api_key" in str(e)
    
    # Test validation exceptions
    try:
        raise InvalidDataError({"invalid": "data"}, "missing fields")
    except InvalidDataError as e:
        assert e.data == {"invalid": "data"}
        assert e.reason == "missing fields"
        assert "invalid" in str(e)
        assert "data" in str(e)
        assert "missing fields" in str(e)
    
    try:
        raise MissingDataError("required_field")
    except MissingDataError as e:
        assert e.field_name == "required_field"
        assert "required_field" in str(e)
    
    # Test market data exceptions
    try:
        raise UnsupportedPairError("INVALIDPAIR")
    except UnsupportedPairError as e:
        assert e.pair == "INVALIDPAIR"
        assert "INVALIDPAIR" in str(e)
    
    try:
        raise InvalidTimeframeError("invalid_timeframe")
    except InvalidTimeframeError as e:
        assert e.timeframe == "invalid_timeframe"
        assert "invalid_timeframe" in str(e)
    
    # Test process exceptions
    try:
        raise InitializationError("exchange_connector")
    except InitializationError as e:
        assert e.component == "exchange_connector"
        assert "exchange_connector" in str(e)
    
    try:
        raise ShutdownError("exchange_connector")
    except ShutdownError as e:
        assert e.component == "exchange_connector"
        assert "exchange_connector" in str(e)