"""Custom exceptions for the MetaExpert library.

This module provides a structured hierarchy of custom exception classes
to handle various error conditions specific to the MetaExpert library.
"""

from typing import Any


class MetaExpertError(Exception):
    """Base class for all custom exceptions in the MetaExpert library."""

    def __init__(self, message: str, *args: Any) -> None:
        """Initialize the MetaExpertError.

        Args:
            message: Human-readable error message
            *args: Additional arguments
        """
        super().__init__(message, *args)
        self.message = message
        self.args = args

    def __str__(self) -> str:
        """Return the string representation of the exception."""
        return self.message

# -----------------------------------------------------------------------------
# CONFIGURATION EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to configuration issues.
# -----------------------------------------------------------------------------
class ConfigurationError(MetaExpertError):
    """Base class for configuration-related errors."""

    pass


class InvalidConfigurationError(ConfigurationError):
    """Raised when configuration values are invalid or missing."""

    def __init__(
        self, config_key: str, config_value: Any, message: str | None = None
    ) -> None:
        """Initialize the InvalidConfigurationError.

        Args:
            config_key: The configuration key that is invalid
            config_value: The invalid configuration value
            message: Human-readable error message
        """
        if message is None:
            message = (
                f"Invalid configuration value '{config_value}' for key '{config_key}'"
            )
        super().__init__(message)
        self.config_key = config_key
        self.config_value = config_value


class MissingConfigurationError(ConfigurationError):
    """Raised when required configuration is missing."""

    def __init__(self, config_key: str, message: str | None = None) -> None:
        """Initialize the MissingConfigurationError.

        Args:
            config_key: The missing configuration key
            message: Human-readable error message
        """
        if message is None:
            message = f"Missing required configuration key '{config_key}'"
        super().__init__(message)
        self.config_key = config_key

# -----------------------------------------------------------------------------
# API EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to API interactions.
# -----------------------------------------------------------------------------
class APIError(MetaExpertError):
    """Base class for API-related errors."""

    pass


class AuthenticationError(APIError):
    """Raised when API authentication fails."""

    def __init__(self, exchange: str, message: str | None = None) -> None:
        """Initialize the AuthenticationError.

        Args:
            exchange: The exchange where authentication failed
            message: Human-readable error message
        """
        if message is None:
            message = f"Authentication failed for exchange '{exchange}'"
        super().__init__(message)
        self.exchange = exchange


class RateLimitError(APIError):
    """Raised when API rate limits are exceeded."""

    def __init__(
        self,
        exchange: str,
        retry_after: int | None = None,
        message: str | None = None,
    ) -> None:
        """Initialize the RateLimitError.

        Args:
            exchange: The exchange that imposed the rate limit
            retry_after: Seconds to wait before retrying (if provided by API)
            message: Human-readable error message
        """
        if message is None:
            if retry_after is not None:
                message = f"Rate limit exceeded for exchange '{exchange}'. Retry after {retry_after} seconds."
            else:
                message = f"Rate limit exceeded for exchange '{exchange}'."
        super().__init__(message)
        self.exchange = exchange
        self.retry_after = retry_after


class NetworkError(APIError):
    """Raised when there are network connectivity issues."""

    def __init__(
        self, url: str, reason: str | None = None, message: str | None = None
    ) -> None:
        """Initialize the NetworkError.

        Args:
            url: The URL that failed to connect
            reason: Reason for the network failure
            message: Human-readable error message
        """
        if message is None:
            if reason is not None:
                message = f"Network error connecting to '{url}': {reason}"
            else:
                message = f"Network error connecting to '{url}'"
        super().__init__(message)
        self.url = url
        self.reason = reason

# -----------------------------------------------------------------------------
# TRADING EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to trading operations.
# -----------------------------------------------------------------------------
class TradingError(MetaExpertError):
    """Base class for trading-related errors."""

    pass


class InsufficientFundsError(TradingError):
    """Raised when there are insufficient funds for a trade."""

    def __init__(
        self,
        available: float,
        required: float,
        currency: str,
        message: str | None = None,
    ) -> None:
        """Initialize the InsufficientFundsError.

        Args:
            available: Available funds
            required: Required funds
            currency: Currency code
            message: Human-readable error message
        """
        if message is None:
            message = f"Insufficient funds: {available} {currency} available, {required} {currency} required"
        super().__init__(message)
        self.available = available
        self.required = required
        self.currency = currency


