# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MetaExpert** is a Python library for cryptocurrency trading that provides a unified interface for multiple exchanges (Binance, Bybit, OKX, Bitget, KuCoin, etc.). The system supports spot, futures, and options trading with paper trading, live trading, and backtesting modes. Built for Python 3.12+ with a library-first architecture following SOLID principles.

## Common Development Commands

### Package Management

```bash
# Install dependencies (including dev, test, lint, docs)
uv sync

# Install specific dependency groups
uv sync --group dev
uv sync --group test
uv sync --group lint
uv sync --group docs

# Add new dependency
uv add <package>
uv add --group dev <package>
```

### Code Quality

```bash
# Run ruff linter
uv run ruff check .

# Fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Type checking with pyright
uv run pyright
```

### Testing

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/logger/test_setup.py

# Run tests with coverage
uv run pytest --cov=metaexpert

# Run integration tests only
uv run pytest tests/integration/

# Run tests matching pattern
uv run pytest -k "test_setup"
```

### CLI Usage

```bash
# MetaExpert CLI (after installation)
metaexpert --help
metaexpert init
metaexpert new <project_name> --exchange <exchange> --strategy <strategy>
metaexpert run
metaexpert status
metaexpert stop
metaexpert logs
metaexpert backtest

# Generate documentation
uv run generate-docs
```

## High-Level Architecture

### Core Structure

```text
src/metaexpert/
├── __init__.py          # Main MetaExpert class entry point
├── config.py            # Global configuration constants
├── core/                # Core system components
├── exchanges/           # Exchange integrations (Binance, Bybit, OKX, etc.)
├── backtest/            # Backtesting framework
├── cli/                 # Typer-based CLI interface
│   ├── commands/        # CLI subcommands (new, run, stop, logs, etc.)
│   ├── core/            # CLI core (errors, events, dependencies)
│   └── process/         # Process management
├── logger/              # Structlog-based logging system
│   ├── config.py        # Pydantic-based LoggerConfig
│   ├── setup.py         # Logging configuration
│   ├── processors.py    # Structlog processors chain
│   ├── formatters.py    # Console/JSON formatters
│   └── context.py       # LogContext management
├── utils/               # Utility functions
└── websocket/           # WebSocket connection handling
```

### Key Components

**1. MetaExpert Class** (`src/metaexpert/__init__.py`)

- Main entry point for trading experts
- Manages exchange connections via `MetaExchange.create()`
- Supports three trade modes: 'paper', 'live', 'backtest'
- Event-driven architecture using decorator pattern (`@expert.on_init`, `@expert.on_bar`, etc.)

**2. Logger System** (`src/metaexpert/logger/`)

- Built on `structlog` for structured logging
- Pydantic-validated `LoggerConfig` class
- Context management with `LogContext`
- Automatic security filtering of sensitive data
- Supports JSON and human-readable formats
- Trade-specific logging capabilities

**3. CLI Interface** (`src/metaexpert/cli/`)

- Built with Typer framework
- Commands: init, new, run, stop, status, logs, backtest, config, etc.
- Process management for running experts
- Error handling and recovery system
- Template generation for new projects

**4. Exchange Framework** (`src/metaexpert/exchanges/`)

- Unified interface via `MetaExchange` class
- Individual exchange implementations (binance/, bybit/, okx/, etc.)
- Support for multiple market types (spot, futures, options)
- Contract types: linear (USDT-M), inverse (COIN-M)
- Margin modes: isolated, cross
- Position modes: hedge (two-way), oneway

**5. Examples** (`examples/`)

- Expert implementations for different exchanges and strategies
- Each example demonstrates specific exchange/strategy combination
- Includes: Binance EMA, Bybit RSI, OKX MACD, MEXC Parabolic SAR

### Trading Expert Pattern

Trading experts use an event-driven decorator pattern:

```python
from metaexpert import MetaExpert

expert = MetaExpert(exchange="binance", ...)

