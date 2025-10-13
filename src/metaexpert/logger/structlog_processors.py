"""
Structlog processors for MetaExpert logger module.

These processors ensure logs conform to the schema defined in data-model.md
while preserving compatibility with the existing QueueHandler mechanism.
"""

import datetime
import sys
from typing import Any


def add_log_severity(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Add log level/ severity to the event dict.

    Args:
        logger: The logger object
        method_name: The method name (debug, info, warning, etc.)
        event_dict: The event dictionary to process

    Returns:
        Updated event dictionary with severity information
    """
    # Map logging levels to our severity scale
    severity_map = {
        'debug': 'low',
        'info': 'low',
        'warning': 'medium',
        'error': 'high',
        'critical': 'critical'
    }

    event_dict['level'] = method_name.upper()
    event_dict['severity'] = severity_map.get(method_name, 'low')
    return event_dict


def add_source_location(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Add source location information to the event dict.

    Args:
        logger: The logger object
        method_name: The method name (debug, info, warning, etc.)
        event_dict: The event dictionary to process

    Returns:
        Updated event dictionary with source location
    """
    # This processor would add source location if available
    # For now, we'll add basic information about the logger
    try:
        frame = sys._getframe(5)  # Go up the stack to find the caller
        if frame:
            event_dict['source_path'] = frame.f_code.co_filename
            event_dict['function_name'] = frame.f_code.co_name
            event_dict['line_number'] = frame.f_lineno
    except (ValueError, AttributeError):
        # If we can't get frame info, continue without it
        pass
    return event_dict


def format_log_object(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Format the log object according to the data model schema.

    Args:
        logger: The logger object
        method_name: The method name (debug, info, warning, etc.)
        event_dict: The event dictionary to process

    Returns:
        Updated event dictionary following the schema from data-model.md
    """
    # Rename the 'event' key to 'event' if it exists (structlog default)
    if 'event' not in event_dict and event_dict.get('_record', {}).get('msg'):
        event_dict['event'] = event_dict['_record']['msg']
    elif '_record' in event_dict and 'msg' in event_dict['_record']:
        event_dict['event'] = event_dict['_record']['msg']
        del event_dict['_record']
    elif 'event' not in event_dict and len(event_dict) > 0:
        # If we don't have an explicit event, use the first non-special key or create one
        if 'msg' in event_dict:
            event_dict['event'] = event_dict['msg']
            del event_dict['msg']
        else:
            # Create event from the remaining keys
            event_dict['event'] = str(event_dict)

    # Ensure timestamp exists
    if 'timestamp' not in event_dict:
        event_dict['timestamp'] = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Add logger name if not present
    if 'logger_name' not in event_dict:
        event_dict['logger_name'] = getattr(logger, 'name', 'metaexpert.logger')

    return event_dict


def handle_non_serializable(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """
    Handle non-serializable objects in the event dictionary.

    Args:
        logger: The logger object
        method_name: The method name (debug, info, warning, etc.)
        event_dict: The event dictionary to process

    Returns:
        Updated event dictionary with only serializable values
    """
    for key, value in event_dict.items():
        try:
            # Test if the value is JSON serializable
            import json
            json.dumps(value)
        except (TypeError, ValueError):
            # If not serializable, convert to string representation
            event_dict[key] = repr(value)
    return event_dict


def prepare_for_stdlib_handler(
    logger: Any, method_name: str, event_dict: dict[str, Any]
) -> str:
    """
    Prepare the event dict for the underlying stdlib handler.

    Args:
        logger: The logger object
        method_name: The method name (debug, info, warning, etc.)
        event_dict: The event dictionary to process

    Returns:
        JSON string representation of the log event
    """
    # Apply all the processors to format the event_dict
    event_dict = add_log_severity(logger, method_name, event_dict)
    event_dict = format_log_object(logger, method_name, event_dict)
    event_dict = handle_non_serializable(logger, method_name, event_dict)

    # Convert to JSON string for output
    import json
    return json.dumps(event_dict, ensure_ascii=False)
