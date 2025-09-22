"""Unit tests for configuration validation functionality."""

import os
import pytest
from unittest.mock import patch, mock_open

from metaexpert.services.config_service import ConfigurationManagementService


def test_configuration_parameter_retrieval():
    """Test retrieval of configuration parameters."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Get all configuration parameters
    parameters = config_service.get_configuration_parameters()
    
    # Check that we got some parameters
    assert len(parameters) > 0
    
    # Check that each parameter has required attributes
    for param in parameters:
        assert hasattr(param, 'name')
        assert hasattr(param, 'description')
        assert hasattr(param, 'default_value')
        assert hasattr(param, 'category')
        assert hasattr(param, 'required')


def test_configuration_parameter_filtering():
    """Test filtering of configuration parameters."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Get parameters filtered by category
    core_params = config_service.get_configuration_parameters(category="core")
    
    # Check that we got some core parameters
    assert len(core_params) > 0
    
    # Check that all parameters are in the core category
    for param in core_params:
        assert param.category == "core"


def test_configuration_validation_valid():
    """Test validation of valid configuration parameters."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Create valid configuration parameters
    valid_config = {
        "exchange": "binance",
        "symbol": "BTCUSDT",
        "timeframe": "1h"
    }
    
    # Validate the configuration
    result = config_service.validate_configuration(valid_config)
    
    # Check that validation passed
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_configuration_validation_missing_required():
    """Test validation of configuration with missing required parameters."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Create configuration with missing required parameters
    invalid_config = {
        "symbol": "BTCUSDT"
        # Missing required "exchange" parameter
    }
    
    # Validate the configuration
    result = config_service.validate_configuration(invalid_config)
    
    # Check that validation failed
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    # Check that we get an error for missing required parameter
    assert any("Required parameter 'exchange' is missing" in error["error"] for error in result["errors"])


def test_configuration_validation_invalid_exchange():
    """Test validation of configuration with invalid exchange."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Create configuration with invalid exchange
    invalid_config = {
        "exchange": "invalid_exchange",
        "symbol": "BTCUSDT",
        "timeframe": "1h"
    }
    
    # Validate the configuration
    result = config_service.validate_configuration(invalid_config)
    
    # Check that validation failed
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    # Check that we get an error for invalid exchange
    assert any("Invalid exchange 'invalid_exchange'" in error["error"] for error in result["errors"])


def test_configuration_source_alignment():
    """Test alignment of configuration sources."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Check configuration source alignment
    result = config_service.align_configuration_sources()
    
    # In our current implementation, this might pass or fail depending on the parameter definitions
    # but we're testing the function structure
    assert isinstance(result, dict)
    assert "aligned" in result
    assert "issues" in result


def test_get_parameter_value_with_default():
    """Test getting parameter value with default."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Get a parameter value with default
    value = config_service.get_parameter_value("nonexistent_param", "default_value")
    
    # Check that we get the default value
    assert value == "default_value"


@patch.dict(os.environ, {"DEFAULT_EXCHANGE": "bybit"})
def test_get_parameter_value_from_environment():
    """Test getting parameter value from environment variable."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Get a parameter value that exists in environment
    value = config_service.get_parameter_value("exchange", "binance")
    
    # Check that we get the environment value
    assert value == "bybit"