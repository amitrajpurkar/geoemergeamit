import type { FormEvent } from 'react'
import { useState } from 'react'

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
  const [locationText, setLocationText] = useState('Miami, FL')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  function submit(e: FormEvent) {
    e.preventDefault()
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
            value={locationText}
            onChange={(e) => setLocationText(e.target.value)}
            placeholder="Miami, FL or 33301"
            disabled={disabled}
            style={{ width: '100%', padding: 8 }}
          />
        </label>

        <div style={{ display: 'grid', gap: 8, gridTemplateColumns: '1fr 1fr' }}>
          <label>
            <div style={{ fontSize: 12, color: '#444' }}>Start date</div>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              disabled={disabled}
              style={{ width: '100%', padding: 8 }}
            />
          </label>

          <label>
            <div style={{ fontSize: 12, color: '#444' }}>End date</div>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              disabled={disabled}
              style={{ width: '100%', padding: 8 }}
            />
          </label>
        </div>

        <button type="submit" disabled={disabled} style={{ padding: 10 }}>
          Update overlays
        </button>
      </div>
    </form>
  )
}
