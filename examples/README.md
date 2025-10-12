# MetaExpert Examples

This directory contains example trading experts that demonstrate how to use the MetaExpert library to create automated trading strategies.

## Available Examples

1. [Binance EMA Expert](expert_binance_ema/) - An Exponential Moving Average strategy for Binance
2. [Bybit RSI Expert](expert_bybit_rsi/) - A Relative Strength Index strategy for Bybit
3. [OKX MACD Expert](expert_okx_macd/) - A Moving Average Convergence Divergence strategy for OKX

## Getting Started

1. Navigate to the directory of the example you want to try
2. Copy `.env.example` to `.env` and fill in your API credentials
3. Install dependencies: `pip install -e .` (or use uv: `uv sync`)
4. Run the expert: `python main.py`

## Customization

Each example can be customized by modifying:

- API credentials in the `.env` file
- Strategy parameters in the `@expert.on_init` decorator
- Trading logic in the event handlers (especially the `bar()` function)

## Implementation Notes

The examples include placeholders for the actual trading logic. You'll need to:

1. Uncomment the necessary imports (numpy, etc.)
2. Implement the indicator calculations in the `bar()` function
3. Add your trading logic to generate buy/sell signals
4. Use the expert's methods to place trades

For more information on the MetaExpert library and its capabilities, see the [main documentation](../docs/).