@expert.on_init
def init() -> None:
    """Initialize indicators, load data."""
    pass

@expert.on_bar
def bar(rates) -> None:
    """Handle completed bars - core strategy logic."""
    # EMA crossover logic, RSI signals, etc.

@expert.on_timer(60)
def timer() -> None:
    """Periodic tasks - monitoring, heartbeat."""
    pass

@expert.on_order
def order(order) -> None:
    """Handle order updates."""
    pass

@expert.on_position
def position(pos) -> None:
    """Handle position changes."""
    pass

expert.run(trade_mode="paper")  # or "live" or "backtest"
```

## Testing Strategy

The project follows **mandatory TDD** with comprehensive test coverage:

- **Unit Tests** (`tests/unit/`): Individual component testing
  - Logger system tests
  - CLI command tests
  - Configuration tests
  - Utility function tests

- **Integration Tests** (`tests/integration/`): Module interaction testing
  - CLI integration
  - End-to-end workflows

- **Contract Tests**: API verification (currently minimal)

All tests use `pytest` framework. Run `pytest --collect-only` to see all 431+ tests.

## Key Dependencies

- **structlog** >= 25.5.0: Structured logging
- **rich** >= 13.0.0: Console formatting
- **pydantic** >= 2.12.3: Data validation
- **typer** >= 0.20.0: CLI framework
- **websockets** >= 15.0.1: WebSocket connections
- **pytest** >= 8.3.4: Testing framework

## Configuration

Global settings in `src/metaexpert/config.py`:

- **Trading Modes**: DEFAULT_TRADE_MODE = "paper"
- **Market Types**: DEFAULT_MARKET_TYPE = "futures"
- **Contract Types**: DEFAULT_CONTRACT_TYPE = "inverse"
- **Logging**: LOG_LEVEL = "DEBUG", structured logging flags
- **Backtesting**: BACKTEST_START_DATE, BACKTEST_END_DATE

Logger configuration via `LoggerConfig` class (Pydantic model):

- Environment-specific presets (development, production, backtesting)
- File rotation settings
- JSON vs human-readable output
- Context management

## Development Principles

From AGENT.md, the project follows:

- **Library-First Architecture**: Each feature as standalone, testable library
- **CLI Interface**: All libraries expose CLI with stdin/args → stdout pattern
- **Test-First (TDD)**: Red-Green-Refactor cycle, 85% minimum coverage
- **Security Focus**: Protect API keys, encryption, OWASP compliance
- **OOP & SOLID**: Encapsulation, inheritance, polymorphism, abstraction
- **DRY, KISS, YAGNI**: Avoid duplication, keep simple, implement only what's needed
- **FSD**: Feature-Sliced Design methodology

## Language Conventions

- **Code/Docs**: English only (variables, functions, classes, comments, docstrings, commits)
- **Chat/Discussions**: Russian for conversational responses
- This ensures maintainability while allowing flexible communication

## Important Notes

1. **Exchange Credentials**: Stored in environment variables (`.env` files). See `.env.example` for reference
2. **Testnet Support**: All exchanges support testnet mode (set `testnet=True`)
3. **WebSocket URLs**: Retrieved via `client.get_websocket_url(symbol, timeframe)`
4. **Strategy Decorators**: Event handlers use decorators (`@expert.on_*`)
5. **Position Sizing**: Multiple modes - fixed_base, fixed_quote, percent_equity, risk_based
6. **Risk Management**: Built-in stop-loss, take-profit, trailing stops, drawdown limits
7. **Examples**: Working implementations in `examples/` directory, each with own `pyproject.toml`

## Documentation

- **API Reference**: `docs/api/README.md`
- **CLI Guide**: `docs/CLI_GUIDE.md`
- **Logger Guide**: `docs/guides/logger.md`
- **Command Reference**: `docs/COMMAND_REFERENCE.md`
- **Troubleshooting**: `docs/TROUBLESHOOTING.md`
- **Extending CLI**: `docs/EXTENDING_CLI.md`
