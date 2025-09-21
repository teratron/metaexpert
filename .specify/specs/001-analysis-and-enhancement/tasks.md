# Tasks: MetaExpert Library Template Enhancement

**Input**: Design documents from `/specs/feature/analysis-and-enhancement/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python project with dependencies
- [ ] T003 [P] Configure linting and formatting tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
In accordance with the Test-First Development principle (NON-NEGOTIABLE) from the MetaExpert Constitution:
- [ ] T004 [P] Contract test POST /template/create in tests/contract/test_template_creation.py
- [ ] T005 [P] Contract test template validation in tests/contract/test_template_validation.py
- [ ] T006 [P] Integration test template creation in tests/integration/test_template_creation.py
- [ ] T007 [P] Integration test template customization in tests/integration/test_template_customization.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T008 [P] Template creation service in src/services/template_service.py
- [ ] T009 [P] CLI command for template creation in src/cli/template_commands.py
- [ ] T010 [P] Template validation service in src/services/template_validation_service.py
- [ ] T011 Template file copying functionality
- [ ] T012 Template parameter configuration
- [ ] T013 Template structure validation
- [ ] T014 Error handling and logging

## Phase 3.4: Integration
- [ ] T015 Connect template service to CLI
- [ ] T016 Template file validation middleware
- [ ] T017 Request/response logging
- [ ] T018 Template version management

## Phase 3.5: Polish
- [ ] T019 [P] Unit tests for template validation in tests/unit/test_template_validation.py
- [ ] T020 Performance tests (<200ms)
- [ ] T021 [P] Update docs/template.md
- [ ] T022 Remove duplication
- [ ] T023 Run manual-testing.md

## Dependencies
- Tests (T004-T007) before implementation (T008-T014)
- T008 blocks T009, T015
- T016 blocks T018
- Implementation before polish (T019-T023)

## Parallel Example
```
# Launch T004-T007 together:
Task: "Contract test POST /template/create in tests/contract/test_template_creation.py"
Task: "Contract test template validation in tests/contract/test_template_validation.py"
Task: "Integration test template creation in tests/integration/test_template_creation.py"
Task: "Integration test template customization in tests/integration/test_template_customization.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

In accordance with the MetaExpert Constitution v1.0.0:
- [x] All contracts have corresponding tests (Integration Testing Coverage principle)
- [ ] All entities have model tasks (Library-First Development principle)
- [x] All tests come before implementation (Test-First Development principle)
- [x] Parallel tasks truly independent (Library-First Development principle)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task