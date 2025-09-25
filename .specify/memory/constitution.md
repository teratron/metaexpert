<!-- 
Version Change: 2.0.0 → 2.0.1
Modified Principles: I. Code Quality Standards updated to include ruff, pyright, and import organization requirements
Added Sections: None
Removed Sections: None
Templates Requiring Updates: 
✅ .specify/templates/plan-template.md (updated constitution version reference from v2.0.0 to v2.0.1)
Follow-up TODOs: None
-->

# MetaExpert Constitution

## Core Principles

### I. Code Quality Standards
All Python code must adhere to established quality standards: consistent formatting using ruff and black, comprehensive type annotations validated with pyright, documentation for all public interfaces, proper import organization using isort, and compliance with project linting rules. After generating Python code, developers must check and fix errors and warnings using ruff and pyright, and organize imports. Code reviews must verify these standards before approval.

### II. Testing Standards & Coverage
Comprehensive testing is mandatory: Unit tests for all functions/methods with minimum 85% coverage, Integration tests for inter-component interactions, End-to-end tests for critical user flows, and Performance tests for performance-sensitive components. All tests must pass before merging.

### III. User Experience Consistency
User interfaces and interactions must maintain consistent behavior across all features: Follow established design patterns and UI components, Maintain consistent error messaging and handling, Ensure responsive behavior across different environments, Provide clear feedback for all user actions.

### IV. Performance Requirements
All components must meet defined performance benchmarks: Maximum response times for user interactions (sub-200ms for simple operations), Efficient resource utilization (memory, CPU, network), Scalability under expected load conditions, Optimized algorithms and data structures for performance-critical paths.

### V. Continuous Quality Assurance
Quality must be maintained throughout the development lifecycle: Automated quality checks on all commits, Regular refactoring to maintain code health, Continuous monitoring of performance metrics, Regular security assessments and updates.

## Additional Constraints

The technology stack requires Python 3.12 or higher. All dependencies must be explicitly declared in the pyproject.toml file. Compliance with MIT licensing standards is mandatory. For all tasks related to the MetaExpert project, use only the UV package manager (no pip, requirements.txt, setup.py, or similar). Always activate the virtual environment using .venv/Scripts/activate before executing any UV commands.

## Development Workflow

All code changes must go through pull request review. Testing gates include unit tests with minimum 85% coverage and integration tests for API changes. Deployment requires approval from project maintainers. Automated quality checks must pass before merging.

## Governance
This constitution supersedes all other development practices. Amendments require documentation, stakeholder approval, and a migration plan. All pull requests and reviews must verify compliance with these principles. Complexity must be justified with clear rationale. Refer to project documentation for runtime development guidance.

**Version**: 2.0.1 | **Ratified**: 2025-09-20 | **Last Amended**: 2025-09-25