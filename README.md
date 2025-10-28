# MetaExpert

[![PyPI version](https://badge.fury.io/py/metaexpert.svg)](https://badge.fury.io/py/metaexpert)
[![Documentation Status](https://readthedocs.org/projects/metaexpert/badge/?version=latest)](https://metaexpert.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Description

MetaExpert is a Python library for cryptocurrency trading that provides a unified interface for multiple exchanges and trading types. The system is designed to be modular, extensible, and easy to use while maintaining high performance and reliability. It currently supports major cryptocurrency exchanges including Binance, Bybit, OKX, Bitget, KuCoin, etc.

The project is built for Python 3.12+ and uses a unified interface for different trading types (spot, futures, options) and market modes (linear, inverse contracts). It supports paper trading, live trading, and backtesting modes.

The project follows a strict set of development principles outlined in the `.specify/memory/constitution.md` file, which emphasizes a library-first architecture, mandatory Test-Driven Development (TDD).

## Key Features

- **Multi-exchange Support**: Unified interface for major cryptocurrency exchanges
- **Structured Logging**: Advanced logging system with context management and security features
- **Backtesting**: Comprehensive backtesting capabilities for strategy validation
- **Modular Architecture**: Clean, extensible codebase following SOLID principles
- **Security Focused**: Automatic filtering of sensitive data in logs

## Visuals

## Installation

```shell
pip install metaexpert
```

```shell
poetry add metaexpert
```

```shell
uv add metaexpert
```

If you have already added **MetaExpert**, you can update to the latest version by using:

```shell
pip install --upgrade metaexpert
```

```shell
poetry update metaexpert
```

```shell
uv sync --upgrade-package metaexpert
```

## Usage

### Basic Usage

```python
from metaexpert.logger import setup_logging, get_logger, LoggerConfig

# Initialize logging system
config = LoggerConfig.for_production()
setup_logging(config)

# Get logger in your module
logger = get_logger(__name__)
logger.info("Application started")
```

### Advanced Logging Features

MetaExpert includes a sophisticated logging system with:

- **Structured Logging**: Add context to your log messages
- **Context Management**: Use LogContext for correlated events
- **Security Filtering**: Automatic masking of sensitive data
- **Performance Monitoring**: Track operation durations
- **Environment-Specific Presets**: Development, production, and backtesting configurations

For more details, see the [logging guide](docs/guides/logger.md).

## Documentation

Comprehensive documentation is available:

- [API Reference](docs/api/README.md)
- [Logging Guide](docs/guides/logger.md) - Detailed guide on logging system
- [CLI Guide](docs/guides/cli.md) - Command-line interface usage
- [Troubleshooting](docs/guides/troubleshooting.md) - Solutions to common issues
- [Tutorials](docs/tutorials/README.md) - Step-by-step tutorials

## Examples

You can find examples in the [example's directory](examples):

- [Expert Binance EMA Strategy](examples/expert_binance_ema)
- [Expert Bybit RSI Strategy](examples/expert_bybit_rsi)
- [Expert OKX MACD Strategy](examples/expert_okx_macd)
- [Expert MEXC PaParabolic SAR Strategy](examples/expert_mexc_psar)

Each example demonstrates how to use MetaExpert with different exchanges and trading strategies, including proper logging configuration.

## Support

## Roadmap

## Contributing

## Authors and acknowledgment

## License

[MIT License](LICENSE).

## Project status

_Project at the initial stage._

See the latest [commits](https://github.com/teratron/metaexpert/commits/master).
