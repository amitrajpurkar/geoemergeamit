# Tasks: Client-Side Input Validation

**Input**: Design documents from `/specs/003-input-validation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Deferred post-MVP per constitution check. Manual testing via quickstart.md for acceptance.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create validation utility module structure at frontend/src/utils/validation.ts
- [x] T002 [P] Add TypeScript types for validation errors and form state in frontend/src/utils/validation.ts

**Checkpoint**: Validation module structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core validation functions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Implement `validateLocation()` function for ZIP/city-state dual format validation in frontend/src/utils/validation.ts
- [x] T004 [P] Implement `validateDateRange()` function with 1990-present constraints in frontend/src/utils/validation.ts
- [x] T005 [P] Add error message styling for inline validation errors in frontend/src/styles.css
- [x] T006 [P] Add invalid input border styling (aria-invalid support) in frontend/src/styles.css
- [x] T007 [P] Add disabled button styling in frontend/src/styles.css

**Checkpoint**: Foundation ready - validation functions and styling complete, user story implementation can now begin

---

## Phase 3: User Story 1 - Location Input Format Validation (Priority: P1) 🎯 MVP

**Goal**: Implement location validation (ZIP or city/state) on Home page with immediate blur feedback and submit button control

**Independent Test**: Load Home page, test location input with various formats (5-digit ZIP, city/state, invalid), verify error messages, submit button state, and ARIA attributes

### Implementation for User Story 1

- [x] T008 [US1] Add validation state hooks (locationError, touched) to RiskQueryForm component in frontend/src/components/RiskQueryForm.tsx
- [x] T009 [US1] Add location input blur handler calling validateLocation() in frontend/src/components/RiskQueryForm.tsx
- [x] T010 [US1] Add inline error message display below location input with id="location-error" in frontend/src/components/RiskQueryForm.tsx
- [x] T011 [US1] Add ARIA attributes (aria-invalid, aria-describedby, role="alert", aria-live="polite") to location input and error in frontend/src/components/RiskQueryForm.tsx
- [x] T012 [US1] Implement submit button disabled state based on validation errors in frontend/src/components/RiskQueryForm.tsx
- [x] T013 [US1] Add Enter key submission prevention when validation fails in frontend/src/components/RiskQueryForm.tsx
- [ ] T014 [US1] Manual test: Verify location validation on Home page per quickstart.md Test Scenario 1

**Checkpoint**: User Story 1 complete - Location validation works on Home page with accessibility support

---

## Phase 4: User Story 2 - Date Range Validation (Priority: P2)

**Goal**: Implement date range validation with min/max constraints and start/end date logic on both Home and Drivers pages

**Independent Test**: Select various date combinations (end before start, future dates, pre-1990), verify date picker constraints and error messages

### Implementation for User Story 2

- [x] T015 [US2] Add validation state hooks (dateErrors) to RiskQueryForm component in frontend/src/components/RiskQueryForm.tsx
- [x] T016 [US2] Add min/max attributes to start date input (min="1990-01-01", max=today) in frontend/src/components/RiskQueryForm.tsx
- [x] T017 [US2] Add min/max attributes to end date input (min="1990-01-01", max=today) in frontend/src/components/RiskQueryForm.tsx
- [x] T018 [US2] Add date blur handler calling validateDateRange() for both start and end dates in frontend/src/components/RiskQueryForm.tsx
- [x] T019 [US2] Add inline error messages below start and end date inputs with appropriate ids in frontend/src/components/RiskQueryForm.tsx
- [x] T020 [US2] Add ARIA attributes (aria-invalid, aria-describedby) to date inputs in frontend/src/components/RiskQueryForm.tsx
- [x] T021 [US2] Update submit button disabled logic to include date validation errors in frontend/src/components/RiskQueryForm.tsx
- [x] T022 [US2] Apply identical date validation to Drivers page date inputs in frontend/src/pages/Drivers.tsx
- [ ] T023 [US2] Manual test: Verify date validation on Home page per quickstart.md Test Scenario 2
- [ ] T024 [US2] Manual test: Verify date validation consistency on Drivers page per quickstart.md Test Scenario 5

**Checkpoint**: User Stories 1 AND 2 complete - Location and date validation work on both Home and Drivers pages

---

## Phase 5: User Story 3 - Real-Time Validation Feedback (Priority: P3)

**Goal**: Enhance validation UX with visual feedback (red borders, success indicators, button tooltips) and ensure blur-triggered validation

**Independent Test**: Type in inputs, observe visual feedback appears only after blur, not during typing; verify submit button has tooltip when disabled

### Implementation for User Story 3

- [x] T025 [P] [US3] Add success indicator styling (optional green checkmark or border) in frontend/src/styles.css
- [x] T026 [US3] Add tooltip/title attribute to disabled submit button explaining why submission blocked in frontend/src/components/RiskQueryForm.tsx
- [x] T027 [US3] Verify validation only triggers on blur, not during active typing (review blur handler implementation) in frontend/src/components/RiskQueryForm.tsx
- [x] T028 [US3] Add visual red border to invalid inputs using CSS aria-invalid selector (verify T006 styling applied) in frontend/src/styles.css
- [x] T029 [US3] Ensure error messages persist until input becomes valid (no premature clearing) in frontend/src/components/RiskQueryForm.tsx
- [ ] T030 [US3] Manual test: Verify real-time feedback behavior per quickstart.md Test Scenario 3

**Checkpoint**: All user stories complete - Full validation experience with enhanced visual feedback

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, accessibility validation, and cross-page consistency

**Note**: All tasks below are manual testing/verification tasks. Implementation is complete.

- [ ] T031 [P] Test paste behavior in location field (verify whitespace trimming) per quickstart.md Test Scenario 6
- [ ] T032 [P] Test browser autofill interaction with validation per quickstart.md Test Scenario 6
- [ ] T033 [P] Verify accessibility with browser DevTools (ARIA attributes, keyboard navigation) per quickstart.md Test Scenario 4
- [ ] T034 [P] Test rapid field switching (verify no race conditions) per quickstart.md Test Scenario 6
- [ ] T035 [P] Verify validation consistency between Home and Drivers pages per quickstart.md Test Scenario 5
- [ ] T036 Verify leading zeros in ZIP codes accepted (e.g., "00123") per quickstart.md edge cases
- [ ] T037 Run full quickstart.md validation: All 6 test scenarios pass
- [ ] T038 Verify success criteria: Test with invalid inputs to confirm 100% prevention (SC-001, SC-002)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T002) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T003-T007) - MVP, must complete first
- **User Story 2 (Phase 4)**: Depends on Foundational (T003-T007) - Can start after US1 or in parallel
- **User Story 3 (Phase 5)**: Depends on Foundational (T003-T007) and US1/US2 completion - Enhances existing validation
- **Polish (Phase 6)**: Depends on all user stories (T008-T030) being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends only on Foundational phase - No dependencies on other stories
- **User Story 2 (P2)**: Depends only on Foundational phase - Independent of US1, can be developed in parallel
- **User Story 3 (P3)**: Depends on US1 and US2 being implemented (enhances their validation UX)

### Within Each User Story

- **US1**: All tasks (T008-T014) modify same file (RiskQueryForm.tsx) - must run sequentially
- **US2**: Tasks T015-T021 modify RiskQueryForm.tsx (sequential), T022 modifies Drivers.tsx (can be parallel with T015-T021)
- **US3**: Visual enhancements (T025, T028) can run in parallel; logic checks (T026, T027, T029) sequential

### Parallel Opportunities

**Phase 1 (Setup)**:
- T001 and T002 can run in parallel (different concerns in same file)

**Phase 2 (Foundational)**:
- ALL tasks (T003-T007) can run in parallel (different files: validation.ts vs styles.css; different functions within validation.ts)

**Phase 4 (User Story 2)**:
- T022 (Drivers.tsx) can run in parallel with T015-T021 (RiskQueryForm.tsx)

**Phase 5 (User Story 3)**:
- T025 and T028 (styles.css changes) can run in parallel

**Phase 6 (Polish)**:
- T031, T032, T033, T034, T035 can all run in parallel (different test scenarios, read-only verification)

---

## Parallel Example: Foundational Phase

```bash
# Launch all foundational tasks together (different files/functions):
Task T003: "Implement validateLocation() function in frontend/src/utils/validation.ts"
Task T004: "Implement validateDateRange() function in frontend/src/utils/validation.ts"
Task T005: "Add error message styling in frontend/src/styles.css"
Task T006: "Add invalid input border styling in frontend/src/styles.css"
Task T007: "Add disabled button styling in frontend/src/styles.css"
```

## Parallel Example: User Story 2

```bash
# While working on RiskQueryForm.tsx (T015-T021), separately work on:
Task T022: "Apply date validation to Drivers.tsx" (different file, no conflict)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T007) - **CRITICAL GATE**
3. Complete Phase 3: User Story 1 (T008-T014)
4. **STOP and VALIDATE**: Run T014 manual test
5. Deploy/demo MVP: Location validation on Home page

