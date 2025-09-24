"""Performance tests for template creation and configuration management."""

import pytest
import time
import tempfile
import os

from metaexpert.template.template_service import TemplateCreationService
from metaexpert.services.config_service import ConfigurationManagementService
from metaexpert.template.template_creator import create_expert_from_template


def test_template_creation_performance():
    """Test that template creation completes within 200ms."""
    # Create a template creation service
    service = TemplateCreationService()
    
    # Measure the time it takes to load the template
    start_time = time.time()
    
    try:
        template_file = service.load_template()
        
        end_time = time.time()
        duration = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Check that it completed within 200ms
        assert duration < 200, f"Template loading took {duration:.2f}ms, which is longer than 200ms"
        
    except FileNotFoundError:
        # If template file doesn't exist, skip this test
        pytest.skip("Template file not found")


def test_template_creation_with_parameters_performance():
    """Test that template creation with parameters completes within 200ms."""
    # Create a temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "test_strategy.py")
        
        # Measure the time it takes to create a template
        start_time = time.time()
        
        try:
            result_path = create_expert_from_template(
                output_path,
                parameters={"exchange": "binance", "symbol": "BTCUSDT"}
            )
            
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Check that it completed within 200ms
            assert duration < 200, f"Template creation took {duration:.2f}ms, which is longer than 200ms"
            
            # Check that the file was created
            assert os.path.exists(result_path)
            
        except Exception as e:
            # If there's an error, report it
            pytest.fail(f"Template creation failed: {e}")


def test_configuration_parameter_retrieval_performance():
    """Test that configuration parameter retrieval completes within 200ms."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Measure the time it takes to get configuration parameters
    start_time = time.time()
    
    parameters = config_service.get_configuration_parameters()
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Check that it completed within 200ms
    assert duration < 200, f"Configuration parameter retrieval took {duration:.2f}ms, which is longer than 200ms"
    
    # Check that we got some parameters
    assert len(parameters) > 0


def test_configuration_validation_performance():
    """Test that configuration validation completes within 200ms."""
    # Create a configuration management service
    config_service = ConfigurationManagementService()
    
    # Create test configuration parameters
    test_config = {
        "exchange": "binance",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "api_key": "test_key",
        "api_secret": "test_secret"
    }
    
    # Measure the time it takes to validate configuration
    start_time = time.time()
    
    result = config_service.validate_configuration(test_config)
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Check that it completed within 200ms
    assert duration < 200, f"Configuration validation took {duration:.2f}ms, which is longer than 200ms"
    
    # Check that validation returned expected structure
    assert isinstance(result, dict)
    assert "valid" in result
    assert "errors" in result


def test_get_supported_exchanges_performance():
    """Test that getting supported exchanges completes within 200ms."""
    # Create a template creation service
    service = TemplateCreationService()
    
    # Measure the time it takes to get supported exchanges
    start_time = time.time()
    
    exchanges = service.get_supported_exchanges()
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Check that it completed within 200ms
    assert duration < 200, f"Getting supported exchanges took {duration:.2f}ms, which is longer than 200ms"
    
    # Check that we got some exchanges
    assert len(exchanges) > 0


def test_get_template_parameters_performance():
    """Test that getting template parameters completes within 200ms."""
    # Create a template creation service
    service = TemplateCreationService()
    
    # Measure the time it takes to get template parameters
    start_time = time.time()
    
    parameters = service.get_template_parameters()
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to milliseconds
    
    # Check that it completed within 200ms
    assert duration < 200, f"Getting template parameters took {duration:.2f}ms, which is longer than 200ms"
    
    # Check that we got some parameters
    assert len(parameters) > 0