#!/usr/bin/env python3
"""Test script for CLI argument parsing without importing problematic modules."""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now test the argument parser module directly
from metaexpert.cli.argument_parser import create_argument_parser

# Create parser and print help to verify it works
parser = create_argument_parser()
print("Argument parser created successfully!")
print("\nHelp output:")
parser.print_help()