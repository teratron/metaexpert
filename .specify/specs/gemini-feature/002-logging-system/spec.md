# Feature Specification: Comprehensive Logging System

**Feature Branch**: `gemini-feature/002-logging-system`  
**Created**: 2025-10-17  
**Status**: Draft  
**Input**: User description: "logging: Create a comprehensive logging system specification based on the exact description in @/.rules/spec-logging.md, incorporating additional context from @/src/metaexpert/cli/templates/template.py, @/src/metaexpert/__init__.py, and @/src/metaexpert/config.py to ensure full alignment with the existing architecture and configuration patterns."

## Clarifications

### Session 2025-10-17
- Q: Should the logging system send real-time alerts for critical errors? → A: Yes, include a handler for real-time alerts. The system should send notifications for `CRITICAL` level events to a configurable webhook or messenger (e.g., Telegram).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Debugging (Priority: P1)

As a developer, I need to view detailed, structured (JSON) logs so that I can efficiently trace application behavior, diagnose bugs, and understand the context of events without parsing unstructured text.

**Why this priority**: This is the primary mechanism for development and troubleshooting. Without clear, machine-readable logs, diagnosing issues becomes extremely time-consuming and inefficient.

**Independent Test**: Can be fully tested by running an expert in `DEBUG` mode, performing a single action (like attempting a trade), and verifying that a structured JSON log entry with the correct context (e.g., `order_id`, `symbol`) is written to the specified log file.

**Acceptance Scenarios**:

1. **Given** the expert is configured for structured logging (`structured_logging=True`) and `log_level="DEBUG"`,
   **When** an API call is made,
   **Then** a JSON log entry is created in `expert.log` containing the request and response details.
2. **Given** an error occurs within a strategy,
   **When** an exception is caught,
   **Then** a JSON log entry is created in `errors.log` containing the error message, level "ERROR", and a full stack trace.

---

### User Story 2 - Operator Monitoring (Priority: P1)

As an operator running a live trading bot, I need logs to be separated into distinct files for general events (`expert.log`), trade operations (`trades.log`), and critical errors (`errors.log`) so that I can quickly assess application health and isolate important events without noise.

**Why this priority**: Separating logs is crucial for effective monitoring in a production environment. It allows for targeted alerting and quick identification of critical issues (errors) or auditing of financial operations (trades).

**Independent Test**: Can be tested by running an expert that executes one successful trade and one failed trade. This single run delivers value by demonstrating the log separation.

**Acceptance Scenarios**:

1. **Given** an expert is running,
   **When** it successfully opens a position,
   **Then** the trade details are recorded *only* in `trades.log` as a JSON object.
2. **Given** an expert is running,
   **When** a non-trade-related warning occurs (e.g., high slippage detected),
   **Then** the event is recorded in `expert.log` but *not* in `trades.log` or `errors.log`.
3. **Given** an expert is running,
   **When** an order fails due to "Insufficient funds",
   **Then** the error event is recorded in `errors.log` with full context.

---

### User Story 3 - Operator Real-Time Alerting (Priority: P1)

As an operator of a live trading bot, I need to receive immediate notifications via a service like Telegram or a webhook when a critical, application-terminating error occurs, so that I can take immediate action to prevent further losses or system downtime.

**Why this priority**: For a live trading system, automated real-time alerts for critical failures are essential for risk management and operational stability. Relying solely on file-based logs for such events is too slow.

**Independent Test**: Can be tested by configuring an alert handler (e.g., a mock webhook endpoint) and running an expert that intentionally triggers a `CRITICAL` error (e.g., by using invalid API keys). The test passes if the mock endpoint receives a correctly formatted notification.

**Acceptance Scenarios**:

1. **Given** an alert handler is configured with a valid webhook URL,
   **When** the expert logs an event with level `CRITICAL`,
   **Then** a POST request containing the structured log data is sent to the configured URL.
2. **Given** an alert handler is configured,
   **When** the expert logs an event with level `ERROR`,
   **Then** no notification is sent to the webhook URL.

---

### User Story 4 - Flexible Configuration (Priority: P2)

