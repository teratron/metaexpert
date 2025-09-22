# Feature Specification: Implement on_init Handler for Expert Loading

**Feature Branch**: `005-implement-the-on`  
**Created**: 2025-09-22  
**Status**: Draft  
**Input**: User description: "Implement the on_init handler in src/metaexpert/_expert.py and src/metaexpert/service.py to process the on_init event triggered upon expert loading. The handler should support void or int return types, with no parameters (def on_init() -> None | int). Non-zero return values indicate failed initialization, triggering a on_deinit event with reason REASON_INITFAILED. Use an ENUM_INIT_RETCODE-style enumeration (INIT_SUCCEEDED, INIT_FAILED, INIT_PARAMETERS_INCORRECT, INIT_AGENT_NOT_SUITABLE) to manage initialization outcomes, optimize testing agent selection (e.g., via system resource checks), and ensure compatibility with template.py. Update documentation in @/docs/ with English docstrings."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies  
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a developer using the MetaExpert library, I want to implement custom initialization logic in my trading strategy that can indicate success or failure, so that I can properly set up my strategy before trading begins and handle initialization failures gracefully.

### Acceptance Scenarios
1. **Given** a trading strategy with an on_init handler that returns None, **When** the expert is loaded, **Then** the initialization is considered successful and trading proceeds normally.
2. **Given** a trading strategy with an on_init handler that returns 0, **When** the expert is loaded, **Then** the initialization is considered successful and trading proceeds normally.
3. **Given** a trading strategy with an on_init handler that returns a non-zero value, **When** the expert is loaded, **Then** the initialization is considered failed, the on_deinit handler is called with REASON_INITFAILED, and trading does not proceed.
4. **Given** a trading strategy without an on_init handler, **When** the expert is loaded, **Then** the initialization is considered successful and trading proceeds normally.

### Edge Cases
- What happens when the on_init handler raises an exception?
- How does the system handle different non-zero return values?
- What happens if the on_init handler takes parameters (which it shouldn't)?
- How does the system handle initialization when system resources are insufficient?

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST allow developers to implement an on_init handler in their trading strategies
- **FR-002**: System MUST support on_init handlers with no parameters
- **FR-003**: System MUST support on_init handlers with return types of None or int
- **FR-004**: System MUST treat None or 0 return values as successful initialization
- **FR-005**: System MUST treat non-zero return values as failed initialization
- **FR-006**: System MUST trigger the on_deinit handler with REASON_INITFAILED when initialization fails
- **FR-007**: System MUST provide an ENUM_INIT_RETCODE-style enumeration with values INIT_SUCCEEDED, INIT_FAILED, INIT_PARAMETERS_INCORRECT, INIT_AGENT_NOT_SUITABLE
- **FR-008**: System MUST be compatible with the existing template.py structure
- **FR-009**: System MUST include proper English documentation in the docs directory

### Key Entities *(include if feature involves data)*
- **on_init Handler**: A function that runs when an expert is loaded, allowing developers to perform initialization tasks
- **Initialization Return Code**: An enumeration value that indicates the success or failure of initialization
- **REASON_INITFAILED**: A constant that indicates initialization failure as the reason for deinitialization

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous  
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---