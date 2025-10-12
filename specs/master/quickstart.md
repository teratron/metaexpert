# Quickstart Guide for MetaExpert

## Prerequisites

- Python 3.12+
- uv package manager
- Access to cryptocurrency exchange API keys (Binance, Bybit, or OKX)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd metaexpert
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies using uv:
   ```bash
   uv pip install -e .
   ```

## Setting up Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your exchange API credentials:
   ```bash
   # Binance API credentials
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_api_secret
   
   # Bybit API credentials
   BYBIT_API_KEY=your_bybit_api_key
   BYBIT_API_SECRET=your_bybit_api_secret
   
   # OKX API credentials
   OKX_API_KEY=your_okx_api_key
   OKX_API_SECRET=your_okx_api_secret
   ```

## Creating Your First Trading Expert

1. Use the CLI to create a new expert:
   ```bash
   metaexpert create --name "MyEMAStrategy" --exchange binance --symbol BTCUSDT
   ```

2. Configure your strategy in the generated config file

3. Start your expert:
   ```bash
   metaexpert start --expert-id <expert-id>
   ```

## CLI Commands

- `metaexpert list`: List all experts
- `metaexpert create`: Create a new expert
- `metaexpert start <expert-id>`: Start an expert
- `metaexpert stop <expert-id>`: Stop an expert
- `metaexpert status <expert-id>`: Check expert status
- `metaexpert trades <expert-id>`: View trades for an expert
- `metaexpert backtest <expert-id>`: Run backtest for an expert

## Project Structure

After creating your first expert, you'll have a directory structure like:

```
your-expert/
├── main.py                 # Entry point for your expert
├── config.py               # Configuration for your expert
├── strategy.py             # Your trading strategy implementation
├── pyproject.toml          # Dependencies and settings
├── .env                   # Environment variables (not in repo)
├── .env.example           # Example .env file
└── README.md              # Documentation for your expert
```

## Running Tests

To ensure your expert is working correctly:

```bash
python -m pytest tests/
```

## Next Steps

1. Review the [Architecture Documentation](../docs/architecture.md)
2. Check out the [Usage Guide](../docs/usage.md)
3. Look at example experts in the `examples/` directory
4. Consult the [API Documentation](../docs/api/)
5. Follow the [Best Practices Guide](../docs/guides/best-practices.md)

## Troubleshooting

- Ensure your API keys have the correct permissions
- Check that your firewall allows outbound connections
- Verify your system time is synchronized (important for API authentication)
- Enable logging to debug issues: `metaexpert --verbose`