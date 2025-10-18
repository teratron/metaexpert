# Checklist: CLI Formal Review

**Purpose**: This checklist is for a formal peer review of the CLI feature requirements before implementation begins. It validates the quality, clarity, and completeness of the requirements in the spec.
**Scope**: CLI UX, Error Handling, and Process Management.
**Created**: 2025-10-18

---

## Command-Line UX

- [X] CHK001 - Are the names and aliases for all commands and subcommands clear and unambiguous? [Clarity, Spec §FR-001 to FR-008]
- [X] CHK002 - Does the spec require that output for all commands is human-readable and provides sufficient context? [Clarity, Spec §FR-010]
- [X] CHK003 - Are the requirements for the `list` command's output format (e.g., table columns) explicitly defined? [Completeness, Spec §FR-004]
- [X] CHK004 - Does the spec ensure that auto-generated help messages from Typer will be reviewed for clarity and completeness? [Clarity, Spec §SC-004]
- [X] CHK005 - Is the requirement for providing user-friendly error messages that suggest corrections explicitly stated? [Clarity, Spec §SC-005]

## Error Handling

- [X] CHK006 - Does the spec define the required behavior for when a user tries to run an expert with missing or invalid API keys? [Coverage, Spec §Edge Cases]
- [X] CHK007 - Is the required error behavior for running a non-existent expert file specified? [Coverage, Spec §Edge Cases]
- [X] CHK008 - Are requirements defined for handling mutually exclusive options (e.g., `backtest` with `--trade-mode live`)? [Completeness, Spec §Edge Cases]
- [X] CHK009 - Does the spec explicitly require that all commands fail gracefully with clear, actionable error messages? [Clarity, Spec §FR-010]
- [X] CHK010 - Is the expected behavior defined for when the global config file (`~/.metaexpert/config.json`) is malformed or unreadable? [Gap]
- [X] CHK011 - Are requirements specified for how the `new` command should behave if it lacks permissions to create a new directory? [Gap]

## Process Management

- [X] CHK012 - Is the location for storing PID files explicitly defined and justified? [Clarity, Spec §FR-012]
- [X] CHK013 - Does the spec define the required behavior for handling stale PID files where the process no longer exists? [Completeness, Spec §Edge Cases]
- [X] CHK014 - Are the requirements for the `status` command's output (e.g., table columns including PID) clearly defined? [Clarity, Spec §User Story 3]
- [X] CHK015 - Does the spec clarify that `stop` should target a process via its PID file, not just a name? [Clarity, Spec §FR-007]
- [X] CHK016 - Is the requirement for `run` to operate as a *detached* background process explicitly stated? [Clarity, Spec §FR-002]
- [X] CHK017 - Does the spec account for potential race conditions, such as running `stop` on an expert that is still in the process of starting up? [Gap]