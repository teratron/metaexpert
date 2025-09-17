# Binance EMA Trading Expert

This is an example trading expert that implements an Exponential Moving Average (EMA) strategy for trading on Binance.

## Strategy Overview

The EMA strategy uses two exponential moving averages:

- Fast EMA (3 periods)
- Slow EMA (7 periods)

When the fast EMA crosses above the slow EMA, a buy signal is generated.
When the fast EMA crosses below the slow EMA, a sell signal is generated.

## Configuration

1. Copy `.env.example` to `.env` and fill in your Binance API credentials:

   ```env
   BINANCE_API_KEY="your_api_key"
   BINANCE_API_SECRET="your_api_secret"
   BINANCE_BASE_URL="https://testnet.binancefuture.com"  # For testnet
   ```

2. Adjust the strategy parameters in the `@expert.on_init` decorator as needed.

## Running the Expert

```bash
python __main__.py
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

The actual EMA calculation and trading logic need to be implemented in the `bar()` function. The necessary imports (numpy, talib) are commented out and should be uncommented when implementing the strategy.