**Value Delivered**: Users get immediate feedback for invalid location inputs, preventing 95% of invalid API requests for location errors.

### Incremental Delivery

1. **Setup + Foundational** (T001-T007) → Foundation ready
2. **+ User Story 1** (T008-T014) → Test independently → **Deploy MVP** ✅
3. **+ User Story 2** (T015-T024) → Test independently → **Deploy V2** ✅
4. **+ User Story 3** (T025-T030) → Test independently → **Deploy V3** ✅
5. **+ Polish** (T031-T038) → Final validation → **Production Ready** ✅

Each increment is independently deployable and adds value without breaking previous features.

### Parallel Team Strategy

With 2-3 developers:

1. **Together**: Complete Setup + Foundational (T001-T007)
2. **Once Foundational done**:
   - **Developer A**: User Story 1 (T008-T014) - Priority 1, blocking
   - **Developer B**: User Story 2 (T015-T024) - Independent work
   - **Developer C**: User Story 3 prep/styling (T025, T028) - Can start early
3. Stories merge independently without conflicts (different user flows)

---

## Notes

- **[P] tasks**: Different files or independent functions - safe to parallelize
- **[Story] labels**: Maps tasks to user stories from spec.md for traceability
- **No automated tests**: Manual testing via quickstart.md per constitution check (tests deferred post-MVP)
- **File conflicts**: RiskQueryForm.tsx is main bottleneck (US1 → US2 → US3 sequential for that file)
- **Drivers.tsx**: Independent from Home.tsx changes, can work in parallel
- **CSS changes**: Minimal conflicts, can batch or parallelize
- **Validation functions**: Pure, no side effects, easy to test manually
- **Accessibility**: Built-in from start (ARIA attributes in US1), not bolted on later
- **Success metrics**: Tracked via quickstart.md test scenarios and backend error rate monitoring post-deployment

---

## Task Count Summary

- **Total Tasks**: 38
- **Setup**: 2 tasks
- **Foundational**: 5 tasks (blocking, but all parallelizable)
- **User Story 1 (MVP)**: 7 tasks
- **User Story 2**: 10 tasks
- **User Story 3**: 6 tasks
- **Polish**: 8 tasks
- **Parallel opportunities**: 12 tasks marked [P] (31% of total)

---

## MVP Scope Recommendation

**Minimum Viable Product**: Complete through Phase 3 (T001-T014)

**Delivers**:
- Location validation (ZIP or city/state format)
- Inline error messages
- Submit button control
- Full accessibility (ARIA attributes)
- Prevents invalid location API requests

**Defer to V2**:
- Date range validation (User Story 2)
- Enhanced visual feedback (User Story 3)
- Edge case testing (Polish phase)

**Rationale**: User Story 1 is independently testable, delivers primary value (95% of invalid requests are location errors per spec), and demonstrates validation pattern for future stories.
