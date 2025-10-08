<!-- 
Version Change: 2.0.7 → 2.0.8
Modified Principles: None
Added Sections: Project Structure description in Additional Constraints
Removed Sections: None
Templates Requiring Updates: 
✅ .specify/templates/plan-template.md (updated constitution version reference from v2.0.7 to v2.0.8)
✅ .specify/templates/spec-template.md (updated constitution version reference)
✅ .specify/templates/tasks-template.md (updated constitution version reference)
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

### VI. Template Management
The @/src/metaexpert/template/template.py file is the primary (reference) template for the MetaExpert library, copied into a user's project when the metaexpert new or metaexpert --new command is executed. This file must not be modified without explicit approval from the library owner. For every new task, the AI agent must verify that its actions and outputs do not conflict with the structure, parameters, or functionality defined in template.py. As a developer using the MetaExpert library, one must create new trading strategies by using the template.py file to quickly set up a working expert advisor with all the necessary configuration options and event handlers.

### VII. Documentation Management
Upon every task execution that involves functional changes, the documentation in the @/docs directory must be updated, preserving the existing documentation structure: api, guides, tutorials. Additionally, the README.md file in the project root must be updated to ensure the functionality description, usage examples, and configuration information remain current. The documentation must reflect all changes made to the API, new methods, parameters, data formats, and system behavior characteristics.

### VIII. Version Management
Each significant functional change must update the project version according to the Semantic Versioning (SemVer) convention. Changes must be applied to all files where the version is mentioned: @/pyproject.toml, @/README.md, @/src/metaexpert/__version__.py, @/docs/* (where applicable) and any other relevant files. When updating versions, dependencies from external libraries, documentation updates, API changes, and backward compatibility must be taken into account. Versioning must strictly follow the major.minor.patch rules with corresponding updates in changelog and release tags. Major version updates indicate backward incompatible changes, minor version updates indicate new functionality in a backward compatible manner, and patch version updates indicate backward compatible bug fixes.

## Additional Constraints

MetaExpert is a library designed for cryptocurrency trading that provides a unified interface for multiple exchanges (initially Binance, Bybit, OKX and etc.) and supports various trading options through their respective APIs. The library aims to simplify algorithmic trading by providing a consistent interface while maintaining access to exchange-specific features. The system must: create a unified interface for multiple cryptocurrency exchanges; support all major trading types (spot, futures, margin, options and etc.) through exchange APIs; provide an event-driven architecture for trading strategies; enable easy strategy implementation through decorators; support paper trading and live trading modes; and implement comprehensive risk management features. The technology stack requires Python 3.12 or higher. All dependencies must be explicitly declared in the pyproject.toml file. Compliance with MIT licensing standards is mandatory. For all tasks related to the MetaExpert project, use only the UV package manager (no pip, requirements.txt, setup.py, or similar). Always activate the virtual environment using .venv/Scripts/activate before executing any UV commands.

The project consists of two main directories: @/src/metaexpert contains the core library with a modular system where each module handles specific functions (avoid creating model and service modules), and @/examples contains three sample projects that serve as verification material for client developers.

### Language Requirements
Code and documentation language:
- All code, comments, documentation, variable names, function names, class names, method names, attribute names, and technical terms must be in English
- Maintain English as the primary language for all technical elements including error messages, log entries, configuration keys, and API responses to ensure readability and maintainability
- Technical documentation, inline comments, docstrings, and README files must be written in English
- All commit messages, pull request descriptions, and issue titles related to code changes should be in English

Communication style:
- Explanations and discussions in the chat interface should be in Russian
- Use Russian for conversational responses, clarifications, project planning, and non-technical interactions
- Project management communications, feature discussions, and strategic decisions should be conducted in Russian
- Code review comments and technical discussions during development can be in Russian unless collaborating with English-speaking developers

## Development Workflow

All code changes must go through pull request review. Testing gates include unit tests with minimum 85% coverage and integration tests for API changes. Deployment requires approval from project maintainers. Automated quality checks must pass before merging.

## Governance
This constitution supersedes all other development practices. Amendments require documentation, stakeholder approval, and a migration plan. All pull requests and reviews must verify compliance with these principles. Complexity must be justified with clear rationale. Refer to project documentation for runtime development guidance.

**Version**: 2.0.8 | **Ratified**: 2025-09-20 | **Last Amended**: 2025-10-08