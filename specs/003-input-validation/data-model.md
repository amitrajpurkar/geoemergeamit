# Data Model: Client-Side Input Validation

**Feature**: 003-input-validation  
**Date**: February 10, 2026  
**Phase**: 1 - Data & Entity Design

## Overview

This feature introduces client-side form state entities for validation. No backend data model changes are required. All entities exist only in React component state during user interaction.

---

## Entity Definitions

### 1. ValidationError

**Purpose**: Represents a single validation failure for a form field

**Attributes**:
- `message`: string - Human-readable error message displayed to user
- `fieldId`: string - Identifier of the input field (e.g., "location", "startDate", "endDate")
- `timestamp`: number - When error was created (for debugging)

**Lifecycle**:
- Created: When validation rule fails on blur event
- Updated: When user corrects input and validation re-runs
- Destroyed: When field becomes valid or component unmounts

**Example**:
```typescript
type ValidationError = {
  message: string
  fieldId: string
  timestamp: number
}

// Example instance
{
  message: "Enter a 5-digit ZIP code or city/state name",
  fieldId: "location",
  timestamp: 1707594123456
}
```

---

### 2. FormState

**Purpose**: Aggregates validation status and controls form submission

**Attributes**:
- `fields`: Map<string, FieldState> - Validation state for each input
- `isSubmitting`: boolean - Whether form submission is in progress
- `hasBeenTouched`: boolean - Whether user has interacted with form

**Derived Properties** (computed, not stored):
- `isValid`: boolean - True if all fields have no errors and required fields are filled
- `errors`: ValidationError[] - List of current validation errors
- `canSubmit`: boolean - True if isValid and not isSubmitting

**Lifecycle**:
- Created: When form component mounts
- Updated: On every user interaction (input change, blur, focus)
- Destroyed: When form component unmounts

**Example**:
```typescript
type FormState = {
  fields: Map<string, FieldState>
  isSubmitting: boolean
  hasBeenTouched: boolean
}

// Example instance
{
  fields: new Map([
    ["location", { value: "33172", error: null, touched: true }],
    ["startDate", { value: "2023-01-01", error: null, touched: true }],
    ["endDate", { value: "2024-12-31", error: null, touched: true }]
  ]),
  isSubmitting: false,
  hasBeenTouched: true
}
```

---

### 3. FieldState

**Purpose**: Tracks individual input field state and validation

**Attributes**:
- `value`: string - Current input value
- `error`: string | null - Current validation error (null if valid)
- `touched`: boolean - Whether user has interacted with this field (blur event occurred)
- `validating`: boolean - Whether async validation is in progress (not used in MVP)

**Validation Rules by Field**:

**location**:
- Required: Yes
- Format: 5-digit ZIP OR text with letters/spaces/commas
- Trimming: Yes (leading/trailing whitespace)

**startDate**:
- Required: Yes
- Format: ISO 8601 date (YYYY-MM-DD)
- Range: 1990-01-01 to today
- Constraint: Must be ≤ endDate

**endDate**:
- Required: Yes
- Format: ISO 8601 date (YYYY-MM-DD)
- Range: 1990-01-01 to today
- Constraint: Must be ≥ startDate

**Example**:
```typescript
type FieldState = {
  value: string
  error: string | null
  touched: boolean
  validating: boolean
}

// Valid field
{
  value: "Miami, FL",
  error: null,
  touched: true,
  validating: false
}

// Invalid field
{
  value: "123",
  error: "Enter a 5-digit ZIP code or city/state name",
  touched: true,
  validating: false
}
```

---

## Entity Relationships

```
FormState
  ├── fields: Map<fieldId, FieldState>
  │     ├── "location" → FieldState
  │     │     └── error → ValidationError | null
  │     ├── "startDate" → FieldState
  │     │     └── error → ValidationError | null
  │     └── "endDate" → FieldState
  │           └── error → ValidationError | null
  └── (computed) isValid: boolean
```

**Relationship Rules**:
- FormState aggregates multiple FieldState entities (1-to-many)
- Each FieldState may have zero or one ValidationError
- FormState.isValid is derived from all FieldState.error values

---

## State Transitions

### FieldState Transitions

