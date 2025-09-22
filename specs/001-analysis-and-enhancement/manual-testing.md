# Manual Testing for Template Enhancement

This document outlines the manual tests to verify the template enhancement implementation.

## Prerequisites

1. Python 3.12 or higher
2. UV package manager
3. Git

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd metaexpert
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Tests

### 1. Template Creation via CLI

Test creating a new template using the new CLI commands:

```bash
# Create a new strategy template
python -m metaexpert create my_test_strategy ./test_strategies

# Create a template with specific parameters
python -m metaexpert create my_test_strategy ./test_strategies --exchange binance --symbol BTCUSDT --timeframe 1h

# Check that the files were created
ls -la ./test_strategies/
```

### 2. List Supported Exchanges

Test listing supported exchanges:

```bash
python -m metaexpert exchanges
```

Expected output:
```
Supported exchanges:
  - binance
  - bybit
  - okx
  - bitget
  - kucoin
```

### 3. List Template Parameters

Test listing template parameters:

```bash
python -m metaexpert parameters
```

Expected output should show the core template parameters.

### 4. Validate Configuration

Test validating configuration parameters:

```bash
# Valid configuration
python -m metaexpert validate exchange=binance symbol=BTCUSDT timeframe=1h

# Invalid configuration (invalid exchange)
python -m metaexpert validate exchange=invalid_exchange symbol=BTCUSDT timeframe=1h
```

### 5. Template Structure Validation

Test that created templates have the correct structure:

1. Open the created template file
2. Verify it contains all required sections:
   - EXPERT CORE CONFIGURATION
   - STRATEGY INITIALIZATION
   - EVENT HANDLERS
   - ENTRY POINT
3. Verify it has the correct imports
4. Verify it has the correct main function and if-name-main block

### 6. Configuration Parameter Alignment

Test that configuration parameters are properly aligned:

1. Set environment variables:
   ```bash
   export DEFAULT_EXCHANGE=bybit
   export DEFAULT_SYMBOL=ETHUSDT
   ```

2. Create a template and verify the parameters are correctly applied

### 7. Template Customization

Test that templates can be customized with parameters:

1. Create a template with custom parameters:
   ```bash
   python -m metaexpert create custom_strategy ./test_strategies --exchange okx --symbol SOLUSDT --timeframe 5m
   ```

2. Verify the created template has the correct parameter values

## Cleanup

Remove test files:
```bash
rm -rf ./test_strategies/
```