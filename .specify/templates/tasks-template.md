---
description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

**NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T011 [P] [US1] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T013 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T014 [US1] Implement [Service] in src/services/[service].py (depends on T012, T013)
- [ ] T015 [US1] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T016 [US1] Add validation and error handling
- [ ] T017 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T019 [P] [US2] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py
- [ ] T025 [P] [US3] Integration test for [user journey] in tests/integration/test_[name].py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/
- [ ] TXXX Security hardening
- [ ] TXXX UI consistency check: Ensure all UI elements follow established design patterns
- [ ] TXXX UI consistency check: Verify consistent error messaging and handling across all interfaces
- [ ] TXXX UI consistency check: Validate responsive behavior across different environments
- [ ] TXXX UI consistency check: Confirm clear feedback for all user actions
- [ ] TXXX Performance benchmark check: Verify sub-200ms response times for simple operations
- [ ] TXXX Performance benchmark check: Validate efficient resource utilization (memory, CPU, network)
- [ ] TXXX Performance benchmark check: Test scalability under expected load conditions
- [ ] TXXX Performance benchmark check: Ensure optimized algorithms and data structures for performance-critical paths
- [ ] TXXX Quality check: Implement automated quality checks on all commits
- [ ] TXXX Quality check: Perform regular refactoring to maintain code health
- [ ] TXXX Quality check: Set up continuous monitoring of performance metrics
- [ ] TXXX Quality check: Conduct regular security assessments and updates
- [ ] TXXX SOLID check: Verify all classes adhere to Single Responsibility Principle
- [ ] TXXX SOLID check: Ensure entities follow Open/Closed Principle (open for extension, closed for modification)
- [ ] TXXX SOLID check: Validate Liskov Substitution Principle compliance for inheritance hierarchies
- [ ] TXXX SOLID check: Apply Interface Segregation Principle (no forced dependencies on unused interfaces)
- [ ] TXXX SOLID check: Implement Dependency Inversion Principle (depend on abstractions)
- [ ] TXXX DRY check: Identify and eliminate code duplication
- [ ] TXXX DRY check: Ensure each piece of knowledge has a single authoritative representation
- [ ] TXXX DRY check: Extract shared functionality into reusable components, functions, or modules
- [ ] TXXX DRY check: Establish single source of truth to reduce maintenance overhead
- [ ] TXXX KISS check: Evaluate code and architectural solutions for unnecessary complexity
- [ ] TXXX KISS check: Assess complex solutions against simpler alternatives before implementation
- [ ] TXXX KISS check: Prioritize simple code for better understandability, maintainability, testability, and debuggability
- [ ] TXXX KISS check: Ensure implementation follows the "Keep It Simple, Stupid" principle
- [ ] TXXX YAGNI check: Verify only currently needed functionality is implemented
- [ ] TXXX YAGNI check: Ensure features for anticipated future needs are not added prematurely
- [ ] TXXX YAGNI check: Validate that infrastructure for potential future use cases is not added if not immediately required
- [ ] TXXX YAGNI check: Confirm implementation follows "You Ain't Gonna Need It" principle to prevent code bloat
- [ ] TXXX FSD check: Implement features as cohesive slices spanning all necessary layers (UI, business logic, data access)
- [ ] TXXX FSD check: Apply Feature-Sliced Design methodology for architectural organization
- [ ] TXXX FSD check: Ensure feature implementation promotes better maintainability and clearer separation of concerns
- [ ] TXXX FSD check: Verify feature development approach improves scalability and simplifies feature development
- [ ] TXXX Testing check: Write unit tests for all functions/methods with minimum 85% coverage
- [ ] TXXX Testing check: Create integration tests for inter-component interactions
- [ ] TXXX Testing check: Implement end-to-end tests for critical user flows
- [ ] TXXX Testing check: Conduct performance tests for performance-sensitive components
- [ ] TXXX Testing check: Ensure all tests pass before merging using pytest framework
- [ ] TXXX Testing check: Ensure proper test discovery, execution, and reporting through pytest built-in functionality and compatible plugins
- [ ] TXXX Python Quality check: Ensure all Python code follows ruff and black formatting standards
- [ ] TXXX Python Quality check: Validate comprehensive type annotations with pyright
- [ ] TXXX Python Quality check: Add proper documentation for all public interfaces
- [ ] TXXX Python Quality check: Organize imports properly using isort
- [ ] TXXX Python Quality check: Run ruff and pyright checks after each modification and fix all issues
- [ ] TXXX Documentation check: Update documentation in @/docs directory for functional changes
- [ ] TXXX Documentation check: Preserve documentation structure (api, guides, tutorials) when updating @/docs
- [ ] TXXX Documentation check: Update README.md file to ensure functionality description remains current
- [ ] TXXX Documentation check: Update README.md with usage examples and configuration information
- [ ] TXXX Documentation check: Ensure documentation reflects all changes to API, methods, parameters, data formats, and system behavior
- [ ] TXXX Versioning check: Update project version according to Semantic Versioning for significant functional changes
- [ ] TXXX Versioning check: Apply version updates to all relevant files (pyproject.toml, README.md, __version__.py, docs/*)
- [ ] TXXX Versioning check: Follow major.minor.patch rules (major=backward incompatible, minor=new functionality, patch=bug fixes)
- [ ] TXXX Versioning check: Update changelog and release tags corresponding to version changes
- [ ] TXXX Versioning check: Consider external library dependencies, API changes, and backward compatibility when updating versions
- [ ] TXXX OOP check: Ensure all code follows OOP principles - Encapsulation to hide internal state and implementation details
- [ ] TXXX OOP check: Ensure all code follows OOP principles - Inheritance to promote code reuse and create hierarchical relationships
- [ ] TXXX OOP check: Ensure all code follows OOP principles - Polymorphism to allow objects of different types to be treated uniformly
- [ ] TXXX OOP check: Ensure all code follows OOP principles - Abstraction to focus on behavior rather than implementation details
- [ ] TXXX OOP check: Verify code maintains scalable and maintainable design through OOP principles
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence


