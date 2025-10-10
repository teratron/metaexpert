<!-- 
Sync Impact Report:
- Version change: 2.2.0 → 2.3.0 (added Template File Requirements section)
- Added sections: Template File Requirements section
- Templates requiring updates: ✅ .specify/templates/plan-template.md / ✅ .specify/templates/spec-template.md / ✅ .specify/templates/tasks-template.md 
- Follow-up TODOs: RATIFICATION_DATE needs to be determined
-->

# MetaExpert Constitution

## Core Principles

### Library-First Architecture
Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries

### CLI Interface
Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats

### Test-First (NON-NEGOTIABLE)
Comprehensive testing is mandatory: Unit tests for all functions/methods with minimum 85% coverage, Integration tests for inter-component interactions, End-to-end tests for critical user flows, and Performance tests for performance-sensitive components. All tests must pass before merging. For all test types, use pytest framework as the required testing tool, ensuring proper test discovery, execution, and reporting through pytest built-in functionality and compatible plugins. TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced

### Integration Testing
Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas

### UI Consistency
User interfaces and interactions must maintain consistent behavior across all features: Follow established design patterns and UI components, Maintain consistent error messaging and handling, Ensure responsive behavior across different environments, Provide clear feedback for all user actions

## Performance Benchmarks

All components must meet defined performance benchmarks: Maximum response times for user interactions (sub-200ms for simple operations), Efficient resource utilization (memory, CPU, network), Scalability under expected load conditions, Optimized algorithms and data structures for performance-critical paths.

## Quality Maintenance

Quality must be maintained throughout the development lifecycle: Automated quality checks on all commits, Regular refactoring to maintain code health, Continuous monitoring of performance metrics, Regular security assessments and updates.

## SOLID Principles

Classes, methods, functions and modules must follow the SOLID principles: Single Responsibility Principle (each class/module has one reason to change), Open/Closed Principle (software entities should be open for extension but closed for modification), Liskov Substitution Principle (objects should be replaceable with instances of their subtypes), Interface Segregation Principle (clients should not be forced to depend on interfaces they don't use), Dependency Inversion Principle (high-level modules should not depend on low-level modules, both should depend on abstractions).

## DRY Principle

"Do not Repeat Yourself" - Code duplication must be eliminated and each piece of knowledge must have a single authoritative representation in the system. All shared functionality must be extracted into reusable components, functions, or modules to ensure a single source of truth and reduce maintenance overhead.

## KISS Principle

"Keep It Simple, Stupid" - Code and architectural solutions must maintain simplicity and avoid unnecessary complexity. Before implementing complex solutions, evaluate if a simpler approach would be equally effective. Simple code is easier to understand, maintain, test, and debug.

## YAGNI Principle

"You Ain't Gonna Need It" - Only implement functionality that is currently needed, not anticipated future needs. Avoid adding features or infrastructure for potential future use cases that are not immediately required. This prevents code bloat and reduces maintenance burden.

## FSD Principle

"Feature-Sliced Design" - Architectural methodology for creating scalable applications with layer-based organization. Each feature should be implemented as a cohesive slice that spans all necessary layers (UI, business logic, data access), promoting better maintainability and clearer separation of concerns. This approach improves scalability and simplifies feature development, particularly for frontend applications.

## OOP Principle

"Object-Oriented Programming" - All code must follow OOP principles: Encapsulation to hide internal state and implementation details, Inheritance to promote code reuse and create hierarchical relationships, Polymorphism to allow objects of different types to be treated uniformly, and Abstraction to focus on behavior rather than implementation details. This ensures maintainable and scalable code design.

## Python Code Quality Standards

All Python code must adhere to established quality standards: consistent formatting using ruff, comprehensive type annotations validated with pyright, documentation for all public interfaces, proper import organization using isort, and compliance with project linting rules. After each creation or modification of Python files, developers MUST automatically run checks using ruff and pyright, analyze all warnings and errors, and then make the necessary corrections to the code to fix problems, ensuring compliance with style and typing standards. Code reviews must verify these standards before approval.

## Additional Constraints

Technology stack requirements: Python 3.12+, modular architecture, dependency management with uv (no pip, requirements.txt, setup.py, or similar), testing with pytest, formatting and linting with ruff, type annotations validated with pyright. Always activate the virtual environment using .venv/Scripts/activate before executing any uv commands.

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

## Documentation Requirements

Upon every task execution that involves functional changes, the documentation in the @/docs directory must be updated, preserving the existing documentation structure: api, guides, tutorials. Additionally, the README.md file in the project root must be updated to ensure the functionality description, usage examples, and configuration information remain current. The documentation must reflect all changes made to the API, new methods, parameters, data formats, and system behavior characteristics.

## Versioning Requirements

Each significant functional change must update the project version according to the Semantic Versioning (SemVer) convention. Changes must be applied to all files where the version is mentioned: @/pyproject.toml, @/README.md, @/src/metaexpert/__version__.py, @/docs/* (where applicable) and any other relevant files. When updating versions, dependencies from external libraries, documentation updates, API changes, and backward compatibility must be taken into account. Versioning must strictly follow the major.minor.patch rules with corresponding updates in changelog and release tags. Major version updates indicate backward incompatible changes, minor version updates indicate new functionality in a backward compatible manner, and patch version updates indicate backward compatible bug fixes.

## Template File Requirements

The @/src/metaexpert/template/file.py is a reference template that serves as the basis for the library and is used as a starting point when creating new projects using the `metaexpert new` or `metaexpert --new` command. This file remains unchanged without explicit approval. With each new task, the AI agent must check this template to make sure that the changes performed do not contradict its structure and content.

## Development Workflow

Code review requirements: All PRs must be reviewed by at least one other team member, Testing gates: Unit tests must pass, Integration tests for features touching contracts, Deployment approval process follows semantic versioning

## Governance

All PRs/reviews must verify compliance with these principles; Complexity must be justified with clear rationale; Use development guidelines for runtime development guidance. Amendment process requires team consensus and documented justification.

**Version**: 2.3.0 | **Ratified**: TODO(RATIFICATION_DATE): Need to determine original adoption date | **Last Amended**: 2025-10-10