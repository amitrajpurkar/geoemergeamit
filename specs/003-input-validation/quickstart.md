# Quickstart: Client-Side Input Validation

**Feature**: 003-input-validation  
**Date**: February 10, 2026  
**Phase**: 1 - Integration & Testing Guide

## Overview

This guide provides step-by-step instructions for implementing and testing the client-side input validation feature. Follow these steps to integrate validation into the Home and Drivers pages.

---

## Prerequisites

- Node.js and npm installed
- Repository cloned and on branch `003-input-validation`
- Backend running (for end-to-end testing)

---

## Implementation Steps

### Step 1: Create Validation Utility Functions

**File**: `frontend/src/utils/validation.ts`

**Purpose**: Pure functions for validation logic, no React dependencies

**Implementation**:
```typescript
// frontend/src/utils/validation.ts

export function validateLocation(value: string): string | null {
  const trimmed = value.trim()
  
  if (!trimmed) {
    return "Location is required"
  }
  
  // If numeric, must be exactly 5 digits (ZIP code)
  if (/^\d+$/.test(trimmed)) {
    return trimmed.length === 5 
      ? null 
      : "Enter a 5-digit ZIP code or city/state name"
  }
  
  // If text, must contain valid city/state characters
  if (/^[a-zA-Z\s,.-]+$/.test(trimmed)) {
    return null
  }
  
  return "Enter a 5-digit ZIP code or city/state name"
}

export function validateDateRange(
  startDate: string,
  endDate: string
): { start: string | null; end: string | null } {
  const today = new Date().toISOString().split('T')[0]
  const minDate = "1990-01-01"
  
  let startError: string | null = null
  let endError: string | null = null
  
  if (!startDate) startError = "Start date is required"
  if (!endDate) endError = "End date is required"
  
  if (startDate && endDate) {
    if (startDate < minDate) startError = "Start date must be after 1990-01-01"
    if (startDate > today) startError = "Start date cannot be in the future"
    if (endDate < minDate) endError = "End date must be after 1990-01-01"
    if (endDate > today) endError = "End date cannot be in the future"
    if (startDate > endDate) endError = "End date must be after start date"
  }
  
  return { start: startError, end: endError }
}
```

**Test**: Create test file to verify validation logic (optional for MVP)

---

### Step 2: Update RiskQueryForm Component

**File**: `frontend/src/components/RiskQueryForm.tsx`

**Changes**:
1. Add validation state for each field
2. Add blur event handlers
3. Display inline error messages
4. Disable submit button when validation fails
5. Add ARIA attributes for accessibility

**Key Changes**:
```typescript
// Add state for validation errors
const [locationError, setLocationError] = useState<string | null>(null)
const [dateErrors, setDateErrors] = useState<{ start: string | null; end: string | null }>({ 
  start: null, 
  end: null 
})

// Validation on blur
const handleLocationBlur = () => {
  const error = validateLocation(locationText)
  setLocationError(error)
}

const handleDateBlur = () => {
  const errors = validateDateRange(startDate, endDate)
  setDateErrors(errors)
}

// Compute form validity
const hasErrors = locationError || dateErrors.start || dateErrors.end
const canSubmit = !hasErrors && locationText && startDate && endDate

// Update JSX
<input
  value={locationText}
  onChange={(e) => setLocationText(e.target.value)}
  onBlur={handleLocationBlur}
  disabled={disabled}
  aria-invalid={!!locationError}
  aria-describedby={locationError ? "location-error" : undefined}
/>
{locationError && (
  <div id="location-error" role="alert" aria-live="polite" style={{ color: 'red', fontSize: 12 }}>
    {locationError}
  </div>
)}

<button onClick={handleSubmit} disabled={!canSubmit || disabled}>
  Submit
</button>
```

---

### Step 3: Update Home.tsx

**File**: `frontend/src/pages/Home.tsx`

**Changes**:
- Pass validation-enabled form component
- No structural changes needed (validation is within RiskQueryForm)

**Verification**: Ensure RiskQueryForm import is correct

---

### Step 4: Update Drivers.tsx

**File**: `frontend/src/pages/Drivers.tsx`

**Changes**:
- Apply same validation logic to date inputs
- Add validation for location field
- Add ARIA attributes

**Pattern**: Similar to Home.tsx, integrate validation into the form inputs

---

### Step 5: Add Error Styling

**File**: `frontend/src/styles.css`

**Add**:
```css
/* Validation error messages */
.error-message {
  color: #d32f2f;
  font-size: 12px;
  margin-top: 4px;
  margin-bottom: 8px;
}

/* Invalid input field border */
input[aria-invalid="true"] {
  border-color: #d32f2f;
  border-width: 2px;
}

/* Disabled submit button */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #ccc;
}
```

---

## Manual Testing Checklist

### Test Scenario 1: Location Validation (Home Page)

**Steps**:
1. Navigate to http://127.0.0.1:5173
2. Clear location field, click submit → **Expect**: "Location is required" error
3. Enter "123" (3 digits), blur → **Expect**: "Enter a 5-digit ZIP code or city/state name" error
4. Enter "123456" (6 digits), blur → **Expect**: "Enter a 5-digit ZIP code or city/state name" error
5. Enter "33-172" (special chars), blur → **Expect**: "Enter a 5-digit ZIP code or city/state name" error
6. Enter "33172" (valid ZIP), blur → **Expect**: No error, submit button enabled
7. Enter "Miami, FL" (city/state), blur → **Expect**: No error, submit button enabled

