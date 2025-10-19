# Inheriting Base Rules

This agent fully inherits and adheres to all universal principles and rules defined in 'AGENT.md'. The following instructions are additions, clarifications, or overrides specific to the Gemini model.

## Gemini-Specific Instructions

## Overview and Architecture

**MetaExpert** is a Python library that uses an **event-driven architecture**. Users define their trading strategies by implementing various event handlers (e.g., `on_tick`, `on_bar`, `on_order`).

## Building and Running

The project uses `uv` for dependency management.

- **Installation:**

  ```shell
  uv sync
  ```

- **Running the CLI:**
  The main entry point (`metaexpert`) is configured via `pyproject.toml`.

  ```shell
  metaexpert [COMMAND]
  ```

  A key command is `metaexpert new`, which creates a new trading expert from a template.

- **Testing:**
  The project uses `pytest`.

  ```shell
  pytest
  ```

- **Linting and Formatting:**
  The project uses `ruff`.

  ```shell
  ruff check .
  ruff format .
  ```

---
*This section is auto-updated by the planning workflow.*
**Last updated**: 2025-10-18

## Active Technologies
- Python 3.12+
- Typer (from feature `gemini-feature/001-cli-specification`)

## Recent Changes

- **`001-project-cli`**: Added `Typer` for the new command-line interface.
