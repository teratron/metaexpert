# MetaExpert Project Context

## Project Overview

**MetaExpert** is a Python library for cryptocurrency trading that provides a unified interface for multiple exchanges and trading types. The system is designed to be modular, extensible, and easy to use while maintaining high performance and reliability. It currently supports major cryptocurrency exchanges including Binance, Bybit, OKX, Bitget, and KuCoin.

The project is built for Python 3.12+ and uses a unified interface for different trading types (spot, futures, options) and market modes (linear, inverse contracts). It supports paper trading, live trading, and backtesting modes.

The project follows a strict set of development principles outlined in the `constitution.md` file, which emphasizes a library-first architecture, mandatory Test-Driven Development (TDD), and adherence to SOLID, DRY, and KISS principles.

The project is in an early alpha stage. A key planned feature is a Command-Line Interface (CLI) for scaffolding new expert projects from a template, but this is not yet implemented.

## Architecture & Core Components

### Main Structure
- `src/metaexpert/` - Main source code directory
- `src/metaexpert/cli/` - Command-line interface module (currently with a placeholder)
- `src/metaexpert/template/template.py` - Reference template for creating new trading strategies
- `src/metaexpert/__main__.py` - Entry point that delegates to the CLI module
- `examples/` - Directory for example trading strategies
- `specs/` - Feature specifications (including CLI feature spec)

### Key Classes & Modules
- `MetaExpert` class: Core trading system class that handles exchange connections, configuration, and execution
- `MetaExchange`: Handles connections to various cryptocurrency exchanges
- `MetaLogger`: Provides logging functionality for trading operations
- `MetaProcess`: Manages the trading process and execution
- Event system with handlers for different trading events (ticks, bars, orders, positions, etc.)

### Configuration Parameters
The system supports extensive configuration for:
- Exchange connections (API keys, testnet, proxies)
- Trading parameters (leverage, position size, stop losses, take profits)
- Risk management (drawdown limits, daily loss limits)
- Logging and metrics
- Backtesting parameters

## CLI Implementation Status

The CLI functionality is currently under development. The `__main__.py` file shows that it's designed to delegate to `metaexpert.cli.main()`, but the CLI implementation appears to be incomplete. The project has a feature specification in `specs/cli-new-command/spec.md` that defines the requirements for the `new` command to generate expert templates.

## Building and Running

### Installation
```bash
pip install metaexpert
```
Or with poetry:
```bash
poetry add metaexpert
```

### Development Setup
The project uses `uv` for dependency and environment management.

**1. Setup:**
To set up the development environment and install all dependencies (including dev, test, and linting tools), run:
```shell
# First, ensure you have a virtual environment
python -m venv .venv
# Activate it (Windows)
.venv\Scripts\activate
# Install dependencies
uv sync
```

### CLI Commands
The system is designed to support these CLI commands (pending implementation):
- `metaexpert new <expert_name>` - Creates a new trading expert from the template
- `metaexpert --help` or `metaexpert -h` - Shows help information
- `metaexpert help <command>` - Shows help for specific commands

### Example Usage
The template file (`src/metaexpert/template/template.py`) serves as an example of how to create a trading strategy:
1. Create an instance of MetaExpert with exchange configuration
2. Decorate the init function with `@expert.on_init` to set strategy parameters
3. Implement event handlers (`@expert.on_bar`, `@expert.on_tick`, etc.) for trading logic
4. Use `expert.run()` to start the trading system

## Development Conventions

### Code Style
- Python 3.12+ with type hints
- Ruff for linting and formatting
- Pyright for type checking
- Black for code formatting

### Project Structure
- Modular design with separate directories for different functionality (core, exchanges, logger, utils, websocket)
- Event-driven architecture for handling different trading events
- Template-based approach for creating new trading strategies

### Dependencies
- Core: `websocket-client>=1.9.0`
- Dev: `python-dotenv`, `pyleak`, `pyright`, `specify-cli`
- Test: `pytest`, `pytest-asyncio`, `pytest-cov`
- Lint: `ruff`

### Constitution:
All development MUST adhere to the principles outlined in `.specify/memory/constitution.md`. This is the most important document for guiding contributions. Key rules include:
*   **TDD is non-negotiable.**
*   Code and all technical assets (comments, docs, commits) **MUST be in English**.
*   Conversational chat with the agent **SHOULD be in Russian**.
*   Adherence to SOLID, DRY, KISS, YAGNI, and FSD principles.
*   Strict versioning and documentation update requirements.

### Feature Development:
The project uses the `specify-cli` tool for a specification-driven development process. New features are defined in `spec.md` files within the `specs/` directory.

### Code Style:
*   **Formatting:** Handled by `ruff format` (double quotes, LF line endings).
*   **Linting:** A specific set of `ruff` rules is enforced (see `pyproject.toml`).
*   **Typing:** Code must have comprehensive type annotations, validated by `pyright`.

### Versioning:
The project follows Semantic Versioning (SemVer). Version numbers must be updated in `pyproject.toml`, `src/metaexpert/__version__.py`, and documentation for each significant change.

### Template File:
The file `src/metaexpert/template/template.py` is the immutable, authoritative source template for new experts. It must not be modified without explicit approval and should be used as a reference for new features.

## Testing
The project includes a `tests/` directory and uses pytest for testing. The pyproject.toml file defines test dependencies but doesn't show specific test configurations yet.

Running Tests:
The project uses `pytest` for testing. TDD is a mandatory practice.
```shell
# Run all tests
pytest
# Run tests with coverage report
pytest --cov=src/metaexpert
```

Linting and Formatting:
`ruff` is used for both linting and formatting. `pyright` is used for static type checking.
```shell
# Format code
ruff format .
# Run linter
ruff check .
# Run static type checker
pyright
```

## Current Development Focus
Based on the feature specification in `specs/cli-new-command/spec.md`, the current focus appears to be on implementing a CLI that allows users to create new expert templates using the `metaexpert new` command. This would generate a new Python file based on the template in `src/metaexpert/template/template.py` with appropriate naming conventions and structure.

## Key Files
- `pyproject.toml` - Project configuration, dependencies, and build settings
- `src/metaexpert/__init__.py` - Main MetaExpert class definition
- `src/metaexpert/__main__.py` - Entry point for the application
- `src/metaexpert/template/template.py` - Reference template for new trading strategies
- `specs/cli-new-command/spec.md` - Feature specification for CLI implementation

## Project Status
The project is in the initial stage (alpha) and is actively being developed with focus on establishing core trading functionality and CLI tools for creating new trading strategies.