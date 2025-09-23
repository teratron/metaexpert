"""Unit tests for argument validation utilities."""

import pytest
from src.metaexpert.cli.argument_validation import ArgumentValidationUtils, ArgumentValidationError


def test_validate_exchange():
    """Test exchange validation."""
    # Valid exchange should not raise an exception
    ArgumentValidationUtils.validate_exchange('binance', ['binance', 'bybit'])
    
    # Invalid exchange should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_exchange('invalid', ['binance', 'bybit'])


def test_validate_percentage():
    """Test percentage validation."""
    # Valid percentage should not raise an exception
    ArgumentValidationUtils.validate_percentage(50.0)
    
    # Invalid percentage should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_percentage(150.0)
        
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_percentage(-10.0)


def test_validate_positive_float():
    """Test positive float validation."""
    # Valid positive float should not raise an exception
    ArgumentValidationUtils.validate_positive_float(1.5)
    
    # Invalid negative float should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_positive_float(-1.5)
        
    # Zero should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_positive_float(0.0)


def test_validate_date_format():
    """Test date format validation."""
    # Valid date format should not raise an exception
    ArgumentValidationUtils.validate_date_format('2024-01-01')
    
    # Invalid date format should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_date_format('01-01-2024')
        
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_date_format('2024/01/01')


def test_validate_trading_pair():
    """Test trading pair validation."""
    # Valid trading pair should not raise an exception
    ArgumentValidationUtils.validate_trading_pair('BTCUSDT')
    
    # Invalid trading pair should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_trading_pair('invalid')


def test_validate_timeframe():
    """Test timeframe validation."""
    # Valid timeframe should not raise an exception
    ArgumentValidationUtils.validate_timeframe('1h')
    
    # Invalid timeframe should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_timeframe('invalid')


def test_validate_log_level():
    """Test log level validation."""
    # Valid log level should not raise an exception
    ArgumentValidationUtils.validate_log_level('INFO')
    
    # Invalid log level should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_log_level('invalid')


def test_validate_trade_mode():
    """Test trade mode validation."""
    # Valid trade mode should not raise an exception
    ArgumentValidationUtils.validate_trade_mode('paper')
    
    # Invalid trade mode should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_trade_mode('invalid')


def test_validate_market_type():
    """Test market type validation."""
    # Valid market type should not raise an exception
    ArgumentValidationUtils.validate_market_type('spot')
    
    # Invalid market type should raise an exception
    with pytest.raises(ArgumentValidationError):
        ArgumentValidationUtils.validate_market_type('invalid')