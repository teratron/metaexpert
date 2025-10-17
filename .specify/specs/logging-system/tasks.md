# Tasks: Comprehensive Logging System

**Feature**: Comprehensive Logging System
**Branch**: `gemini-feature/logging-system`

## Phase 1: Setup

- [ ] T001 Create directory `src/metaexpert/logger/handlers`
- [ ] T002 Add `structlog` and `httpx` to `[tool.poetry.dependencies]` in `pyproject.toml`

## Phase 2: Foundational - Configuration (User Story 4)

**Goal**: Implement the core configuration logic, making the system configurable via the `MetaExpert` constructor.
**Independent Test**: Initialize `MetaExpert` with custom logging parameters and verify they are correctly applied.

- [ ] T003 [US4] Create `tests/test_logger_config.py` and write a unit test to validate the `LoggerConfig` Pydantic model.
- [ ] T004 [US4] Implement the `LoggerConfig` Pydantic model in `src/metaexpert/logger/config.py`.
- [ ] T005 [US4] Create `tests/test_logger_factory.py` and write a unit test for the `MetaLogger` factory's initialization.
- [ ] T006 [US4] Implement the initial `MetaLogger` factory in `src/metaexpert/logger/__init__.py`.
- [ ] T007 [US4] Integrate the `MetaLogger` into the `MetaExpert` class `__init__` method in `src/metaexpert/__init__.py`.
- [ ] T007a [US4] Add integration test to `tests/test_logging_integration.py` to verify configuration priority (CLI > Constructor > Env > Defaults) as per FR-007.

## Phase 3: Core Logging - JSON & Console (User Story 1)

**Goal**: Implement basic structured JSON and human-readable console logging to a single file.
**Independent Test**: Run an expert and verify that a well-formed JSON log entry is written to `expert.log`.

- [ ] T008 [US1] Create `tests/test_logger_components.py` with unit tests for processors and formatters.
- [ ] T009 [US1] Implement the `structlog` processor chain (timestamps, levels, etc.) in `src/metaexpert/logger/processors.py`.
- [ ] T010 [US1] Implement formatters for JSON and console output in `src/metaexpert/logger/formatters.py`.
- [ ] T011 [US1] Implement a rotating file handler in `src/metaexpert/logger/handlers/file.py`, ensuring it supports asynchronous, non-blocking I/O as per FR-006.
- [ ] T012 [US1] Add an integration test to `tests/test_logging_integration.py` to verify a single JSON log is written to `expert.log`.

## Phase 4: Log Stream Separation (User Story 2)

**Goal**: Separate log streams for trades and errors into their own files.
**Independent Test**: Run an expert that produces info, trade, and error events, then verify that `trades.log` and `errors.log` contain only the correct events.

- [ ] T013 [US2] Implement log filtering logic based on log level and context (e.g., `category='trade'`) in `src/metaexpert/logger/processors.py`.
- [ ] T014 [US2] Update the `MetaLogger` factory to configure and attach handlers for `trades.log` and `errors.log`.
- [ ] T015 [US2] Add an integration test to `tests/test_logging_integration.py` to verify correct log routing to all three files.

## Phase 5: Real-Time Alerting (User Story 3)

**Goal**: Implement webhook alerting for critical errors.
**Independent Test**: Trigger a `CRITICAL` error and verify that a mock webhook server receives the correct payload.

- [ ] T016 [US3] Create `tests/test_logger_handlers.py` and write a unit test for the `WebhookHandler` using a mock `httpx` client.
- [ ] T017 [US3] Implement the `WebhookHandler` in `src/metaexpert/logger/handlers/webhook.py`.
- [ ] T018 [US3] Update the `MetaLogger` factory to conditionally add the `WebhookHandler` if a `webhook_url` is provided.
- [ ] T019 [US3] Add an integration test to `tests/test_logging_integration.py` that uses a mock server to confirm the webhook is called correctly.

## Phase 6: Polish & Documentation

- [ ] T020 [P] Create the user guide in `docs/guides/logging.md`.
- [ ] T021 [P] Update `README.md` to mention the new logging system.
- [ ] T022 [P] Update `src/metaexpert/cli/templates/template.py` to include all new logging configuration parameters and comments.
- [ ] T023 [P] Create a performance benchmark test to validate logging overhead is within the 5% threshold defined in SC-002.

---

## Implementation Strategy

The implementation will follow the phases outlined above, which are ordered by dependency. Each phase corresponding to a user story (US4, US1, US2, US3) delivers an independently testable increment of value. This aligns with an iterative MVP-first approach.

- **MVP**: Completing Phase 3 will deliver the minimum viable product: a working, configurable, structured logger.
- **Dependencies**: Phase 3 depends on Phase 2. Phase 4 depends on Phase 3. Phase 5 is parallel to Phase 4 but depends on Phase 3.

### Parallel Execution Opportunities

- Within each phase, test creation can often be parallelized with implementation (`[P]` marker).
- The documentation tasks in Phase 6 are marked as parallel `[P]` and can be worked on at any point after Phase 2 is complete.