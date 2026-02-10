import type { FormEvent } from 'react'
import { useState } from 'react'
import { validateLocation, validateDateRange } from '../utils/validation'

export type RiskQuery = {
  location_text: string
  start_date: string
  end_date: string
}

export function RiskQueryForm({
  onSubmit,
  disabled
}: {
  onSubmit: (q: RiskQuery) => void
  disabled?: boolean
}) {
  const [locationText, setLocationText] = useState('33172')
  const [startDate, setStartDate] = useState('2023-01-01')
  const [endDate, setEndDate] = useState('2024-12-31')
  
  // Validation state (T008, T015)
  const [locationError, setLocationError] = useState<string | null>(null)
  const [locationTouched, setLocationTouched] = useState(false)
  const [dateErrors, setDateErrors] = useState<{ start: string | null; end: string | null }>({ 
    start: null, 
    end: null 
  })
  const [dateTouched, setDateTouched] = useState(false)

  // Location blur handler (T009)
  function handleLocationBlur() {
    setLocationTouched(true)
    const error = validateLocation(locationText)
    setLocationError(error)
  }
  
  // Date blur handler (T018)
  function handleDateBlur() {
    setDateTouched(true)
    const errors = validateDateRange(startDate, endDate)
    setDateErrors(errors)
  }
  
  // Compute form validity (T012, T021)
  const hasErrors = locationError !== null || dateErrors.start !== null || dateErrors.end !== null
  const canSubmit = !hasErrors && locationText.trim() && startDate && endDate
  
  // Compute today's date for max attribute (T016, T017)
  const today = new Date().toISOString().split('T')[0]
  
  function submit(e: FormEvent) {
    e.preventDefault()
    
    // Prevent submission if validation fails (T013)
    if (!canSubmit || disabled) {
      return
    }
    
    onSubmit({ location_text: locationText.trim(), start_date: startDate, end_date: endDate })
  }

  return (
    <form onSubmit={submit} className="panel" style={{ marginBottom: 12 }}>
      <div className="panel-header">
        <h2 className="panel-title">Explore by location</h2>
      </div>

      <div style={{ display: 'grid', gap: 8, padding: 12 }}>
        <label>
          <div style={{ fontSize: 12, color: '#444' }}>City / ZIP</div>
          <input
            id="location-input"
            value={locationText}
            onChange={(e) => setLocationText(e.target.value)}
            onBlur={handleLocationBlur}
            placeholder="Miami, FL or 33301"
            disabled={disabled}
            style={{ width: '100%', padding: 8 }}
            aria-invalid={locationError !== null}
            aria-describedby={locationError ? "location-error" : undefined}
          />
          {locationError && locationTouched && (
            <div 
              id="location-error" 
              className="error-message"
              role="alert" 
              aria-live="polite"
            >
              {locationError}
            </div>
          )}
        </label>

        <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
          <label>
            <div style={{ fontSize: 12, color: '#444' }}>Start date</div>
            <input
              id="start-date-input"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              onBlur={handleDateBlur}
              disabled={disabled}
              style={{ width: '100%', padding: 8 }}
              min="1990-01-01"
              max={today}
              aria-invalid={dateErrors.start !== null}
              aria-describedby={dateErrors.start ? "start-date-error" : undefined}
            />
            {dateErrors.start && dateTouched && (
              <div 
                id="start-date-error" 
                className="error-message"
                role="alert" 
                aria-live="polite"
              >
                {dateErrors.start}
              </div>
            )}
          </label>

          <label>
            <div style={{ fontSize: 12, color: '#444' }}>End date</div>
            <input
              id="end-date-input"
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              onBlur={handleDateBlur}
              disabled={disabled}
              style={{ width: '100%', padding: 8 }}
              min="1990-01-01"
              max={today}
              aria-invalid={dateErrors.end !== null}
              aria-describedby={dateErrors.end ? "end-date-error" : undefined}
            />
            {dateErrors.end && dateTouched && (
              <div 
                id="end-date-error" 
                className="error-message"
                role="alert" 
                aria-live="polite"
              >
                {dateErrors.end}
              </div>
            )}
          </label>
        </div>

        <button 
          type="submit" 
          disabled={!canSubmit || disabled} 
          style={{ padding: 10 }}
          title={!canSubmit && !disabled ? "Please fix validation errors" : undefined}
        >
          Update overlays
        </button>
      </div>
    </form>
  )
}
