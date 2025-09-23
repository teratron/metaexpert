# Backward Compatibility Integration Test

import pytest
import sys
from io import StringIO
from src.metaexpert.cli.argument_parser import parse_arguments

# Test that existing command-line usage patterns continue to work
def test_backward_compatibility():
    # Given existing command-line arguments that users are accustomed to
    test_args = ['--exchange', 'binance', '--pair', 'BTCUSDT']
    
    # Save original sys.argv
    original_argv = sys.argv
    
    # When parsing with the enhanced argument parser
    sys.argv = ['test'] + test_args
    try:
        parsed = parse_arguments()
        
        # Then the arguments should be parsed correctly as before
        assert parsed.exchange == 'binance'
        assert parsed.pair == 'BTCUSDT'
    finally:
        # Restore original sys.argv
        sys.argv = original_argv

# Test that the function can handle typical arguments
def test_typical_usage():
    # Given a typical set of command-line arguments
    test_args = ['--log-level', 'DEBUG', '--trade-mode', 'paper']
    
    # Save original sys.argv
    original_argv = sys.argv
    
    # When parsing with the enhanced argument parser
    sys.argv = ['test'] + test_args
    try:
        parsed = parse_arguments()
        
        # Then the arguments should be parsed correctly
        assert parsed.log_level == 'DEBUG'
        assert parsed.trade_mode == 'paper'
    finally:
        # Restore original sys.argv
        sys.argv = original_argv