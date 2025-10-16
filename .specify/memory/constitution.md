# MetaExpert Constitution
<!-- Constitution for the MetaExpert project, defining core development principles and governance. -->

## Core Principles

### I. Modular & Layered Architecture
The project is divided into distinct layers (`core`, `exchanges`, `utils`, `cli`). Each layer has a specific responsibility, promoting separation of concerns and maintainability. Business logic is isolated from external integrations and infrastructure code.

### II. Event-Driven & Extensible Core
The system is built on an event-driven model. Core logic is triggered by market events (`tick`, `bar`). Users extend the system by implementing event handlers using decorators (`@expert.on_tick`, `@expert.on_bar`), following the Inversion of Control (IoC) principle.

### III. Test-Driven Development (TDD) - NON-NEGOTIABLE
Test-Driven Development is mandatory. All new features or bug fixes must be accompanied by tests. The Red-Green-Refactor cycle is strictly enforced. A minimum of 85% test coverage is required for all new code.

### IV. Strict Code Quality & Typing
All code must adhere to strict quality standards enforced by `Ruff` (linting, formatting) and `Pyright` (static typing). The entire codebase must be fully typed and pass all linter checks before being merged.

### V. Comprehensive Documentation
Every feature, module, and public function must be clearly documented. This includes in-code docstrings for developers and user-facing guides and examples in the `docs/` and `examples/` directories. The `template.py` file serves as a key piece of documentation for new users.

## Development Workflow

The project follows a standard Git workflow. All changes must be introduced through Pull Requests. All CI checks (linting, testing, type checking) must pass before a branch can be merged into `main`.

## Versioning

The project adheres to Semantic Versioning (SemVer). Version numbers must be consistently updated in `pyproject.toml`, `src/metaexpert/__version__.py`, and `README.md` for every release.

## Governance
This constitution is the single source of truth for development practices. All code reviews must validate compliance with these principles. Any deviation must be explicitly justified and approved by the project maintainers.

**Version**: 1.0.0 | **Ratified**: 2025-10-16 | **Last Amended**: 2025-10-16