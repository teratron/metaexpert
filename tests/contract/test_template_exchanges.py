"""Contract test for GET /template/exchanges endpoint."""

import pytest
from unittest.mock import patch, mock_open


def test_template_exchanges_success():
    """Test successful retrieval of supported exchanges.
    
    Given a request for supported exchanges
    When the template exchanges endpoint is called
    Then a success response with the list of exchanges should be returned
    """
    # Given
    request = {}
    
    # When
    # This test should fail initially as the implementation doesn't exist yet
    
    # Then
    assert False, "Not implemented"


def test_template_exchanges_with_filter():
    """Test retrieval of supported exchanges with filter.
    
    Given a request for supported exchanges with filter
    When the template exchanges endpoint is called
    Then a success response with the filtered list of exchanges should be returned
    """
    # Given
    request = {
        "filter": "futures"  # Filter for exchanges supporting futures
    }
    
    # When
    # This test should fail initially as the implementation doesn't exist yet
    
    # Then
    assert False, "Not implemented"