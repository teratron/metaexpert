# Implementation Plan: Comprehensive Logging System

**Feature Branch**: `gemini/logging-system`  
**Specification**: [spec.md](./spec.md)

## Technical Context

- **Languages**: Python 3.12+
- **Frameworks/Libraries**: 
  - `structlog`: Core library for structured logging.
  - `httpx`: For asynchronous webhook notifications.
- **Datastores**: N/A (logging to file system).
- **APIs/Integrations**: External webhook endpoint (URL provided via configuration) for critical alerts.
- **Tooling/Build**: `uv` for dependency management, `ruff` for linting, `pytest` for testing.
- **Constraints**: Must support `asyncio` and have minimal performance overhead, as per the specification.

## Constitution Check

- **I. Modular Architecture**: **PASS**. The new logging module will be located in `src/metaexpert/logger`, maintaining architectural separation.
- **II. Event-Driven & Extensible**: **PASS**. The logger will be integrated into the event-driven `MetaExpert` class and will be extensible with custom handlers/processors in the future.
- **III. TDD**: **PASS**. The implementation plan includes dedicated tasks for unit and integration tests with a target coverage of >95% for the new module.
- **IV. Strict Code Quality & Typing**: **PASS**. All new code will be fully typed and compliant with `ruff` and `pyright`.
- **V. Comprehensive Documentation**: **PASS**. The plan includes tasks for creating user guides and examples.
- **VI. Foundational Template**: **PASS**. The integration will be exposed through the `MetaExpert` constructor in `template.py`, aligning with the principle of template-driven configuration.

**Gate Evaluation**: The plan introduces two new third-party dependencies: `structlog` and `httpx`. 
- **Justification**: These additions are necessary to meet core functional requirements (structured logging, asynchronous alerts) and are considered best-in-class for their respective tasks. The introduction is justified.

---

## Phase 0: Outline & Research

**Status**: Completed.

- **Summary**: The primary research task was to select an appropriate asynchronous HTTP client for webhook notifications. `httpx` was chosen over `aiohttp` and synchronous `requests` for its modern API, performance, and async-first design.
- **Artifacts**: [research.md](./research.md)

---

## Phase 1: Design & Contracts

**Status**: Completed.

- **Summary**: The conceptual data model, public API contract, and user quickstart guide have been designed and documented. The design establishes `MetaLogger` as the factory for creating configured logger instances and defines the public-facing API for logging and context binding.
- **Artifacts**:
  - [data-model.md](./data-model.md)
  - [contracts/public_api.md](./contracts/public_api.md)
  - [quickstart.md](./quickstart.md)

---

## Phase 2: Task Decomposition (for `/speckit.implement`)

**High-Level Goal**: Implement the `metaexpert.logger` module as defined in the specification.

### Task Breakdown

1.  **Setup & Configuration**:
    - Create the module structure: `src/metaexpert/logger/`.
    - Define `LoggerConfig` Pydantic models in `logger/config.py`.
    - Add new dependencies (`structlog`, `httpx`) to `pyproject.toml`.

2.  **Core `structlog` Implementation**:
    - Implement the processor chain in `logger/processors.py` (timestamps, log levels, context merging).
    - Create formatters in `logger/formatters.py` for both JSON and console rendering.

3.  **Handler Implementation**:
    - Implement rotating file handlers for `expert.log`, `trades.log`, and `errors.log` in `logger/handlers/file.py`.
    - Implement the `WebhookHandler` for critical alerts using `httpx` in `logger/handlers/webhook.py`.
    - Implement filtering logic to route logs to the correct handlers based on level or context.

4.  **Factory & Integration**:
    - Implement the `MetaLogger` factory in `logger/__init__.py` to assemble the logger from config, processors, and handlers.
    - Integrate `MetaLogger` into the `MetaExpert` class `__init__` method, passing configuration parameters.
    - Update the `template.py` to include the new logging configuration parameters in the `MetaExpert` constructor.

5.  **Testing**:
    - Write unit tests for processors, handlers, and the `MetaLogger` factory.
    - Write integration tests to verify log file separation, formatting, and webhook alerting.
    - Ensure test coverage meets the >95% requirement.

6.  **Documentation**:
    - Create the user guide at `docs/guides/logging.md`.
    - Update the main `README.md` with a brief mention of the new logging capabilities.
