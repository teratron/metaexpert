# Contract Tests: Exception Handling Module

These tests verify that the exception classes in the MetaExpert library conform to the defined API contract.

## Test Structure
Each test file validates one aspect of the exception module contract.

## Test Files to Create

1. `test_base_exceptions.py` - Tests for MetaExpertError base class
2. `test_configuration_exceptions.py` - Tests for configuration-related exceptions
3. `test_api_exceptions.py` - Tests for API-related exceptions
4. `test_trading_exceptions.py` - Tests for trading-related exceptions
5. `test_validation_exceptions.py` - Tests for validation-related exceptions
6. `test_market_data_exceptions.py` - Tests for market data-related exceptions
7. `test_process_exceptions.py` - Tests for process-related exceptions

## Test Requirements

### test_base_exceptions.py
```python
import pytest
from metaexpert.exceptions import MetaExpertError

def test_metaexpert_error_inheritance():
    """Test that MetaExpertError inherits from Exception"""
    assert issubclass(MetaExpertError, Exception)

def test_metaexpert_error_creation():
    """Test that MetaExpertError can be instantiated with a message"""
    error = MetaExpertError("Test error message")
    assert str(error) == "Test error message"

def test_metaexpert_error_with_args():
    """Test that MetaExpertError can be instantiated with additional arguments"""
    error = MetaExpertError("Test error", "arg1", "arg2")
    assert str(error) == "Test error"
    assert error.args == ("arg1", "arg2")
```

### test_configuration_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    ConfigurationError,
    InvalidConfigurationError,
    MissingConfigurationError
)

def test_configuration_error_inheritance():
    """Test that ConfigurationError inherits from MetaExpertError"""
    assert issubclass(ConfigurationError, MetaExpertError)

def test_invalid_configuration_error_creation():
    """Test that InvalidConfigurationError can be instantiated with required attributes"""
    error = InvalidConfigurationError("api_key", "invalid_value")
    assert error.config_key == "api_key"
    assert error.config_value == "invalid_value"

def test_invalid_configuration_error_message():
    """Test that InvalidConfigurationError has a proper error message"""
    error = InvalidConfigurationError("api_key", "invalid_value")
    assert "api_key" in str(error)
    assert "invalid_value" in str(error)

def test_missing_configuration_error_creation():
    """Test that MissingConfigurationError can be instantiated with required attributes"""
    error = MissingConfigurationError("api_secret")
    assert error.config_key == "api_secret"

def test_missing_configuration_error_message():
    """Test that MissingConfigurationError has a proper error message"""
    error = MissingConfigurationError("api_secret")
    assert "api_secret" in str(error)
```

### test_api_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    NetworkError
)

def test_api_error_inheritance():
    """Test that APIError inherits from MetaExpertError"""
    assert issubclass(APIError, MetaExpertError)

def test_authentication_error_creation():
    """Test that AuthenticationError can be instantiated with required attributes"""
    error = AuthenticationError("binance")
    assert error.exchange == "binance"

def test_authentication_error_message():
    """Test that AuthenticationError has a proper error message"""
    error = AuthenticationError("binance")
    assert "binance" in str(error)

def test_rate_limit_error_creation():
    """Test that RateLimitError can be instantiated with required attributes"""
    error = RateLimitError("binance", 60)
    assert error.exchange == "binance"
    assert error.retry_after == 60

def test_rate_limit_error_optional_retry():
    """Test that RateLimitError can be instantiated without retry_after"""
    error = RateLimitError("binance")
    assert error.exchange == "binance"
    assert error.retry_after is None

def test_network_error_creation():
    """Test that NetworkError can be instantiated with required attributes"""
    error = NetworkError("https://api.binance.com", "Connection timeout")
    assert error.url == "https://api.binance.com"
    assert error.reason == "Connection timeout"

def test_network_error_optional_reason():
    """Test that NetworkError can be instantiated without reason"""
    error = NetworkError("https://api.binance.com")
    assert error.url == "https://api.binance.com"
    assert error.reason is None
```

### test_trading_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    TradingError,
    InsufficientFundsError,
    InvalidOrderError,
    OrderNotFoundError
)

def test_trading_error_inheritance():
    """Test that TradingError inherits from MetaExpertError"""
    assert issubclass(TradingError, MetaExpertError)

