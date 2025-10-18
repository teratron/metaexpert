"""Unit tests for JSON formatter in the MetaExpert logging system."""

import json
import tempfile
import os

from src.metaexpert.logger.formatters import get_json_formatter


class TestJSONFormatter:
    """Test cases for JSON formatter functionality."""
    
    def test_json_formatter_basic_functionality(self):
        """Test that JSON formatter correctly formats basic event dicts."""
        formatter = get_json_formatter()
        
        # Create a basic event dict
        event_dict = {
            'timestamp': '2025-10-18T10:30:00.000Z',
            'level': 'info',
            'event': 'Test message'
        }
        
        result = formatter(None, None, event_dict)
        
        # Verify the result is valid JSON
        parsed = json.loads(result)
        
        assert parsed['timestamp'] == '2025-10-18T10:30:00.000Z'
        assert parsed['severity'] == 'info'  # Should be mapped to 'severity'
        assert parsed['message'] == 'Test message'  # Should be mapped to 'message'
    
    def test_json_formatter_with_domain_context_fields(self):
        """Test that JSON formatter includes domain context fields."""
        formatter = get_json_formatter()
        
        event_dict = {
            'timestamp': '2025-10-18T10:30:00.000Z',
            'level': 'info',
            'event': 'Trade executed',
            'expert_name': 'TestExpert',
            'symbol': 'BTCUSDT',
            'trade_id': 'trade_123',
            'order_id': 'order_456',
            'strategy_id': 'TestStrategy',
            'account_id': 'account_789'
        }
        
        result = formatter(None, None, event_dict)
        parsed = json.loads(result)
        
        # Verify all domain context fields are present
        assert parsed['expert_name'] == 'TestExpert'
        assert parsed['symbol'] == 'BTCUSDT'
        assert parsed['trade_id'] == 'trade_123'
        assert parsed['order_id'] == 'order_456'
        assert parsed['strategy_id'] == 'TestStrategy'
        assert parsed['account_id'] == 'account_789'
        
        # Verify standard fields are mapped correctly
        assert parsed['severity'] == 'info'
        assert parsed['message'] == 'Trade executed'
        assert parsed['timestamp'] == '2025-10-18T10:30:00.000Z'
    
    def test_json_formatter_additional_fields(self):
        """Test that JSON formatter preserves additional fields."""
        formatter = get_json_formatter()
        
        event_dict = {
            'timestamp': '2025-10-18T10:30:00.000Z',
            'level': 'warning',
            'event': 'Warning message',
            'expert_name': 'TestExpert',
            'custom_field': 'custom_value',
            'numeric_field': 123,
            'bool_field': True
        }
        
        result = formatter(None, None, event_dict)
        parsed = json.loads(result)
        
        # Verify standard fields
        assert parsed['severity'] == 'warning'
        assert parsed['message'] == 'Warning message'
        assert parsed['timestamp'] == '2025-10-18T10:30:00.000Z'
        
        # Verify domain context fields
        assert parsed['expert_name'] == 'TestExpert'
        
        # Verify additional custom fields are preserved
        assert parsed['custom_field'] == 'custom_value'
        assert parsed['numeric_field'] == 123
        assert parsed['bool_field'] is True
    
    def test_json_formatter_missing_required_fields(self):
        """Test that JSON formatter handles missing fields gracefully."""
        formatter = get_json_formatter()
        
        # Event dict with no timestamp
        event_dict = {
            'level': 'error',
            'event': 'Error occurred'
        }
        
        result = formatter(None, None, event_dict)
        parsed = json.loads(result)
        
        # Should have added a timestamp
        assert 'timestamp' in parsed
        assert parsed['severity'] == 'error'
        assert parsed['message'] == 'Error occurred'
    
    def test_json_formatter_no_event_field(self):
        """Test that JSON formatter handles missing event field."""
        formatter = get_json_formatter()
        
        # Event dict with no event field
        event_dict = {
            'timestamp': '2025-10-18T10:30:00.000Z',
            'level': 'info',
            'extra_field': 'value'
        }
        
        result = formatter(None, None, event_dict)
        parsed = json.loads(result)
        
        # Should have created a message from the whole dict
        assert 'timestamp' in parsed
        assert parsed['severity'] == 'info'
        assert 'extra_field' in parsed
        assert parsed['extra_field'] == 'value'
    
    def test_json_formatter_rfc5424_compliance(self):
        """Test that JSON formatter produces RFC 5424-like output."""
        formatter = get_json_formatter()
        
        event_dict = {
            'timestamp': '2025-10-18T10:30:00.000Z',
            'level': 'critical',
            'event': 'Critical system alert',
            'expert_name': 'SystemExpert',
            'symbol': 'SYS',
            'error_code': 'ERR-500'
        }
        
        result = formatter(None, None, event_dict)
        parsed = json.loads(result)
        
        # Check for RFC 5424 compliance: should have key fields
        required_keys = ['timestamp', 'severity', 'message']
        for key in required_keys:
            assert key in parsed, f"Missing required field: {key}"
        
        # Severity should be the level
        assert parsed['severity'] == 'critical'
        
        # Message should be the event
        assert parsed['message'] == 'Critical system alert'
        
        # Domain-specific fields should be preserved
        assert parsed['expert_name'] == 'SystemExpert'
        assert parsed['symbol'] == 'SYS'
        assert parsed['error_code'] == 'ERR-500'