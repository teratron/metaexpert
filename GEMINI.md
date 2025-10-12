# MetaExpert Project Context

## Project Overview

**MetaExpert** is a Python library for creating cryptocurrency trading bots, referred to as "experts". It provides a unified interface for multiple exchanges and is designed to be modular and extensible. It currently supports major cryptocurrency exchanges including Binance, Bybit, OKX, Bitget, and KuCoin.

The project follows a strict set of development principles outlined in the `constitution.md` file, which emphasizes a library-first architecture, mandatory Test-Driven Development (TDD), and adherence to SOLID, DRY, and KISS principles.

The project is in an early alpha stage. A key planned feature is a Command-Line Interface (CLI) for scaffolding new expert projects from a template, but this is not yet implemented.

## Building and Running

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

**2. Running Tests:**
The project uses `pytest` for testing. TDD is a mandatory practice.
```shell
# Run all tests
pytest
# Run tests with coverage report
pytest --cov=src/metaexpert
```

**3. Linting and Formatting:**
`ruff` is used for both linting and formatting. `pyright` is used for static type checking.
```shell
# Format code
ruff format .
# Run linter
ruff check .
# Run static type checker
pyright
```

**4. Running the CLI (Once Implemented):**
The entry point for the CLI is defined, but the implementation is pending. Once complete, it will be run as:
```shell
python -m metaexpert <command>
```

## Development Conventions

**1. Constitution:**
All development MUST adhere to the principles outlined in `.specify/memory/constitution.md`. This is the most important document for guiding contributions. Key rules include:
*   **TDD is non-negotiable.**
*   Code and all technical assets (comments, docs, commits) **MUST be in English**.
*   Conversational chat with the agent **SHOULD be in Russian**.
*   Adherence to SOLID, DRY, KISS, YAGNI, and FSD principles.
*   Strict versioning and documentation update requirements.

**2. Feature Development:**
The project uses the `specify-cli` tool for a specification-driven development process. New features are defined in `spec.md` files within the `specs/` directory.

**3. Code Style:**
*   **Formatting:** Handled by `ruff format` (double quotes, LF line endings).
*   **Linting:** A specific set of `ruff` rules is enforced (see `pyproject.toml`).
*   **Typing:** Code must have comprehensive type annotations, validated by `pyright`.

**4. Versioning:**
The project follows Semantic Versioning (SemVer). Version numbers must be updated in `pyproject.toml`, `src/metaexpert/__version__.py`, and documentation for each significant change.

**5. Template File:**
The file `src/metaexpert/template/template.py` is the immutable, authoritative source template for new experts. It must not be modified without explicit approval and should be used as a reference for new features.