class InvalidOrderError(TradingError):
    """Raised when an order is invalid."""

    def __init__(self, order_details: dict, message: str | None = None) -> None:
        """Initialize the InvalidOrderError.

        Args:
            order_details: Details of the invalid order
            message: Human-readable error message
        """
        if message is None:
            message = f"Invalid order: {order_details}"
        super().__init__(message)
        self.order_details = order_details


class OrderNotFoundError(TradingError):
    """Raised when an order cannot be found."""

    def __init__(self, order_id: str, message: str | None = None) -> None:
        """Initialize the OrderNotFoundError.

        Args:
            order_id: The ID of the missing order
            message: Human-readable error message
        """
        if message is None:
            message = f"Order not found: {order_id}"
        super().__init__(message)
        self.order_id = order_id

# -----------------------------------------------------------------------------
# DATA VALIDATION EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to data validation.
# -----------------------------------------------------------------------------
class ValidationError(MetaExpertError):
    """Base class for data validation errors."""

    pass


class InvalidDataError(ValidationError):
    """Raised when data is invalid or malformed."""

    def __init__(
        self, data: Any, reason: str | None = None, message: str | None = None
    ) -> None:
        """Initialize the InvalidDataError.

        Args:
            data: The invalid data
            reason: Reason for the validation failure
            message: Human-readable error message
        """
        if message is None:
            if reason is not None:
                message = f"Invalid data: {data}. Reason: {reason}"
            else:
                message = f"Invalid data: {data}"
        super().__init__(message)
        self.data = data
        self.reason = reason


class MissingDataError(ValidationError):
    """Raised when required data is missing."""

    def __init__(self, field_name: str, message: str | None = None) -> None:
        """Initialize the MissingDataError.

        Args:
            field_name: The name of the missing field
            message: Human-readable error message
        """
        if message is None:
            message = f"Missing required data field: '{field_name}'"
        super().__init__(message)
        self.field_name = field_name

# -----------------------------------------------------------------------------
# MARKET DATA EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to market data.
# -----------------------------------------------------------------------------
class MarketDataError(MetaExpertError):
    """Base class for market data-related errors."""

    pass


class UnsupportedPairError(MarketDataError):
    """Raised when a trading pair is not supported."""

    def __init__(self, pair: str, message: str | None = None) -> None:
        """Initialize the UnsupportedPairError.

        Args:
            pair: The unsupported trading pair
            message: Human-readable error message
        """
        if message is None:
            message = f"Unsupported trading pair: '{pair}'"
        super().__init__(message)
        self.pair = pair


class InvalidTimeframeError(MarketDataError):
    """Raised when a timeframe is invalid."""

    def __init__(self, timeframe: str, message: str | None = None) -> None:
        """Initialize the InvalidTimeframeError.

        Args:
            timeframe: The invalid timeframe
            message: Human-readable error message
        """
        if message is None:
            message = f"Invalid timeframe: '{timeframe}'"
        super().__init__(message)
        self.timeframe = timeframe

# -----------------------------------------------------------------------------
# PROCESS EXCEPTIONS
# -----------------------------------------------------------------------------
# These exceptions handle errors related to process management.
# -----------------------------------------------------------------------------
class ProcessError(MetaExpertError):
    """Base class for process-related errors."""

    pass


class InitializationError(ProcessError):
    """Raised when initialization fails."""

    def __init__(self, component: str, message: str | None = None) -> None:
        """Initialize the InitializationError.

        Args:
            component: The component that failed to initialize
            message: Human-readable error message
        """
        if message is None:
            message = f"Failed to initialize component: '{component}'"
        super().__init__(message)
        self.component = component


class ShutdownError(ProcessError):
    """Raised when shutdown fails."""

    def __init__(self, component: str, message: str | None = None) -> None:
        """Initialize the ShutdownError.

        Args:
            component: The component that failed to shut down
            message: Human-readable error message
        """
        if message is None:
            message = f"Failed to shut down component: '{component}'"
        super().__init__(message)
        self.component = component
