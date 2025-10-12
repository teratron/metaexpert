# Feature Specification: MetaExpert CLI for Creating New Experts

**Feature Branch**: `feature/cli-new-expert`  
**Created**: воскресенье, 12 октября 2025 г.  
**Status**: Draft  
**Input**: User description: "CLI: @/src/metaexpert/cli for a project with an entry point @/src/metaexpert/__main__.py to create a new expert from a reference template @/src/metaexpert/template/template.py using the commands `new` and/or `--new`, `help` and/or `--help` and other commands when it becomes necessary to add them."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Expert Template (Priority: P1)

As a user, I want to create a new trading expert by running a simple CLI command that generates a complete template file based on the reference template, so I can quickly start developing my custom trading strategy without having to manually copy and structure the template myself.

**Why this priority**: This is the core functionality that enables users to start creating custom trading experts efficiently. Without this, users must manually copy the template, which is error-prone and time-consuming.

**Independent Test**: Can be fully tested by running the `metaexpert new my_strategy` command and verifying that a new file `my_strategy.py` is created with the appropriate template content.

**Acceptance Scenarios**:

1. **Given** user has installed the MetaExpert package, **When** user runs `metaexpert new my_strategy`, **Then** a new Python file named `my_strategy.py` is created in the current directory with the template structure populated
2. **Given** user runs `metaexpert new MyStrategy`, **When** command executes, **Then** a new file named `MyStrategy.py` is created with proper class/function naming conventions adapted to the input name
3. **Given** user runs `metaexpert new my_strategy` in a directory where the file doesn't exist, **When** command executes, **Then** the file is created without overwriting any existing files

---

### User Story 2 - Get Help Information (Priority: P1)

As a user, I want to access help information about available commands and their usage, so I can understand how to use the CLI effectively without referring to external documentation.

**Why this priority**: Essential for user experience and discoverability of functionality. Users need to understand what commands are available and how to use them.

**Independent Test**: Can be fully tested by running `metaexpert --help` or `metaexpert help` and verifying that clear usage information is displayed.

**Acceptance Scenarios**:

1. **Given** user runs `metaexpert --help`, **When** command executes, **Then** comprehensive help information is displayed showing available commands and their purposes
2. **Given** user runs `metaexpert help new`, **When** command executes, **Then** detailed help information specific to the `new` command is displayed
3. **Given** user runs `metaexpert -h`, **When** command executes, **Then** the same help information as `--help` is displayed (short-form alias)

---

### User Story 3 - Command Error Handling (Priority: P2)

As a user, when I provide invalid arguments or commands, I want to receive clear error messages, so I can quickly understand what went wrong and how to fix it.

**Why this priority**: Good error handling prevents user frustration and provides guidance for correct usage.

**Independent Test**: Can be tested by running invalid commands and verifying appropriate error messages are displayed.

**Acceptance Scenarios**:

1. **Given** user runs `metaexpert invalid_command`, **When** command executes, **Then** an error message is displayed indicating the command is not recognized
2. **Given** user runs `metaexpert new` without providing a name, **When** command executes, **Then** an error message is displayed indicating the name argument is required
3. **Given** user runs `metaexpert new` with an invalid filename, **When** command executes, **Then** an error message is displayed about valid naming conventions

---

### Edge Cases

- What happens when a user tries to create a new expert with a name that conflicts with existing Python keywords or reserved names?
- How does the system handle special characters, spaces, or invalid characters in the expert name?
- What happens when a file with the same name already exists in the current directory?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a `new` command to generate a new expert template from the reference template
- **FR-002**: The system MUST allow users to run `metaexpert new <expert_name>` to create a new expert file
- **FR-003**: The system MUST generate a Python file named `<expert_name>.py` with all the necessary template structure
- **FR-004**: The system MUST ensure the generated expert file follows proper Python naming conventions (e.g., replacing spaces, special characters with underscores)
- **FR-005**: The system MUST preserve all template functionality in the generated expert file
- **FR-006**: The system MUST provide a `help` command to display available commands and their usage
- **FR-007**: The system MUST accept both `--help` and `-h` as aliases for the help command
- **FR-008**: The system MUST accept both `help <command>` and `<command> --help` for command-specific help
- **FR-009**: The system MUST validate the expert name argument to ensure it follows Python naming conventions and reject names that are not valid Python identifiers (e.g., starting with numbers, containing special characters other than underscores, matching Python reserved keywords)
- **FR-010**: The system MUST check if a file with the same name already exists and provide an appropriate message
- **FR-011**: The system MUST properly handle the entry point configuration as specified in the template
- **FR-012**: The system MUST update all relevant identifiers in the template to match the new expert name
- **FR-013**: The system MUST preserve all comments and documentation in the generated template
- **FR-014**: The system MUST provide clear error messages for invalid commands or arguments
- **FR-015**: The system MUST handle special characters and spaces in the expert name appropriately
- **FR-016**: The system MUST follow the existing project structure and conventions
- **FR-017**: The system MUST ensure the generated expert file imports the necessary modules correctly
- **FR-018**: The system MUST maintain all event handlers and their proper structure in the generated expert
- **FR-019**: The system MUST create a command-line interface module at `@/src/metaexpert/cli` as specified
- **FR-020**: The system MUST have an entry point at `@/src/metaexpert/__main__.py` that delegates to the CLI

### Key Entities *(include if feature involves data)*

- **Expert Template**: A Python file that serves as the reference structure for creating new trading experts, containing all necessary configuration parameters, event handlers, and the main entry point
- **Expert Name**: A string identifier provided by the user that determines the name of the generated expert file and updates internal identifiers within the template

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new expert template in under 10 seconds from the command line
- **SC-002**: 95% of users successfully create their first expert using the CLI without referring to additional documentation
- **SC-003**: The system handles 100% of valid expert name inputs without errors
- **SC-004**: Users can access help information and understand available commands within 30 seconds of running the help command