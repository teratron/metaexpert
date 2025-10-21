# Test-Driven Development Workflow

## Brief overview

This document outlines the test-driven development (TDD) workflow for this Python project. Adherence to these rules is mandatory to ensure code quality, maintainability, and robustness. Every change must be validated through this process.

## Core Principles

- **Test-First Approach**: All code modifications (bug fixes, new features, refactoring) must be covered by `pytest` unit tests. If tests are missing for the modified code, the first step is to write them.
- **Isolate and Conquer**: When tests reveal failures in unrelated modules, create a new, dedicated task to debug and fix the separate problem. Do not proceed with the original task until the blocking issue is resolved.
- **Mandatory Validation**: A task is not complete until all quality checks pass. Never assume a change works without verification.
- **Role-Based Delegation**: Leverage specialized modes for specific sub-tasks. For instance, delegate comprehensive test creation to a `test-engineer` persona and complex debugging to a `debug` persona.

## Development & CI Workflow

The project uses a modern Python stack managed by `pyproject.toml`. Adhere strictly to the following commands for all operations:

- **Environment Activation**: Before running any quality checks, activate the virtual environment: `.venv/Scripts/activate` or `source .venv/bin/activate`
- **Dependency Management**: Use `uv` for all package installation and management (e.g., `uv add <package>`, `uv remove <package>`, `uv sync`, `uv lock`, `uv check`, `uv clean`, `uv build`, `uv run`, `uv format`, `uv version`, `uv help`).
- **Code Quality & Verification (Run before every completion)**:
    1. Format Code: `uv run ruff format .`
    2. Lint and Autofix: `uv run ruff check . --fix`
    3. Static Type Check: `uv run pyright`
    4. Run Automated Tests: `uv run pytest`
- **Package Building**: When ready for distribution, build the package using `uv build`.
