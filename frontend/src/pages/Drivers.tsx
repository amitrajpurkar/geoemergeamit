import { useEffect, useState } from 'react'

import { DriverTile } from '../components/DriverTile'
import { fetchDrivers, type DriversResponse } from '../services/api'

export function Drivers({
  onBack,
  initialQuery
}: {
  onBack: () => void
  initialQuery: { location_text: string; start_date: string; end_date: string } | null
}) {
  const [locationText, setLocationText] = useState(initialQuery?.location_text ?? 'Miami, FL')
  const [startDate, setStartDate] = useState(initialQuery?.start_date ?? '')
  const [endDate, setEndDate] = useState(initialQuery?.end_date ?? '')
  const [data, setData] = useState<DriversResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

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
        setError(e instanceof Error ? e.message : 'Failed to load')
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
    try {
      setLoading(true)
      setError(null)
      const resp = await fetchDrivers({
        location_text: locationText,
        date_range: startDate && endDate ? { start_date: startDate, end_date: endDate } : undefined
      })
      setData(resp)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load')
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
            <input value={locationText} onChange={(e) => setLocationText(e.target.value)} disabled={loading} style={{ width: '100%', padding: 8 }} />
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            <label>
              <div style={{ fontSize: 12, color: '#444' }}>Start date</div>
              <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} disabled={loading} style={{ width: '100%', padding: 8 }} />
            </label>
            <label>
              <div style={{ fontSize: 12, color: '#444' }}>End date</div>
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} disabled={loading} style={{ width: '100%', padding: 8 }} />
            </label>
          </div>
          <button onClick={onRefresh} disabled={loading} style={{ padding: 10 }}>
            Refresh
          </button>
        </div>
      </div>

      {error ? <div className="error">{error}</div> : null}

      <div className="grid" style={{ marginTop: 12 }}>
        {data?.tiles?.map((t) => (
          <DriverTile key={t.driver_type} tile={t} viewport={data.viewport ?? null} />
        ))}
      </div>
    </div>
  )
}
