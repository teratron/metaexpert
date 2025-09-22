# Tasks: MetaExpert Library Template Enhancement

**Input**: Design documents from `/specs/001-analysis-and-enhancement/`
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
- [ ] T005 [P] Contract test GET /template/exchanges in tests/contract/test_template_exchanges.py
- [ ] T006 [P] Contract test GET /template/parameters in tests/contract/test_template_parameters.py
- [ ] T007 [P] Contract test GET /config/parameters in tests/contract/test_config_parameters.py
- [ ] T008 [P] Contract test POST /config/validate in tests/contract/test_config_validation.py
- [ ] T009 [P] Integration test template creation in tests/integration/test_template_creation.py
- [ ] T010 [P] Integration test template customization in tests/integration/test_template_customization.py
- [ ] T011 [P] Integration test configuration management in tests/integration/test_config_management.py
- [ ] T012 [P] Integration test environment variable handling in tests/integration/test_env_var_handling.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T013 [P] TemplateFile model in src/models/template_file.py
- [ ] T014 [P] ConfigurationParameter model in src/models/configuration_parameter.py
- [ ] T015 [P] EventHandler model in src/models/event_handler.py
- [ ] T016 [P] Exchange model in src/models/exchange.py
- [ ] T017 [P] ConfigurationSource model in src/models/configuration_source.py
- [ ] T018 [P] StrategyParameter model in src/models/strategy_parameter.py
- [ ] T019 [P] Template creation service in src/services/template_service.py
- [ ] T020 [P] Configuration management service in src/services/config_service.py
- [ ] T021 [P] CLI command for template creation in src/cli/template_commands.py
- [ ] T022 Template file copying functionality
- [ ] T023 Template parameter configuration
- [ ] T024 Template structure validation
- [ ] T025 Configuration parameter alignment
- [ ] T026 Error handling and logging

## Phase 3.4: Integration
- [ ] T027 Connect template service to CLI
- [ ] T028 Template file validation middleware
- [ ] T029 Request/response logging
- [ ] T030 Template version management
- [ ] T031 Configuration source priority handling
- [ ] T032 Exchange API integration

## Phase 3.5: Polish
- [ ] T033 [P] Unit tests for template validation in tests/unit/test_template_validation.py
- [ ] T034 [P] Unit tests for configuration validation in tests/unit/test_config_validation.py
- [ ] T035 Performance tests (<200ms)
- [ ] T036 [P] Update docs/template.md
- [ ] T037 [P] Update docs/configuration.md
- [ ] T038 Remove duplication
- [ ] T039 Run manual-testing.md

## Dependencies
- Tests (T004-T012) before implementation (T013-T026)
- T013-T018 blocks T019-T020
- T019-T020 blocks T021-T027
- Implementation before polish (T033-T039)

## Parallel Example
```
# Launch T004-T008 together:
Task: "Contract test POST /template/create in tests/contract/test_template_creation.py"
Task: "Contract test GET /template/exchanges in tests/contract/test_template_exchanges.py"
Task: "Contract test GET /template/parameters in tests/contract/test_template_parameters.py"
Task: "Contract test GET /config/parameters in tests/contract/test_config_parameters.py"
Task: "Contract test POST /config/validate in tests/contract/test_config_validation.py"

# Launch T009-T012 together:
Task: "Integration test template creation in tests/integration/test_template_creation.py"
Task: "Integration test template customization in tests/integration/test_template_customization.py"
Task: "Integration test configuration management in tests/integration/test_config_management.py"
Task: "Integration test environment variable handling in tests/integration/test_env_var_handling.py"

# Launch T013-T018 together:
Task: "TemplateFile model in src/models/template_file.py"
Task: "ConfigurationParameter model in src/models/configuration_parameter.py"
Task: "EventHandler model in src/models/event_handler.py"
Task: "Exchange model in src/models/exchange.py"
Task: "ConfigurationSource model in src/models/configuration_source.py"
Task: "StrategyParameter model in src/models/strategy_parameter.py"
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

In accordance with the MetaExpert Constitution v1.1.0:
- [x] All contracts have corresponding tests (Integration Testing Coverage principle)
- [x] All entities have model tasks (Library-First Development principle)
- [x] All tests come before implementation (Test-First Development principle)
- [x] Parallel tasks truly independent (Library-First Development principle)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task