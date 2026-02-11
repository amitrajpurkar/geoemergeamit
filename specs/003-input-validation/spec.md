# Feature Specification: Client-Side Input Validation

**Feature Branch**: `003-input-validation`  
**Created**: February 10, 2026  
**Status**: Draft  
**Input**: User description: "Handle input data validation for zip code and date range on both home and query pages; zip code should be a 5-digit number; handle format validation on client side and show error message if invalid; date picker should restrict values to only valid dates"

## Clarifications

### Session 2026-02-10

- Q: Should validation ONLY validate ZIP code format, or also handle city/state text inputs? → A: Validate both formats with appropriate rules for each (allow 5-digit ZIP codes OR city/state text format)
- Q: When should validation errors first appear for each input field? → A: On blur (when user leaves the field)
- Q: Should date picker restrict to specific data availability ranges or allow any historical dates? → A: Allow any past dates (1990-present), let backend handle unavailable data
- Q: How should validation error messages be announced to screen reader users? → A: Use ARIA live regions with polite announcements

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Location Input Format Validation (Priority: P1)

Users entering a location on the Home page or Drivers page need immediate feedback when they enter an invalid format, preventing wasted API calls and improving user experience. The system accepts both 5-digit ZIP codes and city/state text (e.g., "Miami, FL").

**Why this priority**: This is the most common user error and directly prevents invalid API requests. Location validation is the primary gating mechanism for valid queries.

**Independent Test**: Can be fully tested by entering various location formats (4 digits, 6 digits, letters only, empty input) and verifying that either valid 5-digit ZIP codes OR city/state text are accepted. Delivers immediate user feedback without backend involvement.

**Acceptance Scenarios**:

1. **Given** a user is on the Home page, **When** they enter a 5-digit ZIP code (e.g., "33172"), **Then** no validation error appears and the submit button remains enabled
2. **Given** a user is on the Home page, **When** they enter city/state text (e.g., "Miami, FL" or "Los Angeles"), **Then** no validation error appears and the submit button remains enabled
3. **Given** a user is on the Home page, **When** they enter a numeric value that is not 5 digits (e.g., "3317" or "331722"), **Then** an inline error message appears stating "Enter a 5-digit ZIP code or city/state name" and the submit button is disabled
4. **Given** a user is on the Home page, **When** they enter only special characters or numbers mixed with special chars (e.g., "!!!", "33-172"), **Then** an inline error message appears stating "Enter a 5-digit ZIP code or city/state name" and the submit button is disabled
5. **Given** a user is on the Home page, **When** they leave the location field empty, **Then** an inline error message appears stating "Location is required" and the submit button is disabled
6. **Given** a user enters an invalid location and sees an error, **When** they correct it to either a valid ZIP or city/state, **Then** the error message disappears immediately and the submit button becomes enabled

---

### User Story 2 - Date Range Validation (Priority: P2)

Users selecting date ranges need constraints that prevent selecting invalid or illogical date combinations, ensuring all queries have valid temporal bounds.

**Why this priority**: Prevents backend errors from invalid date ranges and guides users toward valid inputs. Essential for data integrity but less frequent than ZIP code errors.

**Independent Test**: Can be tested by attempting to select dates in various invalid combinations (end before start, future dates, dates outside available data range) and verifying that the date inputs prevent or correct these selections.

**Acceptance Scenarios**:

1. **Given** a user is selecting dates, **When** they choose a start date, **Then** the end date picker automatically sets its minimum allowed date to the selected start date
2. **Given** a user has selected a start date, **When** they attempt to select an end date before the start date, **Then** the date picker prevents the selection and keeps the previous valid end date
3. **Given** a user is selecting dates, **When** they attempt to select a future date, **Then** the date picker prevents selecting dates beyond today's date
4. **Given** a user has selected an invalid date range, **When** the form is submitted, **Then** a validation error appears stating "End date must be after start date" and submission is blocked
5. **Given** a user is on the Drivers page, **When** they select dates, **Then** the same date validation rules apply consistently with the Home page

---

### User Story 3 - Real-Time Validation Feedback (Priority: P3)

Users receive immediate visual feedback as they type or select inputs, creating a responsive and intuitive interface that guides them toward correct inputs without requiring submission attempts.

