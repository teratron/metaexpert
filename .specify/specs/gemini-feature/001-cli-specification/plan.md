# Implementation Plan: Command-Line Interface (CLI)

**Feature Branch**: `gemini-feature/001-cli-specification`  
**Feature Spec**: [spec.md](./spec.md)  
**Research**: [research.md](./research.md)  
**Data Model**: [data-model.md](./data-model.md)  
**Public API**: [contracts/](./contracts/)  
**Quickstart**: [quickstart.md](./quickstart.md)  

## 1. Technical Context & Dependencies

| Category | Decision | Justification |
|---|---|---|
| **Primary Language** | Python 3.12+ | Project standard. |
| **CLI Framework** | Typer | Modern, easy-to-use, based on Python type hints, excellent for building robust CLIs with automatic help generation. |
| **Configuration** | `.env` files (project-specific), JSON file (global) | Per spec clarification: separates sensitive project config from non-sensitive global config. |
| **Process Mgmt** | Detached processes with PID files | Per spec clarification: simple, OS-level approach for managing running experts. |
| **Packaging** | `pyproject.toml` with `uv` | Project standard for dependency management and packaging. |
| **Testing** | `pytest` | Project standard for testing. |
| **Linting/Formatting** | `ruff` | Project standard for code quality. |

## 2. Constitution Check & Quality Gates

*This section is auto-filled and validated by the workflow.*

| Principle | Status | Justification |
|---|---|---|
| **I. Modular & Layered Architecture** | ✅ **PASS** | The CLI will be a new layer (`src/metaexpert/cli`) that orchestrates actions on the `core` and `expert` layers. It will not contain business logic. |
| **II. Event-Driven & Extensible Core** | ✅ **PASS** | The CLI will trigger the existing event-driven core but will not modify its architecture. |
| **III. Test-Driven Development (TDD)** | ✅ **PASS** | All CLI commands and logic will be developed with TDD, using `pytest` and `Typer`'s testing utilities. |
| **IV. Strict Code Quality & Typing** | ✅ **PASS** | `ruff` and `pyright` will be used to enforce standards on all new CLI code. |
| **V. Comprehensive Documentation** | ✅ **PASS** | `Typer` provides auto-generated `--help` for all commands. A new `quickstart.md` and `cli.md` guide will be added to `docs/guides/`. |
| **VI. Foundational Template** | ✅ **PASS** | The `new` command will directly use `src/metaexpert/cli/templates/template.py` as its source, ensuring all generated projects are compliant. |

## 3. Phase 0: Research & Prototyping

*No research tasks are required for this feature, as the clarifications have resolved all major ambiguities and the technology choices are standard for the project.*

## 4. Phase 1: Core Implementation & Design Artifacts

### 4.1. `data-model.md`

*This file will formalize the data structures identified in the feature spec.*

- **ExpertProject**: Defines the file structure and key metadata for a user-created trading bot.
- **GlobalConfig**: Defines the schema for the `~/.metaexpert/config.json` file.
- **PIDFile**: Defines the structure for the process ID file used to track running experts.

### 4.2. `contracts/`

*No public-facing API contracts (e.g., REST, GraphQL) are required for this feature, as it is a command-line interface.*

### 4.3. `quickstart.md`

*This guide will provide a step-by-step tutorial for new users.*

1.  **Installation**: How to install `metaexpert` from PyPI.
2.  **Create a Project**: Using `metaexpert new my-first-bot`.
3.  **Configure API Keys**: Editing the `.env` file.
4.  **Run the Bot**: Using `metaexpert run`.
5.  **Check Status**: Using `metaexpert status` and `metaexpert list`.
6.  **Stop the Bot**: Using `metaexpert stop`.

### 4.4. Agent Context Update

*The following technologies will be added to the agent's context to improve future interactions.*

- `Typer`

## 5. Phase 2: Task-Driven Implementation

*This phase will be managed via the `tasks.md` file, which will be generated from this plan.*

### Task Breakdown

1.  **Setup**:
    - `T-01`: Add `typer` and its dependencies to `pyproject.toml`.
    - `T-02`: Create the main CLI application object in `src/metaexpert/cli/main.py`.

2.  **`new` command**:
    - `T-03`: Implement the `new` command logic to copy the template from `src/metaexpert/cli/templates/template.py`.
    - `T-04`: Add support for `--exchange` and `--force` options.
    - `T-05`: Write unit tests for the `new` command, covering success and failure cases.

3.  **`config` command**:
    - `T-06`: Implement the `config` command group with `show`, `set`, `get`, `reset` subcommands.
    - `T-07`: Implement logic to read/write the global `~/.metaexpert/config.json` file.
    - `T-08`: Write unit tests for all `config` subcommands.

4.  **`run`, `status`, `stop`, `list` commands**:
    - `T-09`: Implement the `run` command to start an expert as a detached process and create a PID file.
    - `T-10`: Implement the `list` command to find expert projects and check PID files for status.
    - `T-12`: Implement the `stop` command to read a PID file and send a `SIGTERM` signal.
    - `T-13`: Write integration tests for the full `run -> list -> status -> stop` lifecycle.

5.  **`backtest` and `logs` commands**:
    - `T-14`: Implement the `backtest` command, passing arguments to the backtesting engine.
    - `T-15`: Implement the `logs` command to tail log files from a designated log directory.
    - `T-16`: Write unit tests for `backtest` and `logs` commands.

6.  **Documentation & Finalization**:
    - `T-17`: Create `docs/guides/cli.md` with detailed usage for all commands.
    - `T-18`: Review and update all docstrings and auto-generated help messages.
    - `T-19`: Run a final `uv sync`, `ruff check .`, and `pytest` to ensure all checks pass.
