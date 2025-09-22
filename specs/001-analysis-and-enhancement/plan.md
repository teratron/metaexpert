# Updated Implementation Plan: MetaExpert Library Template Enhancement

**Branch**: `feature/analysis-and-enhancement` | **Date**: 2025-09-21 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/feature/analysis-and-enhancement/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
This feature focuses on ensuring the template.py file serves as a robust starting point for developers creating trading strategies with the MetaExpert library. The template must preserve all core functionality while allowing for strategy-specific customization. Additionally, the configuration system has been enhanced to provide better alignment between environment variables, command-line arguments, and template parameters.

## Technical Context
**Language/Version**: Python 3.12  
**Primary Dependencies**: MetaExpert library, supported exchange APIs, python-dotenv  
**Storage**: N/A  
**Testing**: pytest  
**Target Platform**: Cross-platform (Windows, Linux, macOS)  
**Project Type**: single (library-based)  
**Performance Goals**: N/A  
**Constraints**: Template file structure must remain consistent with MetaExpert library requirements. For all tasks related to the MetaExpert project, use only the UV package manager (no pip, requirements.txt, setup.py, or similar). Always activate the virtual environment using .venv/Scripts/activate before executing any UV commands.  
**Scale/Scope**: Single template file for all user projects with enhanced configuration system

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the MetaExpert Constitution v1.1.0, the following gates must be checked:

1. Library-First Development: All features must start as standalone libraries that are self-contained, independently testable, and well-documented.
2. CLI Interface Standard: Functionality must be exposed via Command Line Interface with text-based protocols.
3. Test-First Development: Test-Driven Development is mandatory with Red-Green-Refactor cycle enforcement.
4. Integration Testing Coverage: Integration tests are required for new contracts, contract changes, and inter-service communication.
5. Observability & Versioning: Structured logging is required, and versioning follows MAJOR.MINOR.BUILD format.
6. Package Management: Only the UV package manager must be used for all dependency management tasks.

## Project Structure

### Documentation (this feature)
```
specs/feature/analysis-and-enhancement/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── config-research.md   # Research on configuration system enhancement
├── enhanced-config-design.md # Design for enhanced configuration system
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/
    └── metaexpert/
        ├── config.py
        ├── _argument.py
        ├── template_creator.py
        └── template.py

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: DEFAULT to Option 1 as this is a single library project

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

4. **Additional Research Tasks**:
   - Task: "Research best practices for environment variable management in Python CLI applications"
   - Task: "Research patterns for aligning configuration systems with template parameters"
   - Task: "Research best practices for command-line argument parsing with complex nested options"

**Output**: research.md, config-research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

6. **Enhanced Configuration System Design**:
   - Create comprehensive environment variable system supporting all exchanges
   - Align config.py with template.py parameters
   - Enhance command-line interface with all template parameters
   - Improve template creator with configuration support

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file, enhanced-config-design.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-35 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Enhanced configuration system | Provides better user experience and alignment with template | Separate configuration systems would increase maintenance overhead and user confusion |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v1.1.0 - See `/memory/constitution.md`*