# Feature Specification: Command-Line Interface (CLI)

**Feature Branch**: `gemini-feature/001-cli-specification`  
**Created**: 2025-10-18  
**Status**: Draft  
**Input**: User description: "command-line interface: Create a comprehensive command-line interface specification based on the exact description in @/.rules/spec-cli.md, incorporating additional context from @/src/metaexpert/cli/templates/template.py, @/src/metaexpert/__init__.py, and @/src/metaexpert/config.py to ensure full alignment with the existing architecture and configuration patterns."

## Clarifications

### Session 2025-10-18
- Q: How should the CLI store sensitive configuration data like API keys for live trading? → A: Do not store them centrally; require them to be in per-project .env files.
- Q: How should we resolve the conflict with FR-005 (global config command)? → A: Keep the global `config` command, but only for non-sensitive data (e.g., default author name, preferred exchange). Sensitive data like API keys must remain in project .env files.
- Q: How should the CLI manage the lifecycle of running expert processes? → A: The `run` command starts the expert as a completely independent, detached background process. The CLI then has no direct control. `status` and `stop` would rely on OS-level process inspection (e.g., finding processes by name or PID file).
- Q: What specific actions should a "graceful stop" entail when the `metaexpert stop` command is used? → A: The `stop` command sends a standard termination signal (SIGTERM) to the expert process. The expert is expected to catch this signal and perform its own cleanup (e.g., save state, close trades) before exiting.
- Q: What information should the `metaexpert list` command display to the user? → A: Display the name of each expert project and its current running status (e.g., "running", "stopped") by checking for a corresponding PID file.
- Q: Where should the global, non-sensitive configuration managed by the `config` command be stored? → A: A simple JSON file in the user's home directory (e.g., `~/.metaexpert/config.json`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a New Expert Project (Priority: P1)

As a new user, I want to quickly start a new trading bot project so that I can immediately begin developing my strategy. I should be able to run a single command that generates a complete, runnable project structure with sensible defaults based on the standard template.

**Why this priority**: This is the primary entry point for any user of the library. A smooth onboarding experience is critical for adoption.

**Independent Test**: Can be fully tested by running `metaexpert new my-first-bot`. The command should create a new directory `my-first-bot/` containing `main.py`, `pyproject.toml`, `.env.example`, and `README.md`. The generated project should be runnable out-of-the-box in paper mode.

**Acceptance Scenarios**:

1. **Given** a user is in a clean directory, **When** they run `metaexpert new my-bot`, **Then** a new directory named `my-bot` is created with all required template files (`main.py`, `.env.example`, `pyproject.toml`, `README.md`, `.gitignore`).
2. **Given** a directory named `my-bot` already exists, **When** a user runs `metaexpert new my-bot` without the `--force` flag, **Then** the system shows an error message and does not overwrite the directory.
3. **Given** a user wants to specify a different exchange, **When** they run `metaexpert new my-bybit-bot --exchange bybit`, **Then** the generated `main.py` file has the `exchange` parameter set to `"bybit"`.

---

### User Story 2 - Run and Backtest an Expert (Priority: P1)

As a developer, I want to run my trading expert in different operational modes (paper, live, backtest) using a simple command. I need to be able to override key parameters like the trading symbol or timeframe directly from the command line for quick experiments.

**Why this priority**: This is the core execution functionality. Users need a reliable way to run and test their strategies.

**Independent Test**: Can be tested by using the `metaexpert run` and `metaexpert backtest` commands on a generated project. `metaexpert run` should start the bot in paper trading mode. `metaexpert backtest main.py --start-date 2024-01-01` should execute a backtest and print a results summary.

**Acceptance Scenarios**:

1. **Given** a valid expert project exists, **When** a user runs `metaexpert run`, **Then** the expert starts in the default paper trading mode as a background process and logs its initialization.
2. **Given** a valid expert project, **When** a user runs `metaexpert run --trade-mode live`, **Then** the expert starts in live trading mode as a background process, attempting to connect with the configured API credentials.
3. **Given** a valid expert project, **When** a user runs `metaexpert backtest main.py --start-date 2024-01-01 --end-date 2024-02-01`, **Then** the system runs a backtest for the specified period and outputs a performance report.

---

### User Story 3 - Manage and Monitor a Running Expert (Priority: P2)

As an operator, I need to monitor my running trading bots, view their logs to diagnose issues, and stop them gracefully when needed.

**Why this priority**: Operational management is crucial for any long-running application to ensure stability and control.

**Independent Test**: Can be tested once an expert is running. `metaexpert list` should show the running expert's status. `metaexpert logs` should display its log output. `metaexpert stop <expert_name>` should terminate the process.

**Acceptance Scenarios**:

1. **Given** an expert is running, **When** a user runs `metaexpert list`, **Then** a table is displayed showing the expert's name, status (e.g., "running"), PID, and other key metrics.
2. **Given** a running expert is producing logs, **When** a user runs `metaexpert logs`, **Then** the last 50 log lines are displayed.
3. **Given** a running expert named `my-bot`, **When** a user runs `metaexpert stop my-bot`, **Then** the expert process is terminated gracefully and `metaexpert status` no longer shows it as running.

