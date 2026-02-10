# Research: Client-Side Input Validation

**Feature**: 003-input-validation  
**Date**: February 10, 2026  
**Phase**: 0 - Technical Research & Decisions

## Overview

This document captures technical decisions, patterns, and best practices for implementing client-side form validation in the React-based mosquito risk dashboard.

## Key Decisions

### Decision 1: Validation Strategy

**Decision**: Use controlled React components with custom validation hooks

**Rationale**:
- React 18's concurrent features require state management for validation
- Custom hooks provide reusability across Home and Drivers pages
- Allows fine-grained control over validation timing (blur events)
- Enables ARIA attribute management for accessibility

**Alternatives Considered**:
- **HTML5 native validation**: Rejected due to limited customization for dual-format location validation (ZIP vs city/state) and insufficient accessibility control
- **Third-party library (Formik, React Hook Form)**: Rejected to minimize dependencies and avoid over-engineering for 3 simple inputs
- **Inline validation logic**: Rejected due to code duplication across two pages

**Implementation Approach**:
```typescript
// Custom hook pattern
function useValidation(value, rules) {
  const [error, setError] = useState<string | null>(null)
  const validate = () => { /* validation logic */ }
  return { error, validate, isValid }
}
```

---

### Decision 2: Location Format Detection

**Decision**: Auto-detect format (ZIP vs city/state) based on input pattern

**Rationale**:
- Users shouldn't need to select input mode
- Simple heuristic: if input is 5 digits, validate as ZIP; otherwise validate as city/state text
- Matches existing backend behavior (geocoding service handles both)

**Validation Logic**:
```typescript
function validateLocation(input: string): string | null {
  const trimmed = input.trim()
  if (!trimmed) return "Location is required"
  
  // Check if input is purely numeric
  if (/^\d+$/.test(trimmed)) {
    // Numeric input: must be exactly 5 digits
    if (trimmed.length !== 5) {
      return "Enter a 5-digit ZIP code or city/state name"
    }
    return null // Valid ZIP
  }
  
  // Non-numeric: validate as city/state text
  if (/^[a-zA-Z\s,.-]+$/.test(trimmed)) {
    return null // Valid city/state
  }
  
  // Mixed or invalid characters
  return "Enter a 5-digit ZIP code or city/state name"
}
```

---

### Decision 3: Date Picker Constraints

**Decision**: Use HTML5 `<input type="date">` with `min` and `max` attributes

**Rationale**:
- Native date pickers provide consistent UX across browsers
- `min="1990-01-01"` and `max={today}` prevent invalid selections at UI level
- Keyboard accessibility built-in
- No additional dependencies required

**Implementation**:
```typescript
const today = new Date().toISOString().split('T')[0]
const minDate = "1990-01-01"

<input 
  type="date" 
  min={minDate} 
  max={today}
  value={startDate}
  onChange={handleStartDateChange}
/>
```

**Additional validation** for end date ≥ start date:
```typescript
function validateDateRange(start: string, end: string): string | null {
  if (!start || !end) return "Start and end dates are required"
  if (new Date(end) < new Date(start)) {
    return "End date must be after start date"
  }
  return null
}
```

---

### Decision 4: Accessibility Implementation

**Decision**: Use ARIA live regions (`aria-live="polite"`) + `aria-describedby` + `aria-invalid`

**Rationale**:
- WCAG 2.1 AA compliance requirement
- Polite announcements don't interrupt screen reader users
- `aria-describedby` creates semantic link between input and error
- `aria-invalid` marks fields as erroneous for assistive tech

**Pattern**:
```tsx
<div>
  <label htmlFor="location-input">Location</label>
  <input
    id="location-input"
    aria-invalid={!!error}
    aria-describedby={error ? "location-error" : undefined}
    onBlur={handleBlur}
  />
  {error && (
    <div 
      id="location-error" 
      role="alert" 
      aria-live="polite"
      style={{ color: 'red' }}
    >
      {error}
    </div>
  )}
</div>
```

---

### Decision 5: Error Display Timing

**Decision**: Validate on blur (field exit), not on every keystroke

**Rationale**:
- Prevents frustrating "error while typing" experience
- Aligns with user expectation (wait until they finish)
- Reduces unnecessary validation calls
- Standard form UX pattern

**Exception**: Once error shown, re-validate on each change to provide immediate feedback when correcting

---

### Decision 6: Submit Button State Management

**Decision**: Disable button when any field has validation error

**Rationale**:
- Prevents form submission with invalid data
- Visual indicator of form state
- Matches FR-004, FR-005, FR-013 requirements

**Implementation**:
```typescript
const hasErrors = locationError || dateRangeError
const isFormValid = !hasErrors && location && startDate && endDate

<button disabled={!isFormValid || loading}>
  Submit Query
</button>
```

---

## Best Practices Applied

### 1. React Patterns
- **Controlled components**: All form inputs managed by React state
- **Custom hooks**: Reusable validation logic via `useFormValidation` hook
- **Composition**: Separate validation functions from UI components

### 2. TypeScript Safety
- Strong typing for validation functions
- Error state types: `string | null` (null = no error)
- Date format: ISO 8601 strings (`YYYY-MM-DD`)

### 3. Performance
- Debounce validation on blur (not needed for single blur event)
- Memoize validation functions with `useCallback`
- Avoid unnecessary re-renders with `useMemo` for computed validity

### 4. Accessibility
- All inputs have associated `<label>` elements
- Error messages have `role="alert"`
- Focus management preserved
- Keyboard navigation unaffected

---

## Edge Cases Addressed

1. **Paste behavior**: Trim whitespace before validation
2. **Leading zeros in ZIP**: Allowed (e.g., "00123" is valid format, backend geocoding handles existence)
3. **Rapid field switching**: Each blur triggers validation independently
4. **Browser autofill**: onBlur still triggers after autofill
5. **Empty date picker**: Treated as missing required field

---

## Technology Stack Decisions

| Technology | Choice | Reason |
|------------|--------|--------|
| Form library | None (vanilla React) | Only 3 inputs, custom hooks sufficient |
| Validation library | None (custom functions) | Rules are simple (regex + date comparison) |
| Date picker | HTML5 native | Built-in, accessible, no dependencies |
| CSS framework | None (existing styles.css) | Minimal styling needed for error messages |
| Testing | Manual for MVP | Post-MVP: Vitest + React Testing Library |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Browser compatibility | HTML5 date input supported in all modern browsers; fallback not needed per target platform |
| Accessibility violations | ARIA patterns follow WCAG 2.1 AA guidelines; can be validated with axe DevTools |
| Breaking existing functionality | Validation is additive; existing form submission logic unchanged |
| Over-validation blocking legitimate inputs | Liberal validation (accept both ZIP and city/state); backend still final authority |

---

## Open Questions (None)

All technical decisions resolved during clarification phase. No blocking unknowns remain.
