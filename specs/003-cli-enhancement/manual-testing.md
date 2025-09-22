# Manual Testing: CLI System Enhancement

## Purpose
This document provides instructions for manually testing the enhanced command-line interface in the MetaExpert library.

## Prerequisites
- Python 3.12 or higher
- MetaExpert library installed
- Sample trading strategy using the template.py file

## Test Scenarios

### 1. Basic CLI Functionality
1. Run `metaexpert --help` and verify that help documentation is properly organized
2. Run `metaexpert --new test_strategy` and verify that a new strategy is created
3. Run a sample strategy with various command-line arguments and verify correct parsing

### 2. Argument Grouping
1. Run `metaexpert --help` and verify that arguments are grouped logically
2. Run `metaexpert --help core` and verify that only core configuration arguments are shown
3. Test all argument group help commands

### 3. Backward Compatibility
1. Run existing command-line patterns that users are accustomed to
2. Verify that all existing short-form arguments still work
3. Verify that default values remain consistent with previous versions

### 4. Help Documentation
1. Review all help text for clarity and accuracy
2. Verify that examples are helpful and correct
3. Check that error messages are descriptive and helpful

### 5. Performance Testing
1. Measure argument parsing time for various command complexities
2. Verify that startup time is acceptable
3. Test with a large number of arguments to check for performance issues

### 6. Error Handling
1. Provide invalid argument values and verify appropriate error messages
2. Provide conflicting arguments and verify proper conflict detection
3. Omit required arguments and verify appropriate error messages

## Expected Results

### Basic CLI Functionality
- Help documentation should be clear and well-organized
- New strategy creation should work correctly
- Command-line arguments should be parsed correctly

### Argument Grouping
- Arguments should be logically grouped in help output
- Group-specific help should show only relevant arguments
- All arguments should be accessible through their groups

### Backward Compatibility
- All existing command-line patterns should continue to work
- All existing short-form arguments should work
- Default values should remain consistent

### Help Documentation
- Help text should be clear, accurate, and helpful
- Examples should be correct and illustrative
- Error messages should be descriptive

### Performance
- Argument parsing should be fast (<100ms in most cases)
- Startup time should be acceptable
- No performance degradation with complex commands

### Error Handling
- Invalid arguments should produce clear error messages
- Conflicting arguments should be detected and reported
- Missing required arguments should produce helpful error messages

## Troubleshooting

### Help Documentation Issues
- Check that all arguments have appropriate help text
- Verify that group descriptions are clear and accurate
- Ensure that examples are correct and helpful

### Performance Issues
- Check for unnecessary imports in the argument parsing module
- Verify that validation is efficient
- Review argument processing logic for optimization opportunities

### Compatibility Issues
- Verify that all existing argument names are preserved
- Check that default values remain consistent
- Ensure that deprecated arguments produce appropriate warnings

### Error Handling Issues
- Verify that error messages are clear and helpful
- Check that all validation rules are properly implemented
- Ensure that edge cases are handled appropriately