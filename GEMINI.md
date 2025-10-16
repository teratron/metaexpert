# Gemini Context: MetaExpert Project

## Project Overview

**MetaExpert** is a Python library for creating cryptocurrency trading bots (experts). It provides a unified, event-driven interface for multiple exchanges (Binance, Bybit, OKX, etc.) and trading types (spot, futures). The framework is designed to be modular and extensible, supporting paper trading, live trading, and backtesting modes.

The project is built for Python 3.12+ and uses an event-driven architecture. Users define their trading strategies by implementing various event handlers (e.g., `on_tick`, `on_bar`, `on_order`).

## Core Components & Architecture

The project follows a "Feature-Sliced Design" and is structured as follows:

- `src/metaexpert/`: Main application package.
  - `core/`: Contains the core logic, including the main `Expert` class and data models for trades, markets, and timeframes.
  - `exchanges/`: Provides specific implementations for each supported cryptocurrency exchange.
  - `cli/`: Command-line interface for managing the application.
  - `template/`: Contains `template.py`, a crucial reference file used by the `metaexpert new` command to scaffold a new trading expert.
  - `utils/`: Helper functions for file management, packaging, and time.
  - `__main__.py`: The main entry point for the package.

## Building and Running

The project uses `uv` for dependency management.

- **Installation:**

  ```shell
  uv sync
  ```

- **Running the CLI:**
  The main entry point is exposed as a script via `pyproject.toml`.

  ```shell
  metaexpert [COMMAND]
  ```

  A key command is `metaexpert new`, which creates a new trading expert from `src/metaexpert/template/template.py`.

- **Running Tests:**
  The project uses `pytest` for testing.

  ```shell
  pytest
  ```

- **Linting:**
  The project uses `ruff` for linting and formatting.

  ```shell
  ruff check .
  ruff format .
  ```

## Development Conventions

- **Language:** All code, comments, and documentation are in **English**. Chat communication with the agent is in **Russian**.
- **Testing:** Test-Driven Development (TDD) is mandatory, using the `pytest` framework. A minimum of 85% test coverage is required.
- **Coding Principles:** The project strictly adheres to OOP, SOLID, DRY, KISS, and YAGNI principles.
- **Versioning:** The project follows Semantic Versioning (SemVer). Version numbers are maintained in `pyproject.toml`, `src/metaexpert/__version__.py`, and `README.md`.
- **`template.py` Immutability:** The `src/metaexpert/template/template.py` file is the authoritative source template. It must be copied as-is when running `metaexpert new` and must not be modified without explicit approval. Any new features or changes must be validated against this template to ensure compatibility.

---
*This section is auto-updated by the planning workflow.*
**Last updated**: 2025-10-16

## Active Technologies

- Python 3.12+
- Typer (from feature `001-project-cli`)

## Recent Changes

- **`001-project-cli`**: Added `Typer` for the new command-line interface.