def test_insufficient_funds_error_creation():
    """Test that InsufficientFundsError can be instantiated with required attributes"""
    error = InsufficientFundsError(100.0, 200.0, "USDT")
    assert error.available == 100.0
    assert error.required == 200.0
    assert error.currency == "USDT"

def test_insufficient_funds_error_message():
    """Test that InsufficientFundsError has a proper error message"""
    error = InsufficientFundsError(100.0, 200.0, "USDT")
    assert "100.0" in str(error)
    assert "200.0" in str(error)
    assert "USDT" in str(error)

def test_invalid_order_error_creation():
    """Test that InvalidOrderError can be instantiated with required attributes"""
    order_details = {"symbol": "BTCUSDT", "side": "BUY", "quantity": 1.0}
    error = InvalidOrderError(order_details)
    assert error.order_details == order_details

def test_order_not_found_error_creation():
    """Test that OrderNotFoundError can be instantiated with required attributes"""
    error = OrderNotFoundError("123456")
    assert error.order_id == "123456"

def test_order_not_found_error_message():
    """Test that OrderNotFoundError has a proper error message"""
    error = OrderNotFoundError("123456")
    assert "123456" in str(error)
```

### test_validation_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    ValidationError,
    InvalidDataError,
    MissingDataError
)

def test_validation_error_inheritance():
    """Test that ValidationError inherits from MetaExpertError"""
    assert issubclass(ValidationError, MetaExpertError)

def test_invalid_data_error_creation():
    """Test that InvalidDataError can be instantiated with required attributes"""
    data = {"invalid": "data"}
    error = InvalidDataError(data, "Malformed JSON")
    assert error.data == data
    assert error.reason == "Malformed JSON"

def test_invalid_data_error_message():
    """Test that InvalidDataError has a proper error message"""
    data = {"invalid": "data"}
    error = InvalidDataError(data, "Malformed JSON")
    assert "Malformed JSON" in str(error)

def test_missing_data_error_creation():
    """Test that MissingDataError can be instantiated with required attributes"""
    error = MissingDataError("timestamp")
    assert error.field_name == "timestamp"

def test_missing_data_error_message():
    """Test that MissingDataError has a proper error message"""
    error = MissingDataError("timestamp")
    assert "timestamp" in str(error)
```

### test_market_data_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    MarketDataError,
    UnsupportedPairError,
    InvalidTimeframeError
)

def test_market_data_error_inheritance():
    """Test that MarketDataError inherits from MetaExpertError"""
    assert issubclass(MarketDataError, MetaExpertError)

def test_unsupported_pair_error_creation():
    """Test that UnsupportedPairError can be instantiated with required attributes"""
    error = UnsupportedPairError("BTCUSD")
    assert error.pair == "BTCUSD"

def test_unsupported_pair_error_message():
    """Test that UnsupportedPairError has a proper error message"""
    error = UnsupportedPairError("BTCUSD")
    assert "BTCUSD" in str(error)

def test_invalid_timeframe_error_creation():
    """Test that InvalidTimeframeError can be instantiated with required attributes"""
    error = InvalidTimeframeError("5s")
    assert error.timeframe == "5s"

def test_invalid_timeframe_error_message():
    """Test that InvalidTimeframeError has a proper error message"""
    error = InvalidTimeframeError("5s")
    assert "5s" in str(error)
```

### test_process_exceptions.py
```python
import pytest
from metaexpert.exceptions import (
    ProcessError,
    InitializationError,
    ShutdownError
)

def test_process_error_inheritance():
    """Test that ProcessError inherits from MetaExpertError"""
    assert issubclass(ProcessError, MetaExpertError)

def test_initialization_error_creation():
    """Test that InitializationError can be instantiated with required attributes"""
    error = InitializationError("websocket_client")
    assert error.component == "websocket_client"

def test_initialization_error_message():
    """Test that InitializationError has a proper error message"""
    error = InitializationError("websocket_client")
    assert "websocket_client" in str(error)

def test_shutdown_error_creation():
    """Test that ShutdownError can be instantiated with required attributes"""
    error = ShutdownError("logger")
    assert error.component == "logger"

def test_shutdown_error_message():
    """Test that ShutdownError has a proper error message"""
    error = ShutdownError("logger")
    assert "logger" in str(error)
```