---

### User Story 4 - Discover Available Experts (Priority: P2)

As a developer with multiple projects, I want to quickly see all the expert projects in my workspace and know which ones are currently active.

**Why this priority**: Provides a quick overview of the user's workspace, improving manageability.

**Independent Test**: Can be tested in a directory containing multiple expert projects, some running and some not. `metaexpert list` should correctly identify all projects and their statuses.

**Acceptance Scenarios**:

1. **Given** a directory contains three expert projects (`bot-a`, `bot-b`, `bot-c`), and `bot-a` is running, **When** a user runs `metaexpert list`, **Then** a table is displayed showing `bot-a` with status "running" and `bot-b` and `bot-c` with status "stopped".

---

### Edge Cases

- **Invalid Configuration**: What happens when a user tries to run an expert with an invalid `.env` file or missing API keys in live mode? The system should fail gracefully with a clear error message.
- **Non-existent Expert File**: How does the system handle `metaexpert run non_existent_file.py`? It should report that the file was not found.
- **Conflicting Options**: How does the system handle mutually exclusive options, such as running a backtest with `--trade-mode live`? The CLI should raise a parameter validation error.
- **Stale PID File**: How does the system handle a PID file for a process that no longer exists? `status` should report it as "stopped" or "stale", and `stop` should report that the process is not running.
- **Malformed Global Config**: How should commands behave if the global `~/.metaexpert/config.json` is corrupted? They should fail gracefully with a clear error message about the corruption.
- **Permission Errors**: What happens if the `new` command is run in a directory where the user lacks write permissions? It should fail with a clear OS-level permission error.
- **Stop/Start Race Condition**: How is the system protected against a user running `stop` on an expert that is still starting, or `run` on an expert that is still stopping? Commands should use a locking mechanism on the PID file to prevent simultaneous operations on the same expert instance.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `new` command to create a new expert project from a template, as defined in `spec-cli.md`.
- **FR-002**: System MUST provide a `run` command to execute a trading expert as a detached background process.
- **FR-003**: System MUST provide a `backtest` command to run a strategy on historical data with configurable date ranges and capital.
- **FR-004**: System MUST provide a `list` command to discover and show available experts in a given directory, along with their detailed running status (by checking for a PID file).
- **FR-005**: System MUST provide a `config` command group (`show`, `set`, `get`, `reset`) to manage global, **non-sensitive** configuration (e.g., default author name, preferred exchange).
- **FR-007**: System MUST provide a `stop` command to gracefully terminate a running expert by sending a standard `SIGTERM` signal to the process ID found in its PID file.
- **FR-008**: System MUST provide a `logs` command to view and follow log output from the designated log directory, with filtering by level.
- **FR-009**: The CLI MUST support global options for `--version` and `--help`.
- **FR-010**: All commands MUST provide informative, human-readable output on success and clear, actionable error messages on failure.
- **FR-011**: The CLI application MUST be installable and runnable as a standalone command `metaexpert`.
- **FR-012**: The `run` command MUST generate a PID file (e.g., in a central directory like `~/.metaexpert/pids/`) to track the process ID of the running expert.
- **FR-013**: The system MUST store all expert log files in a central directory (e.g., `~/.metaexpert/logs/`).

### Security Requirements

- **SR-001**: The system MUST NOT store sensitive data, such as API keys, in any global configuration. All secrets MUST be managed via per-project `.env` files, which should be included in the project's `.gitignore` file by default.

### Key Entities *(include if feature involves data)*

- **Expert Project**: A directory containing the user's strategy code (`main.py`), project configuration (`pyproject.toml`), environment variables (`.env`), and documentation (`README.md`). It represents a single, self-contained trading bot.
- **Configuration**: A set of key-value pairs that. This is split into two types:
    - **Global Configuration**: Non-sensitive data (e.g., default author, preferred exchange) managed via the `config` command and stored in a JSON file in the user's home directory (e.g., `~/.metaexpert/config.json`).
    - **Project Configuration**: Sensitive data (e.g., API keys) and project-specific overrides stored in a `.env` file within the Expert Project directory.
- **Running Expert Instance**: A live, detached background process of an expert. It is identified by a unique name or ID and its process ID (PID) is stored in a dedicated PID file. It has a status (running, stopped, error), consumes resources, and produces logs. The expert process itself is responsible for catching the `SIGTERM` signal to perform cleanup (e.g., saving state, closing trades) before exiting.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can create and run a functional paper trading expert using `metaexpert new` and `metaexpert run` in under 60 seconds, without writing any code.
- **SC-002**: The `metaexpert backtest` command can process a 1-year history of 1-hour bars for a single symbol in under 30 seconds.
- **SC-003**: 100% of the commands and options defined in the `spec-cli.md` document are implemented and covered by automated tests.
- **SC-004**: The `--help` output for every command and subcommand is automatically generated by the framework, is clear, and accurately reflects all available arguments and options.
- **SC-005**: The CLI correctly handles at least 10 different types of invalid user input (e.g., wrong data types, non-existent files, invalid choices) across all commands, providing user-friendly error messages that suggest a correct alternative.