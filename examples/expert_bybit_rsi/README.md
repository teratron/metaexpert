# Bybit RSI Trading Expert

This is an example trading expert that implements a Relative Strength Index (RSI) strategy for trading on Bybit.

## Strategy Overview

The RSI strategy uses the Relative Strength Index indicator to identify overbought and oversold conditions:

- Buy signal when RSI crosses above 30 (oversold)
- Sell signal when RSI crosses below 70 (overbought)

## Configuration

1. Copy `.env.example` to `.env` and fill in your Bybit API credentials:

   ```env
   BYBIT_API_KEY="your_api_key"
   BYBIT_API_SECRET="your_api_secret"
   BYBIT_BASE_URL="your_base_url"  # Optional
   ```

2. Adjust the strategy parameters in the `@expert.on_init` decorator as needed.

## Running the Expert

```bash
python main.py
```

## Strategy Parameters

- **Symbols**: BTCUSDT
- **Timeframe**: 1 hour
- **Leverage**: 10x
- **Position Sizing**: Risk-based (1.5% of equity per trade)
- **Stop Loss**: 2%
- **Take Profit**: 4%
- **Trailing Stop**: 1%

## Implementation Notes

The actual RSI calculation and trading logic need to be implemented in the `bar()` function. The necessary imports (numpy, etc.) are commented out and should be uncommented when implementing the strategy.
