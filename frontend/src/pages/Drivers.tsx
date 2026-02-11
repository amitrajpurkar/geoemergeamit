import { useEffect, useState } from 'react'

import { DriverTile } from '../components/DriverTile'
import { ErrorConsole } from '../components/ErrorConsole'
import { MultiLayerLegend } from '../components/MultiLayerLegend'
import { fetchDrivers, type DriversResponse } from '../services/api'
import { validateLocation, validateDateRange } from '../utils/validation'

export function Drivers({
  onBack,
  initialQuery
}: {
  onBack: () => void
  initialQuery: { location_text: string; start_date: string; end_date: string } | null
}) {
  const [locationText, setLocationText] = useState(initialQuery?.location_text ?? '33172')
  const [startDate, setStartDate] = useState(initialQuery?.start_date ?? '2023-01-01')
  const [endDate, setEndDate] = useState(initialQuery?.end_date ?? '2024-12-31')
  const [data, setData] = useState<DriversResponse | null>(null)
  const [error, setError] = useState<Error | string | null>(null)
  const [loading, setLoading] = useState(false)
  
  // Validation state
  const [locationError, setLocationError] = useState<string | null>(null)
  const [locationTouched, setLocationTouched] = useState(false)
  const [dateErrors, setDateErrors] = useState<{ start: string | null; end: string | null }>({ 
    start: null, 
    end: null 
  })
  const [dateTouched, setDateTouched] = useState(false)
  
  // Validation handlers
  function handleLocationBlur() {
    setLocationTouched(true)
    const error = validateLocation(locationText)
    setLocationError(error)
  }
  
  function handleDateBlur() {
    setDateTouched(true)
    const errors = validateDateRange(startDate, endDate)
    setDateErrors(errors)
  }
  
  // Compute form validity
  const hasErrors = locationError !== null || dateErrors.start !== null || dateErrors.end !== null
  const canSubmit = !hasErrors && locationText.trim() && startDate && endDate
  
  // Today's date for max attribute
  const today = new Date().toISOString().split('T')[0]

  useEffect(() => {
    let alive = true
    async function load() {
      try {
        setLoading(true)
        setError(null)
        const resp = await fetchDrivers({
          location_text: locationText,
          date_range: startDate && endDate ? { start_date: startDate, end_date: endDate } : undefined
        })
        if (!alive) return
        setData(resp)
      } catch (e) {
        if (!alive) return
        setError(e instanceof Error ? e : String(e))
      } finally {
        if (!alive) return
        setLoading(false)
      }
    }
    load()
    return () => {
      alive = false
    }
  }, [])

  async function onRefresh() {
    // Prevent submission if validation fails
    if (!canSubmit || loading) {
      return
    }
    
    try {
      setLoading(true)
      setError(null)
      const resp = await fetchDrivers({
        location_text: locationText.trim(),
        date_range: startDate && endDate ? { start_date: startDate, end_date: endDate } : undefined
      })
      setData(resp)
    } catch (e) {
      setError(e instanceof Error ? e : String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <button onClick={onBack} style={{ padding: 8 }}>
          Back
        </button>
        <h1 style={{ margin: 0 }}>Environmental Drivers</h1>
      </div>

      <div className="panel" style={{ marginTop: 12 }}>
        <div style={{ display: 'grid', gap: 8, padding: 12 }}>
          <label>
            <div style={{ fontSize: 12, color: '#444' }}>City / ZIP</div>
            <input 
              id="drivers-location-input"
              value={locationText} 
              onChange={(e) => setLocationText(e.target.value)} 
              onBlur={handleLocationBlur}
              disabled={loading} 
              style={{ width: '100%', padding: 8 }}
              aria-invalid={locationError !== null}
              aria-describedby={locationError ? "drivers-location-error" : undefined}
            />
            {locationError && locationTouched && (
              <div 
                id="drivers-location-error" 
                className="error-message"
                role="alert" 
                aria-live="polite"
              >
                {locationError}
              </div>
            )}
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <label>
              <div style={{ fontSize: 12, color: '#444' }}>Start date</div>
              <input 
                id="drivers-start-date-input"
                type="date" 
                value={startDate} 
                onChange={(e) => setStartDate(e.target.value)} 
                onBlur={handleDateBlur}
                disabled={loading} 
                style={{ width: '100%', padding: 8 }}
                min="1990-01-01"
                max={today}
                aria-invalid={dateErrors.start !== null}
                aria-describedby={dateErrors.start ? "drivers-start-date-error" : undefined}
              />
              {dateErrors.start && dateTouched && (
                <div 
                  id="drivers-start-date-error" 
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
                id="drivers-end-date-input"
                type="date" 
                value={endDate} 
                onChange={(e) => setEndDate(e.target.value)} 
                onBlur={handleDateBlur}
                disabled={loading} 
                style={{ width: '100%', padding: 8 }}
                min="1990-01-01"
                max={today}
                aria-invalid={dateErrors.end !== null}
                aria-describedby={dateErrors.end ? "drivers-end-date-error" : undefined}
              />
              {dateErrors.end && dateTouched && (
                <div 
                  id="drivers-end-date-error" 
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
            onClick={onRefresh} 
            disabled={!canSubmit || loading} 
            style={{ padding: 10 }}
            title={!canSubmit && !loading ? "Please fix validation errors" : undefined}
          >
            Refresh
          </button>
        </div>
      </div>

      <ErrorConsole error={error} />

      {data?.tiles ? <MultiLayerLegend layers={data.tiles} /> : null}

      <div className="grid" style={{ marginTop: 12 }}>
        {data?.tiles?.map((t) => (
          <DriverTile key={t.driver_type} tile={t} viewport={data.viewport ?? null} />
        ))}
      </div>
    </div>
  )
}
