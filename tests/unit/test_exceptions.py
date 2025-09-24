"""Unit tests for exception classes in the MetaExpert library."""

import pytest
from metaexpert.core.exceptions import (
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


def test_metaexpert_error():
    """Test MetaExpertError class."""
    # Test basic creation
    error = MetaExpertError("Test error")
    assert str(error) == "Test error"
    assert error.message == "Test error"
    
    # Test with args
    error = MetaExpertError("Test error", "arg1", "arg2")
    assert str(error) == "Test error"
    assert error.message == "Test error"
    assert error.args == ("arg1", "arg2")


def test_configuration_errors():
    """Test configuration exception classes."""
    # Test ConfigurationError
    error = ConfigurationError("Config error")
    assert isinstance(error, MetaExpertError)
    
    # Test InvalidConfigurationError
    error = InvalidConfigurationError("api_key", "invalid_value")
    assert isinstance(error, ConfigurationError)
    assert error.config_key == "api_key"
    assert error.config_value == "invalid_value"
    assert "api_key" in str(error)
    assert "invalid_value" in str(error)
    
    # Test InvalidConfigurationError with custom message
    error = InvalidConfigurationError("api_key", "invalid_value", "Custom message")
    assert str(error) == "Custom message"
    
    # Test MissingConfigurationError
    error = MissingConfigurationError("api_secret")
    assert isinstance(error, ConfigurationError)
    assert error.config_key == "api_secret"
    assert "api_secret" in str(error)
    
    # Test MissingConfigurationError with custom message
    error = MissingConfigurationError("api_secret", "Custom message")
    assert str(error) == "Custom message"


def test_api_errors():
    """Test API exception classes."""
    # Test APIError
    error = APIError("API error")
    assert isinstance(error, MetaExpertError)
    
    # Test AuthenticationError
    error = AuthenticationError("binance")
    assert isinstance(error, APIError)
    assert error.exchange == "binance"
    assert "binance" in str(error)
    
    # Test AuthenticationError with custom message
    error = AuthenticationError("binance", "Custom message")
    assert str(error) == "Custom message"
    
    # Test RateLimitError
    error = RateLimitError("binance", 60)
    assert isinstance(error, APIError)
    assert error.exchange == "binance"
    assert error.retry_after == 60
    assert "binance" in str(error)
    assert "60" in str(error)
    
    # Test RateLimitError without retry_after
    error = RateLimitError("binance")
    assert error.retry_after is None
    assert "binance" in str(error)
    
    # Test RateLimitError with custom message
    error = RateLimitError("binance", 60, "Custom message")
    assert str(error) == "Custom message"
    
    # Test NetworkError
    error = NetworkError("https://api.binance.com", "timeout")
    assert isinstance(error, APIError)
    assert error.url == "https://api.binance.com"
    assert error.reason == "timeout"
    assert "api.binance.com" in str(error)
    assert "timeout" in str(error)
    
    # Test NetworkError without reason
    error = NetworkError("https://api.binance.com")
    assert error.reason is None
    assert "api.binance.com" in str(error)
    
    # Test NetworkError with custom message
    error = NetworkError("https://api.binance.com", "timeout", "Custom message")
    assert str(error) == "Custom message"


def test_trading_errors():
    """Test trading exception classes."""
    # Test TradingError
    error = TradingError("Trading error")
    assert isinstance(error, MetaExpertError)
    
    # Test InsufficientFundsError
    error = InsufficientFundsError(100.0, 150.0, "USDT")
    assert isinstance(error, TradingError)
    assert error.available == 100.0
    assert error.required == 150.0
    assert error.currency == "USDT"
    assert "100.0" in str(error)
    assert "150.0" in str(error)
    assert "USDT" in str(error)
    
    # Test InsufficientFundsError with custom message
    error = InsufficientFundsError(100.0, 150.0, "USDT", "Custom message")
    assert str(error) == "Custom message"
    
    # Test InvalidOrderError
    error = InvalidOrderError({"symbol": "BTCUSDT", "side": "BUY"})
    assert isinstance(error, TradingError)
    assert error.order_details == {"symbol": "BTCUSDT", "side": "BUY"}
    assert "BTCUSDT" in str(error)
    assert "BUY" in str(error)
    
    # Test InvalidOrderError with custom message
    error = InvalidOrderError({"symbol": "BTCUSDT"}, "Custom message")
    assert str(error) == "Custom message"
    
    # Test OrderNotFoundError
    error = OrderNotFoundError("123456789")
    assert isinstance(error, TradingError)
    assert error.order_id == "123456789"
    assert "123456789" in str(error)
    
    # Test OrderNotFoundError with custom message
    error = OrderNotFoundError("123456789", "Custom message")
    assert str(error) == "Custom message"


def test_validation_errors():
    """Test validation exception classes."""
    # Test ValidationError
    error = ValidationError("Validation error")
    assert isinstance(error, MetaExpertError)
    
    # Test InvalidDataError
    error = InvalidDataError({"invalid": "data"}, "missing fields")
    assert isinstance(error, ValidationError)
    assert error.data == {"invalid": "data"}
    assert error.reason == "missing fields"
    assert "invalid" in str(error)
    assert "data" in str(error)
    assert "missing fields" in str(error)
    
    # Test InvalidDataError without reason
    error = InvalidDataError({"invalid": "data"})
    assert error.reason is None
    assert "invalid" in str(error)
    assert "data" in str(error)
    
    # Test InvalidDataError with custom message
    error = InvalidDataError({"invalid": "data"}, "missing fields", "Custom message")
    assert str(error) == "Custom message"
    
    # Test MissingDataError
    error = MissingDataError("required_field")
    assert isinstance(error, ValidationError)
    assert error.field_name == "required_field"
    assert "required_field" in str(error)
    
    # Test MissingDataError with custom message
    error = MissingDataError("required_field", "Custom message")
    assert str(error) == "Custom message"


def test_market_data_errors():
    """Test market data exception classes."""
    # Test MarketDataError
    error = MarketDataError("Market data error")
    assert isinstance(error, MetaExpertError)
    
    # Test UnsupportedPairError
    error = UnsupportedPairError("INVALIDPAIR")
    assert isinstance(error, MarketDataError)
    assert error.pair == "INVALIDPAIR"
    assert "INVALIDPAIR" in str(error)
    
    # Test UnsupportedPairError with custom message
    error = UnsupportedPairError("INVALIDPAIR", "Custom message")
    assert str(error) == "Custom message"
    
    # Test InvalidTimeframeError
    error = InvalidTimeframeError("invalid_timeframe")
    assert isinstance(error, MarketDataError)
    assert error.timeframe == "invalid_timeframe"
    assert "invalid_timeframe" in str(error)
    
    # Test InvalidTimeframeError with custom message
    error = InvalidTimeframeError("invalid_timeframe", "Custom message")
    assert str(error) == "Custom message"


def test_process_errors():
    """Test process exception classes."""
    # Test ProcessError
    error = ProcessError("Process error")
    assert isinstance(error, MetaExpertError)
    
    # Test InitializationError
    error = InitializationError("exchange_connector")
    assert isinstance(error, ProcessError)
    assert error.component == "exchange_connector"
    assert "exchange_connector" in str(error)
    
    # Test InitializationError with custom message
    error = InitializationError("exchange_connector", "Custom message")
    assert str(error) == "Custom message"
    
    # Test ShutdownError
    error = ShutdownError("exchange_connector")
    assert isinstance(error, ProcessError)
    assert error.component == "exchange_connector"
    assert "exchange_connector" in str(error)
    
    # Test ShutdownError with custom message
    error = ShutdownError("exchange_connector", "Custom message")
    assert str(error) == "Custom message"