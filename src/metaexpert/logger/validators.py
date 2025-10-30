"""Event validation for MetaExpert logger."""

from typing import Any

from metaexpert.logger.constants import (
    ERROR_EVENT_REQUIRED_FIELDS,
    TRADE_EVENT_REQUIRED_FIELDS,
)


class LogEventValidator:
    """Validate log event structure and content."""

    @staticmethod
    def validate_trade_event(event: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate trade event structure.

        Args:
            event: Event dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        missing_fields = TRADE_EVENT_REQUIRED_FIELDS - set(event.keys())
        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate field types
        _validate_symbol(event, errors)
        _validate_side(event, errors)
        _validate_quantity(event, errors)
        _validate_price(event, errors)

        return len(errors) == 0, errors

    @staticmethod
    def validate_error_event(event: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate error event structure.

        Args:
            event: Event dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        missing_fields = ERROR_EVENT_REQUIRED_FIELDS - set(event.keys())
        if missing_fields:
            errors.append(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate level
        if "level" in event:
            level = event["level"]
            valid_levels = {"debug", "info", "warning", "error", "critical"}
            if level.lower() not in valid_levels:
                errors.append(f"level must be one of: {', '.join(valid_levels)}")

        # Validate message
        if "message" in event and not isinstance(event["message"], str):
            errors.append("message must be a string")

        return len(errors) == 0, errors

    @staticmethod
    def validate_general_event(event: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate general event structure.

        Args:
            event: Event dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check for common issues
        if not isinstance(event, dict):
            errors.append("Event must be a dictionary")
            return False, errors

        # Check for extremely large events (potential memory issues)
        event_size = len(str(event))
        if event_size > 1024 * 1024:  # 1MB
            errors.append(f"Event too large: {event_size} bytes (max 1MB)")

        # Check for suspicious patterns
        for key, value in event.items():
            if not isinstance(key, str):
                errors.append(f"Event key must be string, got: {type(key)}")

            if isinstance(value, (list, dict, set)) and len(str(value)) > 10000:
                errors.append(
                    f"Event value too large for key '{key}': {len(str(value))} chars"
                )

        return len(errors) == 0, errors

    @classmethod
    def validate_event(cls, event: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate event based on its type.

        Args:
            event: Event dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        event_type = event.get("event_type", "general")

        if event_type == "trade":
            return cls.validate_trade_event(event)
        elif event_type in ("error", "exception"):
            return cls.validate_error_event(event)
        else:
            return cls.validate_general_event(event)

    @staticmethod
    def sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
        """Sanitize event by removing problematic values.

        Args:
            event: Event dictionary to sanitize

        Returns:
            Sanitized event dictionary
        """
        sanitized = event.copy()

        # Remove None values to reduce noise
        sanitized = {k: v for k, v in sanitized.items() if v is not None}

        # Truncate extremely long strings
        for key, value in sanitized.items():
            if isinstance(value, str) and len(value) > 1000:
                sanitized[key] = value[:1000] + "..."

        # Convert non-serializable objects to strings
        for key, value in sanitized.items():
            try:
                import json

                json.dumps(value)
            except (TypeError, ValueError):
                sanitized[key] = str(value)

        return sanitized


def _validate_symbol(event: dict[str, Any], errors: list[str]) -> None:
    """Validate symbol field."""
    if "symbol" in event and not isinstance(event["symbol"], str):
        errors.append("symbol must be a string")


def _validate_side(event: dict[str, Any], errors: list[str]) -> None:
    """Validate side field."""
    if "side" in event:
        side = event["side"]
        if not isinstance(side, str) or side.upper() not in ["BUY", "SELL"]:
            errors.append("side must be 'BUY' or 'SELL'")


def _validate_quantity(event: dict[str, Any], errors: list[str]) -> None:
    """Validate quantity field."""
    if "quantity" in event:
        try:
            quantity = float(event["quantity"])
            if quantity <= 0:
                errors.append("quantity must be positive")
        except (ValueError, TypeError):
            errors.append("quantity must be a number")


def _validate_price(event: dict[str, Any], errors: list[str]) -> None:
    """Validate price field."""
    if "price" in event:
        try:
            price = float(event["price"])
            if price <= 0:
                errors.append("price must be positive")
        except (ValueError, TypeError):
            errors.append("price must be a number")


# Global validator instance
_validator = LogEventValidator()


def validate_log_event(event: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a log event using the global validator.

    Args:
        event: Event dictionary to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    return _validator.validate_event(event)


def sanitize_log_event(event: dict[str, Any]) -> dict[str, Any]:
    """Sanitize a log event using the global validator.

    Args:
        event: Event dictionary to sanitize

    Returns:
        Sanitized event dictionary
    """
    return _validator.sanitize_event(event)