```
┌─────────────┐
│   Pristine  │ (initial, not touched)
│  error: null│
└──────┬──────┘
       │ User focuses field
       │ User types
       │ User exits field (blur)
       ▼
┌─────────────┐
│   Touched   │
│  validating │
└──────┬──────┘
       │ Validation runs
       ├─────────────┬─────────────┐
       ▼             ▼             ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│  Valid   │   │ Invalid  │   │  Valid   │
│error:null│   │error:msg │   │error:null│
└────┬─────┘   └────┬─────┘   └────┬─────┘
     │              │              │
     │              │ User corrects input
     │              └──────────────┘
     │ User changes valid input
     └───────────────────────────────┐
                                     ▼
                              (back to Touched)
```

### FormState Transitions

```
┌──────────────┐
│    Empty     │ (initial state)
│ canSubmit=NO │
└──────┬───────┘
       │ User enters data
       ▼
┌──────────────┐
│   Partial    │ (some fields filled)
│ canSubmit=NO │
└──────┬───────┘
       │ All required fields filled
       │ All validations pass
       ▼
┌──────────────┐
│    Valid     │
│ canSubmit=YES│
└──────┬───────┘
       │ User clicks submit
       ▼
┌──────────────┐
│  Submitting  │
│ canSubmit=NO │ (disabled)
└──────┬───────┘
       │ API response
       ▼
┌──────────────┐
│   Complete   │ (success) → navigate/refresh
│  or Error    │ (failure) → show error, back to Valid
└──────────────┘
```

---

## Validation Logic

### Location Validation Function

```typescript
function validateLocation(value: string): string | null {
  const trimmed = value.trim()
  
  // Rule 1: Required
  if (!trimmed) {
    return "Location is required"
  }
  
  // Rule 2: If numeric, must be exactly 5 digits
  if (/^\d+$/.test(trimmed)) {
    if (trimmed.length !== 5) {
      return "Enter a 5-digit ZIP code or city/state name"
    }
    return null // Valid ZIP
  }
  
  // Rule 3: If not numeric, must contain valid city/state characters
  if (/^[a-zA-Z\s,.-]+$/.test(trimmed)) {
    return null // Valid city/state
  }
  
  // Rule 4: Invalid characters
  return "Enter a 5-digit ZIP code or city/state name"
}
```

### Date Range Validation Function

```typescript
function validateDateRange(
  startDate: string, 
  endDate: string
): { start: string | null; end: string | null } {
  const today = new Date().toISOString().split('T')[0]
  const minDate = "1990-01-01"
  
  let startError: string | null = null
  let endError: string | null = null
  
  // Rule 1: Required
  if (!startDate) startError = "Start date is required"
  if (!endDate) endError = "End date is required"
  
  if (startDate && endDate) {
    // Rule 2: Range constraints
    if (startDate < minDate) {
      startError = "Start date must be after 1990-01-01"
    }
    if (startDate > today) {
      startError = "Start date cannot be in the future"
    }
    if (endDate < minDate) {
      endError = "End date must be after 1990-01-01"
    }
    if (endDate > today) {
      endError = "End date cannot be in the future"
    }
    
    // Rule 3: Logical ordering
    if (startDate > endDate) {
      endError = "End date must be after start date"
    }
  }
  
  return { start: startError, end: endError }
}
```

---

## Persistence & Storage

**Storage**: None. All validation state is ephemeral (React component state only).

**Rationale**: Validation state is transient UI feedback. No need to persist. Form values themselves are submitted to backend via existing API endpoints, but validation state is discarded after submission.

---

## Data Flow

```
User Input → Field State Update → Blur Event → Validation Function
                                                      │
                                                      ▼
                                           ValidationError created
                                                      │
                                                      ▼
                                           FormState updated
                                                      │
                                                      ▼
                                           UI Re-renders
                                           - Error message displayed
                                           - ARIA attributes updated
                                           - Submit button disabled
```

---

## Notes

- **No backend changes**: This feature is entirely frontend validation. Backend validation remains as-is.
- **No new API contracts**: Existing `/api/risk/query` and `/api/drivers` endpoints unchanged.
- **No database schema**: No persistent data.
- **TypeScript types**: All entities defined as TypeScript types/interfaces in frontend code.
