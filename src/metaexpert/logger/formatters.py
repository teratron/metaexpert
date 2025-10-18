"""Formatter functions for the MetaExpert logging system.

This module contains formatters for structlog that handle
formatting log entries for console and file output.
"""

import json
import structlog
from typing import Any
import datetime


def get_console_formatter():
    """Get the formatter for console output."""
    return structlog.dev.ConsoleRenderer()


def get_json_formatter():
    """Get the formatter for JSON output following RFC 5424."""
    def json_formatter(logger, name, event_dict):
        """Format the event dict as a JSON string following RFC 5424."""
        # Convert the event dict to RFC 5424 compliant format
        rfc5424_event = {}
        
        # Map standard fields to RFC 5424 equivalents
        if 'timestamp' in event_dict:
            rfc5424_event['timestamp'] = event_dict['timestamp']
        else:
            # Add timestamp if not present
            rfc5424_event['timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            
        if 'level' in event_dict:
            rfc5424_event['severity'] = event_dict['level']
        else:
            # Default to INFO if no level specified
            rfc5424_event['severity'] = 'info'
            
        if 'event' in event_dict:
            rfc5424_event['message'] = event_dict['event']
        else:
            # If there's no 'event' field, combine other fields into a message
            rfc5424_event['message'] = str(event_dict)
            
        # Add contextual fields specified in the requirements
        context_fields = ['expert_name', 'symbol', 'trade_id', 'order_id', 'strategy_id', 'account_id']
        for field in context_fields:
            if field in event_dict:
                rfc5424_event[field] = event_dict[field]
                
        # Add any additional fields that aren't part of the core structure
        for key, value in event_dict.items():
            if key not in ['timestamp', 'level', 'event'] + context_fields:
                rfc5424_event[key] = value
                
        return json.dumps(rfc5424_event, ensure_ascii=False)
    
    return json_formatter