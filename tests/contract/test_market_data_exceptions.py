"""Contract test for market data exceptions in the MetaExpert library."""

import pytest
from src.metaexpert.exceptions import (
    MarketDataError,
    UnsupportedPairError,
    InvalidTimeframeError,
    MetaExpertError
)


def test_market_data_error_inheritance():
    """Test that MarketDataError inherits from MetaExpertError.
    
    Given a MarketDataError instance
    When checking its type
    Then it should be an instance of MetaExpertError
    """
    # Given
    exception = MarketDataError("Test error")
    
    # When/Then
    assert isinstance(exception, MetaExpertError)


def test_unsupported_pair_error_creation():
    """Test that UnsupportedPairError can be created with pair.
    
    Given a trading pair
    When UnsupportedPairError is created with the pair
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    pair = "INVALIDPAIR"
    
    # When
    exception = UnsupportedPairError(pair)
    
    # Then
    assert exception.pair == pair
    assert "INVALIDPAIR" in str(exception)


def test_unsupported_pair_error_inheritance():
    """Test that UnsupportedPairError inherits from MarketDataError.
    
    Given an UnsupportedPairError instance
    When checking its type
    Then it should be an instance of MarketDataError
    """
    # Given
    exception = UnsupportedPairError("INVALIDPAIR")
    
    # When/Then
    assert isinstance(exception, MarketDataError)


def test_invalid_timeframe_error_creation():
    """Test that InvalidTimeframeError can be created with timeframe.
    
    Given a timeframe
    When InvalidTimeframeError is created with the timeframe
    Then the exception should be created successfully with the correct attributes
    """
    # Given
    timeframe = "invalid_timeframe"
    
    # When
    exception = InvalidTimeframeError(timeframe)
    
    # Then
    assert exception.timeframe == timeframe
    assert "invalid_timeframe" in str(exception)


def test_invalid_timeframe_error_inheritance():
    """Test that InvalidTimeframeError inherits from MarketDataError.
    
    Given an InvalidTimeframeError instance
    When checking its type
    Then it should be an instance of MarketDataError
    """
    # Given
    exception = InvalidTimeframeError("invalid_timeframe")
    
    # When/Then
    assert isinstance(exception, MarketDataError)