As a user, I need to easily configure the logging behavior (level, format, and outputs) through the `MetaExpert` constructor or CLI arguments, so that I can adapt the logging verbosity and format for different environments (development, production, backtesting) without modifying library code.

**Why this priority**: Configuration flexibility is a core requirement for a reusable library. Users must be able to control logging externally to suit their specific operational needs.

**Independent Test**: Can be tested by initializing two `MetaExpert` instances with different logging parameters and verifying that their log outputs are formatted and filtered correctly according to their individual configurations.

**Acceptance Scenarios**:

1. **Given** an expert is initialized with `log_to_console=False`,
   **When** the expert runs and logs an event,
   **Then** no output appears on the console, but the event is written to the log file.
2. **Given** an expert is initialized with `log_level="WARNING"`,
   **When** the expert's code calls `logger.info("Test message")`,
   **Then** the message is *not* written to any log file or console.

---

### Edge Cases

- **What happens when a log file cannot be written to?** (e.g., disk full, permissions error) The system MUST attempt to write an error to a fallback stream (stderr) and, if possible, continue operation without crashing. The logger error itself should be logged to `logging_errors.log`.
- **How does the system handle extremely high log volume?** (e.g., DEBUG logging in a tight loop) The asynchronous logging feature (`async_logging=True`) MUST prevent the application's main thread from being blocked by I/O, ensuring trading logic is not delayed. A buffer queue will handle backpressure.
- **What happens if the logging configuration is invalid?** (e.g., `log_level="INVALID_LEVEL"`) The system MUST fail gracefully on startup with a clear error message indicating the invalid configuration parameter.
- **What happens if the alert webhook is unavailable?** The system MUST log the failure to send the alert to `errors.log` but MUST NOT crash or halt execution.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support structured logging, outputting logs in JSON format when configured.
- **FR-002**: The system MUST allow configuration of log levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- **FR-003**: The system MUST direct logs to three separate, configurable files: a general log (`expert.log`), a trade-specific log (`trades.log`), and an error log (`errors.log`).
- **FR-004**: The system MUST support human-readable, color-coded console logging for development.
- **FR-005**: The system MUST automatically rotate log files based on configurable size and backup count limits.
- **FR-006**: The system MUST provide an asynchronous logging option to minimize performance impact on the main application thread.
- **FR-007**: The system MUST adhere to a clear configuration priority: CLI arguments > `MetaExpert` constructor parameters > Environment variables > Default values.
- **FR-008**: The system MUST allow for adding contextual information to logs (e.g., `expert_name`, `symbol`) that is consistently applied to all subsequent entries from that logger instance.
- **FR-009**: The logging functionality MUST be implemented using the `structlog` library to ensure best practices for structured logging.
- **FR-010**: The system MUST provide a handler to send real-time notifications to a configurable webhook URL for log events of level `CRITICAL`.

### Key Entities *(include if feature involves data)*

- **`MetaLogger`**: A factory that configures and returns a ready-to-use logger instance based on user-provided settings. It serves as the main public interface for the logging system.
- **`LogRecord`**: A structured data object representing a single log event. It contains a timestamp, log level, the event message, and any bound contextual key-value pairs.
- **`Handler`**: A component responsible for dispatching `LogRecord` objects to a specific destination (e.g., a rotating file, the console, or an external service like a webhook).
- **`Processor`**: A function in a pipeline that enriches or formats a `LogRecord`, such as adding a timestamp, merging context, or rendering the final output format (JSON or text).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of log entries written to `trades.log` and `errors.log` MUST be valid, parseable JSON objects (JSON Lines format).
- **SC-002**: The logging system, when `async_logging` is enabled, MUST introduce no more than a 5% increase in median trade execution latency compared to when logging is disabled entirely.
- **SC-003**: A user MUST be able to change the log level from `INFO` to `DEBUG` via a configuration update (e.g., constructor parameter) and see the change reflected in the log output within 1 second without an application restart.
- **SC-004**: In a test run involving general info, warnings, trades, and errors, the `trades.log` file MUST contain *only* trade-related events, and the `errors.log` file MUST contain *only* events of level `ERROR` or `CRITICAL`.
- **SC-005**: When a `CRITICAL` event is logged, a notification MUST be delivered to the configured webhook endpoint within 5 seconds.
