# Tasks: Command-Line Interface (CLI)

**Feature**: [Command-Line Interface (CLI)](./spec.md)

This document breaks down the implementation of the CLI feature into actionable tasks, organized by development phase and user story.

## Phase 1: Setup

- [X] T001 Add `typer` and its dependencies to `pyproject.toml`.
- [X] T002 Create the main CLI application object in `src/metaexpert/cli/main.py`.

## Phase 2: Foundational Commands

- [X] T003 Implement the `config` command group with `show`, `set`, `get`, `reset` subcommands in `src/metaexpert/cli/config_cmd.py`.
- [X] T004 [P] Implement logic to read/write the global `~/.metaexpert/config.json` file in a new `src/metaexpert/cli/config_manager.py`.
- [X] T005 Write unit tests for all `config` subcommands in `tests/cli/test_config_cmd.py`.

## Phase 3: User Story 1 - Create a New Expert Project (P1)

- **Goal**: Quickly start a new trading bot project from a template.
- **Independent Test**: `metaexpert new my-first-bot` creates a complete, runnable project.

- [ ] T006 [US1] Implement the `new` command logic in `src/metaexpert/cli/new_cmd.py` to copy the template from `src/metaexpert/cli/templates/template.py`.
- [ ] T007 [P] [US1] Add support for `--exchange` and `--force` options to the `new` command.
- [ ] T008 [US1] Write unit tests for the `new` command, covering success and failure cases, in `tests/cli/test_new_cmd.py`.

## Phase 4: User Story 2 - Run and Backtest an Expert (P1)

- **Goal**: Run an expert in different modes (paper, live, backtest) via the command line.
- **Independent Test**: `metaexpert run` starts the bot; `metaexpert backtest` runs a backtest and prints a summary.

- [ ] T009 [US2] Implement the `run` command in `src/metaexpert/cli/run_cmd.py` to start an expert as a detached process and create a PID file.
- [ ] T010 [P] [US2] Implement the `backtest` command in `src/metaexpert/cli/backtest_cmd.py`, passing arguments to the backtesting engine.
- [ ] T011 [US2] Write unit tests for the `run` and `backtest` commands in `tests/cli/test_run_cmd.py` and `tests/cli/test_backtest_cmd.py`.

## Phase 5: User Story 3 & 4 - Manage and Monitor Experts (P2)

- **Goal**: Monitor, list, and stop running trading bots.
- **Independent Test**: `metaexpert list` shows statuses; `metaexpert status` shows details; `metaexpert stop` terminates the process.

- [ ] T012 [US3] Implement the `list` command in `src/metaexpert/cli/list_cmd.py` to find expert projects and check PID files for status.
- [ ] T013 [P] [US3] Implement the `stop` command in `src/metaexpert/cli/stop_cmd.py` to read a PID file and send a `SIGTERM` signal.
- [ ] T014 [P] [US3] Implement the `logs` command in `src/metaexpert/cli/logs_cmd.py` to tail log files from the `~/.metaexpert/logs/` directory.
- [ ] T015 [US3] Write integration tests for the full `run -> list -> stop` lifecycle in `tests/cli/test_lifecycle.py`.

## Phase 6: Polish & Documentation

- [ ] T016 Create `docs/guides/cli.md` with detailed usage for all commands.
- [ ] T017 Review and update all docstrings and auto-generated help messages for clarity.
- [ ] T018 Run a final `uv sync`, `ruff check .`, and `pytest` to ensure all checks pass.
- [ ] T019 Verify the output of `metaexpert --version` and `metaexpert --help` for accuracy and clarity.

## Dependencies

- **User Story 1** is a prerequisite for all other user stories.
- **User Story 2** is a prerequisite for User Story 3 & 4.

## Parallel Execution

- Tasks marked with `[P]` can potentially be worked on in parallel within their respective phases.
- The implementation of `config` (T003-T005) can be done in parallel with User Story 1 (T006-T008).

## Implementation Strategy

- **MVP**: The Minimum Viable Product consists of completing User Story 1 (`new` command) and the `run` command from User Story 2. This provides the core workflow of creating and running a bot.
- **Incremental Delivery**: Subsequent user stories can be delivered incrementally.
