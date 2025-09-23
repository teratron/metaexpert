# MetaExpert Exception Handling

## Overview

The MetaExpert library provides a comprehensive exception hierarchy to handle various error conditions that may occur during trading operations. All custom exceptions inherit from the `MetaExpertError` base class, which itself inherits from Python's built-in `Exception` class.

## Exception Hierarchy

```text
Exception
└── MetaExpertError
    ├── ConfigurationError
    │   ├── InvalidConfigurationError
    │   └── MissingConfigurationError
    ├── APIError
    │   ├── AuthenticationError
    │   ├── RateLimitError
    │   └── NetworkError
    ├── TradingError
    │   ├── InsufficientFundsError
    │   ├── InvalidOrderError
    │   └── OrderNotFoundError
    ├── ValidationError
    │   ├── InvalidDataError
    │   └── MissingDataError
    ├── MarketDataError
    │   ├── UnsupportedPairError
    │   └── InvalidTimeframeError
    └── ProcessError
        ├── InitializationError
        └── ShutdownError
```

## Exception Classes

### MetaExpertError

Base class for all custom exceptions in the MetaExpert library.

**Constructor:**

```python
MetaExpertError(message: str, *args)
```

**Attributes:**

- `message` (str): Human-readable error message
- `args` (tuple): Additional arguments

### Configuration Exceptions

#### ConfigurationError

Base class for configuration-related errors.

#### InvalidConfigurationError

Raised when configuration values are invalid or missing.

**Constructor:**

```python
InvalidConfigurationError(config_key: str, config_value: Any, message: Optional[str] = None)
```

**Attributes:**

- `config_key` (str): The configuration key that is invalid
- `config_value` (Any): The invalid configuration value

#### MissingConfigurationError

Raised when required configuration is missing.

**Constructor:**

```python
MissingConfigurationError(config_key: str, message: Optional[str] = None)
```

**Attributes:**

- `config_key` (str): The missing configuration key

### API Exceptions

#### APIError

Base class for API-related errors.

#### AuthenticationError

Raised when API authentication fails.

**Constructor:**

```python
AuthenticationError(exchange: str, message: Optional[str] = None)
```

**Attributes:**

- `exchange` (str): The exchange where authentication failed

#### RateLimitError

Raised when API rate limits are exceeded.

**Constructor:**

```python
RateLimitError(exchange: str, retry_after: Optional[int] = None, message: Optional[str] = None)
```

**Attributes:**

- `exchange` (str): The exchange that imposed the rate limit
- `retry_after` (int): Seconds to wait before retrying (if provided by API)

#### NetworkError

Raised when there are network connectivity issues.

**Constructor:**

```python
NetworkError(url: str, reason: Optional[str] = None, message: Optional[str] = None)
```

**Attributes:**

- `url` (str): The URL that failed to connect
- `reason` (str): Reason for the network failure

### Trading Exceptions

#### TradingError

Base class for trading-related errors.

#### InsufficientFundsError

Raised when there are insufficient funds for a trade.

**Constructor:**

```python
InsufficientFundsError(available: float, required: float, currency: str, message: Optional[str] = None)
```

**Attributes:**

- `available` (float): Available funds
- `required` (float): Required funds
- `currency` (str): Currency code

#### InvalidOrderError

Raised when an order is invalid.

**Constructor:**

```python
InvalidOrderError(order_details: dict, message: Optional[str] = None)
```

**Attributes:**

- `order_details` (dict): Details of the invalid order

#### OrderNotFoundError

Raised when an order cannot be found.

**Constructor:**

```python
OrderNotFoundError(order_id: str, message: Optional[str] = None)
```

**Attributes:**

- `order_id` (str): The ID of the missing order

### Validation Exceptions

#### ValidationError

Base class for data validation errors.

#### InvalidDataError

Raised when data is invalid or malformed.

**Constructor:**

```python
InvalidDataError(data: Any, reason: Optional[str] = None, message: Optional[str] = None)
```

**Attributes:**

- `data` (Any): The invalid data
- `reason` (str): Reason for the validation failure

#### MissingDataError

Raised when required data is missing.

**Constructor:**

```python
MissingDataError(field_name: str, message: Optional[str] = None)
```

**Attributes:**

- `field_name` (str): The name of the missing field

### Market Data Exceptions

#### MarketDataError

Base class for market data-related errors.

#### UnsupportedPairError

Raised when a trading pair is not supported.

**Constructor:**

```python
UnsupportedPairError(pair: str, message: Optional[str] = None)
```

**Attributes:**

- `pair` (str): The unsupported trading pair

#### InvalidTimeframeError

Raised when a timeframe is invalid.

**Constructor:**

```python
InvalidTimeframeError(timeframe: str, message: Optional[str] = None)
```

**Attributes:**

- `timeframe` (str): The invalid timeframe

### Process Exceptions

#### ProcessError

Base class for process-related errors.

#### InitializationError

Raised when initialization fails.

**Constructor:**

```python
InitializationError(component: str, message: Optional[str] = None)
```

**Attributes:**

- `component` (str): The component that failed to initialize

#### ShutdownError

Raised when shutdown fails.

**Constructor:**

```python
ShutdownError(component: str, message: Optional[str] = None)
```

**Attributes:**

- `component` (str): The component that failed to shut down

## Usage Examples

### Basic Exception Handling

```python
from metaexpert.exceptions import MetaExpertError

try:
    # Some operation that might fail
    raise MetaExpertError("Something went wrong")
except MetaExpertError as e:
    print(f"Error: {e}")
```

### Handling Specific Exceptions

```python
from metaexpert.exceptions import InsufficientFundsError

try:
    # Trading operation
    place_order(symbol="BTCUSDT", quantity=1.0)
except InsufficientFundsError as e:
    print(f"Insufficient funds: {e.available} {e.currency} available, {e.required} {e.currency} required")
```

### Handling Multiple Exception Types

```python
from metaexpert.exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError
)

try:
    # API operation
    fetch_market_data(symbol="BTCUSDT")
except AuthenticationError as e:
    print(f"Authentication failed for {e.exchange}")
except NetworkError as e:
    print(f"Network error connecting to {e.url}: {e.reason}")
except RateLimitError as e:
    if e.retry_after:
        print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
    else:
        print(f"Rate limit exceeded for {e.exchange}")
```

## Best Practices

1. **Use Specific Exceptions**: Always use the most specific exception class for the error condition.
2. **Provide Meaningful Messages**: Include clear, actionable error messages.
3. **Handle Exceptions Appropriately**: Catch exceptions at the appropriate level in your code.
4. **Log Exceptions**: Log exceptions for debugging and monitoring purposes.
5. **Don't Ignore Exceptions**: Always handle or propagate exceptions appropriately.

## Integration with Existing Code

The exception hierarchy is designed to integrate seamlessly with existing MetaExpert components. When upgrading from previous versions, existing error handling code should continue to work, as all custom exceptions inherit from the standard Python `Exception` class.
