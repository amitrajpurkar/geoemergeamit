# Implementation Plan: Client-Side Input Validation

**Branch**: `003-input-validation` | **Date**: February 10, 2026 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-input-validation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement client-side form validation for location inputs and date range selection on Home and Drivers pages. Validation prevents invalid API requests by enforcing format rules: location must be either a 5-digit ZIP code or city/state text (e.g., "Miami, FL"), and date ranges must be within 1990-01-01 to today with end date ≥ start date. Validation triggers on blur events, provides inline error messages with ARIA live region announcements for accessibility, and disables submit button when validation fails. Primary goal is to reduce backend error responses by 95%+ and increase first-attempt success rate by 30%+.

## Technical Context

**Language/Version**: TypeScript 5.7+, React 18.3+  
**Primary Dependencies**: React, Vite 6.1+, HTML5 form validation APIs  
**Storage**: N/A (client-side validation only, no data persistence)  
**Testing**: Manual testing for MVP (future: Vitest + React Testing Library)  
**Target Platform**: Modern web browsers (Chrome, Firefox, Safari, Edge)  
**Project Type**: Web application (frontend-only changes)  
**Performance Goals**: <200ms validation feedback after blur event  
**Constraints**: WCAG 2.1 AA accessibility compliance, no breaking changes to existing functionality  
**Scale/Scope**: 2 pages (Home, Drivers), 3 input fields (location, start date, end date), ~6 validation rules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle 1: Clean Architecture Boundaries
✅ **PASS** - Frontend validation logic will be self-contained in utility functions and React hooks. No framework dependencies in validation rules (pure functions). Form components will depend on validation utilities, not vice versa.

### Principle 2: Reproducible EDA Over Intuition
✅ **N/A** - This feature does not involve exploratory data analysis or modeling.

### Principle 3: Tests for Non-Trivial Logic
⚠️ **DEFERRED** - Validation logic is testable (pure functions), but tests will be added post-MVP. Validation rules are straightforward (regex, date comparisons), reducing risk. Manual testing planned for MVP acceptance.

**Justification**: MVP focuses on user-facing validation. Test suite addition is Phase 2 or follow-up work.

### Principle 4: Contract-Driven API
✅ **N/A** - This feature does not modify API contracts. Frontend-only validation that prevents invalid requests from reaching the backend.

### Principle 5: Observability, Safety, and Simplicity
✅ **PASS** - Validation errors are displayed to users (not swallowed). No secrets/PII logged. All user inputs validated at form boundary. Minimal implementation (validation functions + React hooks).

### Application & Data Standards
✅ **PASS** - TypeScript provides type safety. No notebooks involved. No raw datasets.

### Development Workflow & Quality Gates
✅ **PASS** - Changes are small and scoped to frontend validation. No unrelated refactors. Aligns with existing React component architecture.

**Overall Status**: ✅ **PASS WITH DEFERRED TESTING** - Feature can proceed. Tests should be added in follow-up iteration.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── RiskQueryForm.tsx          # Modify: Add validation logic
│   │   └── (potential) InputField.tsx # New: Reusable validated input component
│   ├── pages/
│   │   ├── Home.tsx                   # Modify: Integrate validated form
│   │   └── Drivers.tsx                # Modify: Integrate validated form
│   ├── utils/
│   │   └── validation.ts              # New: Validation functions
│   └── styles.css                     # Modify: Add error styling
└── tests/                              # Future: E2E/unit tests
```

**Structure Decision**: Web application structure (frontend-only). This feature modifies existing React components in the `frontend/` directory and adds new utility functions for validation logic. No backend changes required.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
