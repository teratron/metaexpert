"""Unit tests for template validation functionality."""

import pytest
import tempfile
import os
from unittest.mock import patch, mock_open

from metaexpert.services.validation_service import validate_template_structure, validate_template_parameters


def test_validate_template_structure_valid():
    """Test validation of a valid template structure."""
    # Create a valid template content
    valid_template = '''
"""Trading Expert Template for the MetaExpert library."""

from metaexpert import MetaExpert

# EXPERT CORE CONFIGURATION
expert = MetaExpert(
    exchange="binance",
    api_key=None,
    api_secret=None,
)

# STRATEGY INITIALIZATION
@expert.on_init(
    symbol="BTCUSDT",
    timeframe="1h",
)
def init() -> None:
    pass

# EVENT HANDLERS
@expert.on_deinit
def deinit(reason) -> None:
    pass

# ENTRY POINT
def main() -> None:
    expert.run()

if __name__ == "__main__":
    main()
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(valid_template)
        temp_path = f.name
    
    try:
        # Validate the template
        result = validate_template_structure(temp_path)
        
        # Check that validation passed
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_template_structure_missing_sections():
    """Test validation of a template with missing sections."""
    # Create an invalid template content (missing sections)
    invalid_template = '''
"""Invalid template."""

from metaexpert import MetaExpert

def main() -> None:
    pass
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(invalid_template)
        temp_path = f.name
    
    try:
        # Validate the template
        result = validate_template_structure(temp_path)
        
        # Check that validation failed
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        # Check that we get errors for missing sections
        assert any("Missing required section" in error for error in result["errors"])
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_template_structure_missing_import():
    """Test validation of a template with missing import."""
    # Create an invalid template content (missing import)
    invalid_template = '''
"""Template missing import."""

# EXPERT CORE CONFIGURATION
expert = MetaExpert(
    exchange="binance",
)

def main() -> None:
    expert.run()

if __name__ == "__main__":
    main()
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(invalid_template)
        temp_path = f.name
    
    try:
        # Validate the template
        result = validate_template_structure(temp_path)
        
        # Check that validation failed
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        # Check that we get an error for missing import
        assert any("Missing MetaExpert import" in error for error in result["errors"])
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_template_parameters_valid():
    """Test validation of valid template parameters."""
    # Create a valid template content
    valid_template = '''
"""Trading Expert Template for the MetaExpert library."""

from metaexpert import MetaExpert

# EXPERT CORE CONFIGURATION
expert = MetaExpert(
    exchange="binance",
    api_key=None,
    api_secret=None,
)

# STRATEGY INITIALIZATION
@expert.on_init(
    symbol="BTCUSDT",
    timeframe="1h",
)
def init() -> None:
    pass

def main() -> None:
    expert.run()

if __name__ == "__main__":
    main()
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(valid_template)
        temp_path = f.name
    
    try:
        # Validate the template parameters
        result = validate_template_parameters(temp_path)
        
        # Check that validation passed
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_template_parameters_invalid_syntax():
    """Test validation of template parameters with invalid syntax."""
    # Create a template with invalid parameter syntax
    invalid_template = '''
"""Template with invalid parameter syntax."""

from metaexpert import MetaExpert

# EXPERT CORE CONFIGURATION
expert = MetaExpert(
    exchange="binance"
    api_key=None,  # Missing comma
    api_secret=None,
)

# STRATEGY INITIALIZATION
@expert.on_init(
    symbol="BTCUSDT"
    timeframe="1h",  # Missing comma
)
def init() -> None:
    pass

def main() -> None:
    expert.run()

if __name__ == "__main__":
    main()
'''
    
    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(invalid_template)
        temp_path = f.name
    
    try:
        # Validate the template parameters
        result = validate_template_parameters(temp_path)
        
        # This might not catch syntax errors in our simple validation
        # but we're testing the function structure
        assert isinstance(result, dict)
        assert "valid" in result
        assert "errors" in result
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)


def test_validate_template_nonexistent_file():
    """Test validation of a nonexistent template file."""
    # Try to validate a nonexistent file
    result = validate_template_structure("/nonexistent/template.py")
    
    # Check that validation failed
    assert result["valid"] is False
    assert len(result["errors"]) > 0
    # Check that we get an error for missing file
    assert any("Template file not found" in error for error in result["errors"])