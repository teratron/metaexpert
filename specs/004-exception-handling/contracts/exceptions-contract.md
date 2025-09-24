# Exception Module API Contract

## Overview
This document describes the API contract for the MetaExpert exceptions module. The module provides a structured hierarchy of custom exception classes to handle various error conditions specific to the library.

## Module Interface

### Import
```python
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
```

## Exception Classes

### MetaExpertError
Base class for all custom exceptions in the MetaExpert library.

**Constructor**:
```python
MetaExpertError(message: str, *args)
```

**Attributes**:
- message (str): Human-readable error message
- args (tuple): Additional arguments

### ConfigurationError
Base class for configuration-related errors.

### InvalidConfigurationError
Raised when configuration values are invalid or missing.

**Constructor**:
```python
InvalidConfigurationError(config_key: str, config_value: Any, message: str = None)
```

**Attributes**:
- config_key (str): The configuration key that is invalid
- config_value (Any): The invalid configuration value
- message (str): Human-readable error message

### MissingConfigurationError
Raised when required configuration is missing.

**Constructor**:
```python
MissingConfigurationError(config_key: str, message: str = None)
```

**Attributes**:
- config_key (str): The missing configuration key
- message (str): Human-readable error message

### APIError
Base class for API-related errors.

### AuthenticationError
Raised when API authentication fails.

**Constructor**:
```python
AuthenticationError(exchange: str, message: str = None)
```

**Attributes**:
- exchange (str): The exchange where authentication failed
- message (str): Human-readable error message

### RateLimitError
Raised when API rate limits are exceeded.

**Constructor**:
```python
RateLimitError(exchange: str, retry_after: int = None, message: str = None)
```

**Attributes**:
- exchange (str): The exchange that imposed the rate limit
- retry_after (int): Seconds to wait before retrying (if provided by API)
- message (str): Human-readable error message

### NetworkError
Raised when there are network connectivity issues.

**Constructor**:
```python
NetworkError(url: str, reason: str = None, message: str = None)
```

**Attributes**:
- url (str): The URL that failed to connect
- reason (str): Reason for the network failure
- message (str): Human-readable error message

### TradingError
Base class for trading-related errors.

### InsufficientFundsError
Raised when there are insufficient funds for a trade.

**Constructor**:
```python
InsufficientFundsError(available: float, required: float, currency: str, message: str = None)
```

**Attributes**:
- available (float): Available funds
- required (float): Required funds
- currency (str): Currency code
- message (str): Human-readable error message

### InvalidOrderError
Raised when an order is invalid.

**Constructor**:
```python
InvalidOrderError(order_details: dict, message: str = None)
```

**Attributes**:
- order_details (dict): Details of the invalid order
- message (str): Human-readable error message

### OrderNotFoundError
Raised when an order cannot be found.

**Constructor**:
```python
OrderNotFoundError(order_id: str, message: str = None)
```

**Attributes**:
- order_id (str): The ID of the missing order
- message (str): Human-readable error message

### ValidationError
Base class for data validation errors.

### InvalidDataError
Raised when data is invalid or malformed.

**Constructor**:
```python
InvalidDataError(data: Any, reason: str = None, message: str = None)
```

**Attributes**:
- data (Any): The invalid data
- reason (str): Reason for the validation failure
- message (str): Human-readable error message

### MissingDataError
Raised when required data is missing.

**Constructor**:
```python
MissingDataError(field_name: str, message: str = None)
```

**Attributes**:
- field_name (str): The name of the missing field
- message (str): Human-readable error message

### MarketDataError
Base class for market data-related errors.

### UnsupportedPairError
Raised when a trading pair is not supported.

**Constructor**:
```python
UnsupportedPairError(pair: str, message: str = None)
```

**Attributes**:
- pair (str): The unsupported trading pair
- message (str): Human-readable error message

### InvalidTimeframeError
Raised when a timeframe is invalid.

**Constructor**:
```python
InvalidTimeframeError(timeframe: str, message: str = None)
```

**Attributes**:
- timeframe (str): The invalid timeframe
- message (str): Human-readable error message

### ProcessError
Base class for process-related errors.

### InitializationError
Raised when initialization fails.

**Constructor**:
```python
InitializationError(component: str, message: str = None)
```

**Attributes**:
- component (str): The component that failed to initialize
- message (str): Human-readable error message

### ShutdownError
Raised when shutdown fails.

**Constructor**:
```python
ShutdownError(component: str, message: str = None)
```

**Attributes**:
- component (str): The component that failed to shut down
- message (str): Human-readable error message