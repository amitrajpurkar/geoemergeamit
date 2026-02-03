import { useEffect, useState } from 'react'

import { RiskLegend } from '../components/RiskLegend'
import { RiskMap } from '../components/RiskMap'
import { RiskQueryForm, type RiskQuery } from '../components/RiskQueryForm'
import { fetchDefaultRisk, fetchRiskQuery, type RiskLayerResponse } from '../services/api'

export function Home() {
  const [month, setMonth] = useState<RiskLayerResponse | null>(null)
  const [year, setYear] = useState<RiskLayerResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let alive = true

    async function load() {
      try {
        setLoading(true)
        setError(null)
        const [m, y] = await Promise.all([
          fetchDefaultRisk('last_30_days'),
          fetchDefaultRisk('last_12_months')
        ])
        if (!alive) return
        setMonth(m)
        setYear(y)
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

  async function onQuery(q: RiskQuery) {
    if (!q.location_text.trim()) {
      setError('Location is required')
      return
    }
    if (!q.start_date || !q.end_date) {
      setError('Start and end date are required')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const layer = await fetchRiskQuery({
        location_text: q.location_text,
        date_range: { start_date: q.start_date, end_date: q.end_date }
      })
      setMonth(layer)
      setYear(layer)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load')
    } finally {
      setLoading(false)
    }
  }

  const legend = month?.legend ?? year?.legend ?? []

  return (
    <div>
      <h1 style={{ margin: '0 0 8px 0' }}>Mosquito Risk Dashboard</h1>
      <p style={{ marginTop: 0, color: '#444' }}>
        Default risk overlays for Florida: last 30 days and last 12 months.
      </p>

      <RiskQueryForm onSubmit={onQuery} disabled={loading} />

      {error ? <div className="error">{error}</div> : null}

      {legend.length ? <RiskLegend legend={legend} /> : null}

      <div className="grid" style={{ marginTop: 12 }}>
        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title">Florida - Last 30 days</h2>
          </div>
          {month ? <RiskMap layer={month} /> : <div style={{ padding: 12 }}>Loading…</div>}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title">Florida - Last 12 months</h2>
          </div>
          {year ? <RiskMap layer={year} /> : <div style={{ padding: 12 }}>Loading…</div>}
        </div>
      </div>
    </div>
  )
}
