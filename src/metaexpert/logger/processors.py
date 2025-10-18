"""Processor functions for the MetaExpert logging system.

This module contains processor functions for structlog that handle
adding contextual information, timestamps, and other transformations
to log entries before they are formatted and output.
"""

import datetime
import re
from collections.abc import MutableMapping
from typing import Any


def add_timestamp(
    logger: Any,
    method_name: str,
    event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Add an ISO 8601 timestamp to the event dict."""
    event_dict['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return event_dict


def add_context(
    logger: Any,
    method_name: str,
    event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Add contextual information to the event dict if available."""
    # This processor should add any contextual information that's bound to the logger
    # structlog automatically handles bound context, so we just need to ensure all fields
    # are properly formatted
    return event_dict


def add_log_level(logger, method_name, event_dict):
    """Add the log level to the event dict."""
    event_dict['level'] = method_name
    return event_dict


def ensure_domain_context(logger, method_name, event_dict):
    """Ensure domain-specific context fields are properly included."""
    # Ensure the required domain context fields are present if they exist in the bound context
    required_fields = ['expert_name', 'symbol', 'trade_id', 'order_id', 'strategy_id', 'account_id']

    for field in required_fields:
        if field in event_dict:
            # Ensure the field is properly formatted
            # This is a no-op if the field is already there, but ensures consistency
            event_dict[field] = event_dict[field]

    return event_dict


def mask_sensitive_data(
    logger: Any,
    method_name: str,
    event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    """Mask sensitive information in the log entry."""
    # Define sensitive field patterns
    sensitive_patterns = [
        r'api[_-]?key',
        r'secret',
        r'password',
        r'token',
        r'account[_-]?id',
        r'access[_-]?token',
    ]

    # Process the message field if it exists
    if 'event' in event_dict and isinstance(event_dict['event'], str):
        event_dict['event'] = mask_text(event_dict['event'])

    # Process other fields in the event dict
    for key, value in event_dict.items():
        if isinstance(value, str):
            # Check if this key is a sensitive field
            for pattern in sensitive_patterns:
                if re.search(pattern, key, re.IGNORECASE):
                    event_dict[key] = '***MASKED***'
                    break
            else:
                # If not a sensitive field name, check if the value contains sensitive info
                event_dict[key] = mask_text(value)
        elif isinstance(value, (dict, list)):
            # For complex structures, apply masking recursively
            event_dict[key] = mask_sensitive_recursive(value)

    return event_dict




def mask_text(text: str) -> str:
    """Mask common sensitive patterns in text."""
    # Mask common API key patterns
    # This is a basic example, could be enhanced based on known formats
    import re

    # Mask API keys (sequences of 20+ alphanumeric chars)
    text = re.sub(r'\b([A-Za-z0-9]{20,})\b', '***MASKED***', text)

    # Mask potential account numbers (sequences of digits)
    # This is simplified and should be more specific in real implementation
    text = re.sub(r'\b\d{10,}\b', '***MASKED***', text)

    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***MASKED***', text)

    return text


def mask_sensitive_recursive(obj):
    """Recursively mask sensitive data in complex structures."""
    if isinstance(obj, dict):
        masked_dict = {}
        for key, value in obj.items():
            # Check if the key is a sensitive field
            if isinstance(key, str):
                # Mask if key matches sensitive pattern
                import re
                sensitive_patterns = [
                    r'api[_-]?key',
                    r'secret',
                    r'password',
                    r'token',
                    r'account[_-]?id',
                    r'access[_-]?token',
                ]

                for pattern in sensitive_patterns:
                    if re.search(pattern, key, re.IGNORECASE):
                        masked_dict[key] = '***MASKED***'
                        break
                else:
                    # If not sensitive key, mask the value if it's sensitive
                    masked_dict[key] = mask_sensitive_recursive(value)
            else:
                masked_dict[key] = mask_sensitive_recursive(value)
        return masked_dict
    elif isinstance(obj, list):
        return [mask_sensitive_recursive(item) for item in obj]
    elif isinstance(obj, str):
        return mask_text(obj)
    else:
        return obj