**Pass Criteria**: All validation messages appear correctly, submit button state changes appropriately

---

### Test Scenario 2: Date Range Validation (Home Page)

**Steps**:
1. Leave start date empty, blur → **Expect**: "Start date is required" error
2. Leave end date empty, blur → **Expect**: "End date is required" error
3. Select start date: 2024-01-15
4. Select end date: 2024-01-10 (before start), blur → **Expect**: "End date must be after start date" error
5. Select end date: 2024-01-20 (after start), blur → **Expect**: No error
6. Attempt to select future date → **Expect**: Date picker prevents selection (grayed out)
7. Attempt to select date before 1990-01-01 → **Expect**: Date picker prevents selection

**Pass Criteria**: All date validations work, date picker constraints enforced

---

### Test Scenario 3: Submit Button State

**Steps**:
1. Start with empty form → **Expect**: Submit button disabled
2. Fill location only → **Expect**: Submit button still disabled
3. Fill all fields with valid data → **Expect**: Submit button enabled
4. Change location to invalid (e.g., "123"), blur → **Expect**: Submit button disabled again
5. Correct location to valid, blur → **Expect**: Submit button enabled

**Pass Criteria**: Button state always reflects form validity

---

### Test Scenario 4: Accessibility (Screen Reader)

**Tools**: Browser DevTools Accessibility Inspector, axe DevTools extension

**Steps**:
1. Inspect location input with error → **Verify**: `aria-invalid="true"` present
2. Inspect error message div → **Verify**: `role="alert"` and `aria-live="polite"` present
3. Tab through form with keyboard → **Verify**: Focus order logical, all interactive elements reachable
4. Trigger error → **Verify**: Error announced by screen reader (test with NVDA/JAWS/VoiceOver)

**Pass Criteria**: All ARIA attributes correct, keyboard navigation works, screen reader announces errors

---

### Test Scenario 5: Drivers Page Consistency

**Steps**:
1. Navigate to http://127.0.0.1:5173, click "View environmental drivers"
2. Repeat location validation tests from Scenario 1
3. Repeat date validation tests from Scenario 2
4. Verify validation behavior identical to Home page

**Pass Criteria**: Validation works identically on both pages

---

### Test Scenario 6: Edge Cases

**Steps**:
1. Paste "ZIP: 33172" into location field → **Expect**: Error (invalid characters)
2. Enter "  33172  " (with spaces), blur → **Expect**: No error (whitespace trimmed)
3. Use browser autofill for location → **Expect**: Validation runs on blur after autofill
4. Rapidly switch between fields → **Expect**: Each validation runs independently, no conflicts

**Pass Criteria**: Edge cases handled gracefully

---

## Validation Rules Summary

### Location Field
| Input | Valid? | Error Message |
|-------|--------|---------------|
| (empty) | ❌ | "Location is required" |
| "123" | ❌ | "Enter a 5-digit ZIP code or city/state name" |
| "123456" | ❌ | "Enter a 5-digit ZIP code or city/state name" |
| "33-172" | ❌ | "Enter a 5-digit ZIP code or city/state name" |
| "ABC12" | ❌ | "Enter a 5-digit ZIP code or city/state name" |
| "33172" | ✅ | - |
| "Miami" | ✅ | - |
| "Miami, FL" | ✅ | - |
| "Los Angeles" | ✅ | - |

### Date Fields
| Start Date | End Date | Valid? | Error Message |
|------------|----------|--------|---------------|
| (empty) | 2024-12-31 | ❌ | "Start date is required" |
| 2024-01-01 | (empty) | ❌ | "End date is required" |
| 2024-01-15 | 2024-01-10 | ❌ | "End date must be after start date" |
| 2024-01-10 | 2024-01-15 | ✅ | - |
| 1989-12-31 | 2024-01-15 | ❌ | "Start date must be after 1990-01-01" |
| 2024-01-10 | 2027-01-15 | ❌ | "End date cannot be in the future" |

---

## Rollback Plan

If validation causes issues:

1. **Revert validation logic**: Remove validation functions from `RiskQueryForm`
2. **Remove error displays**: Delete error message JSX
3. **Re-enable submit button**: Remove `disabled={!canSubmit}` logic
4. **Keep ARIA attributes**: They don't break functionality even without validation

---

## Success Metrics

After deployment, monitor:
- **Backend error rate**: Should decrease by 95%+ for invalid location/date errors
- **Form submission success rate**: Should increase by 30%+ (fewer retry attempts)
- **User feedback**: Check for complaints about validation being too strict/lenient

---

## Troubleshooting

### Issue: Validation not triggering
**Solution**: Verify `onBlur` handlers are attached to inputs

### Issue: Submit button always disabled
**Solution**: Check validation logic isn't producing false errors; log `canSubmit` value

### Issue: ARIA announcements not working
**Solution**: Verify error divs have `role="alert"` and `aria-live="polite"`; test in different browsers

### Issue: Date picker not restricting dates
**Solution**: Verify `min` and `max` attributes set correctly on `<input type="date">`

---

## Next Steps

After MVP validation:
1. Add unit tests for validation functions
2. Add E2E tests with Playwright
3. Consider extracting reusable validation hook (`useFormValidation`)
4. Add debouncing for real-time validation (User Story 3 enhancement)
