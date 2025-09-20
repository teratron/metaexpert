<!-- 
Version Change: 1.0.0 → 1.1.0
Modified Principles: None
Added Sections: None
Removed Sections: None
Templates Requiring Updates: None
Follow-up TODOs: None
-->

# MetaExpert Constitution

## Core Principles

### I. Library-First Development
Every feature starts as a standalone library. Libraries must be self-contained, independently testable, and well-documented. Each library must have a clear, single purpose - no organizational-only libraries.

### II. CLI Interface Standard
Every library exposes functionality via a Command Line Interface. Communication follows a text-based protocol: input through stdin/arguments and output through stdout, with errors directed to stderr. Support for both JSON and human-readable formats is required.

### III. Test-First Development (NON-NEGOTIABLE)
Test-Driven Development is mandatory. The process follows: Tests are written → User-approved → Tests fail → Implementation begins. The Red-Green-Refactor cycle must be strictly enforced for all development.

### IV. Integration Testing Coverage
Integration testing is required for: New library contract validation, Contract modifications, Inter-service communication, and Shared schema compatibility.

### V. Observability & Versioning
Text-based I/O ensures debuggability. Structured logging is required for all components. Versioning follows the MAJOR.MINOR.BUILD format with semantic versioning principles.

## Additional Constraints
The technology stack requires Python 3.12 or higher. All dependencies must be explicitly declared in the pyproject.toml file. Compliance with MIT licensing standards is mandatory. For all tasks related to the MetaExpert project, use only the UV package manager (no pip, requirements.txt, setup.py, or similar). Always activate the virtual environment using .venv/Scripts/activate before executing any UV commands.

## Development Workflow
All code changes must go through pull request review. Testing gates include unit tests with minimum 80% coverage and integration tests for API changes. Deployment requires approval from project maintainers.

## Governance
This constitution supersedes all other development practices. Amendments require documentation, stakeholder approval, and a migration plan. All pull requests and reviews must verify compliance with these principles. Complexity must be justified with clear rationale. Refer to project documentation for runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2025-09-20 | **Last Amended**: 2025-09-20