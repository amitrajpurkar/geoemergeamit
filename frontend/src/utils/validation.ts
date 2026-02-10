// Client-side validation utilities for input validation feature
// Feature: 003-input-validation

// ============================================================================
// TypeScript Types
// ============================================================================

export type ValidationError = {
  message: string
  fieldId: string
  timestamp: number
}

export type FieldState = {
  value: string
  error: string | null
  touched: boolean
  validating: boolean
}

export type FormState = {
  fields: Map<string, FieldState>
  isSubmitting: boolean
  hasBeenTouched: boolean
}

// ============================================================================
// Validation Functions
// ============================================================================

/**
 * Validates location input format (ZIP code or city/state text)
 * @param value - Location input string
 * @returns Error message or null if valid
 */
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

/**
 * Validates date range with constraints (1990-present, end >= start)
 * @param startDate - Start date in ISO format (YYYY-MM-DD)
 * @param endDate - End date in ISO format (YYYY-MM-DD)
 * @returns Object with start and end error messages (null if valid)
 */
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