**Why this priority**: Enhances user experience by preventing errors proactively rather than reactively. Nice-to-have polish that reduces user frustration.

**Independent Test**: Can be tested by typing in input fields and observing real-time validation messages, visual indicators (red borders, checkmarks), and submit button state changes without clicking submit.

**Acceptance Scenarios**:

1. **Given** a user is typing in the location field, **When** they are still focused on the field, **Then** no validation error appears (validation waits for blur event)
2. **Given** a user has entered text in the location field, **When** they move to another field (blur event), **Then** validation runs immediately and shows success indicator or error message
3. **Given** a user sees a validation error, **When** they start correcting the input, **Then** the error message remains visible until the input becomes valid
4. **Given** all form inputs are valid, **When** the user views the form, **Then** the submit button has normal styling and is enabled
5. **Given** any form input is invalid, **When** the user views the form, **Then** the submit button is visually disabled (grayed out) and shows a tooltip explaining why when hovered

---

### Edge Cases

- What happens when a user pastes content into the ZIP code field (e.g., "ZIP: 33172" or "33172-1234")?
- What happens when a user enters leading zeros in the ZIP code (e.g., "00123" - valid format but potentially invalid location)?
- How does the system handle date inputs when the user's browser is set to a non-US locale with different date formats?
- What happens if a user rapidly switches between date fields while validation is running?
- How does validation behave when the user uses browser autofill for the location field?
- What happens when the date picker is opened but the user clicks outside without selecting a date?
- How does validation handle whitespace (leading/trailing spaces in ZIP code input)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate location input format client-side before allowing form submission
- **FR-002**: System MUST accept EITHER (a) exactly 5 numeric digits (ZIP code) OR (b) text containing letters, spaces, and commas (city/state format)
- **FR-003**: System MUST display an inline error message below the location input field when validation fails
- **FR-004**: System MUST disable the submit button when any input validation fails
- **FR-005**: System MUST re-enable the submit button immediately when all validations pass
- **FR-006**: System MUST validate that end date is not before start date
- **FR-007**: System MUST prevent users from selecting future dates in the date picker (maximum: today's date)
- **FR-007a**: System MUST prevent users from selecting dates before 1990-01-01 (minimum: January 1, 1990)
- **FR-008**: System MUST apply date range validation on both Home page and Drivers page consistently
- **FR-009**: System MUST apply location format validation on both Home page and Drivers page consistently
- **FR-010**: System MUST clear validation error messages when the user corrects the input to a valid value
- **FR-011**: System MUST trim leading and trailing whitespace from location input before validation
- **FR-012**: System MUST provide visual feedback (e.g., red border) on invalid input fields
- **FR-013**: System MUST prevent form submission via Enter key when validation fails
- **FR-014**: Date picker MUST restrict selectable dates to valid ranges (no future dates, no dates before 1990-01-01, end date ≥ start date)
- **FR-015**: System MUST show validation errors in a consistent visual style (color, font, positioning) across all pages
- **FR-016**: System MUST use ARIA live regions with `aria-live="polite"` to announce validation errors to screen reader users
- **FR-017**: System MUST associate error messages with their corresponding input fields using `aria-describedby` attributes
- **FR-018**: System MUST mark invalid input fields with `aria-invalid="true"` when validation fails

### Key Entities

- **Validation Error**: Represents a failed validation check with an error message, input field identifier, and visibility state
- **Form State**: Tracks validation status of all inputs (valid/invalid), aggregates errors, and controls submit button enabled state

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users cannot submit queries with invalid ZIP code formats (100% prevention rate)
- **SC-002**: Users cannot submit queries with invalid date ranges (100% prevention rate)
- **SC-003**: Users receive validation feedback within 200ms of blur event (leaving the input field)
- **SC-004**: Validation error messages are clear and actionable (user testing shows 90%+ understand how to fix errors without external help)
- **SC-005**: Reduction in backend error responses related to invalid ZIP codes by 95%+ (comparing pre/post implementation metrics)
- **SC-006**: Users successfully complete valid queries on first attempt increases by 30%+ (reduced trial-and-error from better input guidance)
- **SC-007**: No accessibility regressions (screen readers announce errors via ARIA live regions without interrupting current speech, keyboard navigation remains fully functional, all interactive elements remain keyboard-accessible)
