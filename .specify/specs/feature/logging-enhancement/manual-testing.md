# Manual Testing: Logging System Enhancement

## Purpose
This document provides instructions for manually testing the enhanced logging system in the MetaExpert library.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- Sample trading strategy using the template.py file

## Test Scenarios

### 1. Basic Logging Functionality
1. Create a new trading strategy using the `metaexpert new` command
2. Modify the strategy to include various log messages at different levels
3. Run the strategy and verify that logs are generated correctly
4. Check that logs appear in the correct files and console output

### 2. Structured Logging
1. Add structured data to log messages using the `extra` parameter
2. Verify that the structured data appears in the JSON-formatted logs
3. Check that structured data is searchable and parseable

### 3. Performance Testing
1. Create a high-frequency trading scenario that generates many log messages
2. Measure the performance impact of logging
3. Verify that async logging minimizes blocking of the main thread

### 4. Configuration Testing
1. Modify logging configuration in template.py
2. Verify that configuration changes take effect
3. Test different log levels and output destinations

### 5. Backward Compatibility
1. Test existing strategies that use the old logging system
2. Verify that they continue to work without modification
3. Check that log output format is consistent where expected

## Expected Results

### Basic Logging
- Log messages should appear at the correct level
- Log messages should be formatted correctly
- Log messages should appear in the correct destinations

### Structured Logging
- JSON-formatted logs should be valid JSON
- Structured data should be included in log entries
- Log fields should be consistent across all entries

### Performance
- Logging should have minimal impact on strategy performance
- Main thread should not be blocked by logging operations
- High-frequency logging should not cause system slowdown

### Configuration
- Configuration changes should take effect immediately
- Different log levels should filter messages correctly
- Multiple output destinations should work simultaneously

### Backward Compatibility
- Existing strategies should continue to work
- Old log format should still be available where needed
- No breaking changes to existing logging API

## Troubleshooting

### No Log Output
- Check that log level is set correctly
- Verify that log handlers are properly configured
- Ensure that log destinations are writable

### Performance Issues
- Check that async logging is enabled
- Verify that log level filtering is working
- Review log message complexity and frequency

### Configuration Problems
- Check that configuration file is properly formatted
- Verify that configuration values are valid
- Ensure that configuration changes are being applied