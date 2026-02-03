import { useEffect, useState } from 'react'

import { RiskLegend } from '../components/RiskLegend'
import { RiskMap } from '../components/RiskMap'
import { fetchDefaultRisk, type RiskLayerResponse } from '../services/api'

export function Home() {
  const [month, setMonth] = useState<RiskLayerResponse | null>(null)
  const [year, setYear] = useState<RiskLayerResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let alive = true

    async function load() {
      try {
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
      }
    }

    load()
    return () => {
      alive = false
    }
  }, [])

  const legend = month?.legend ?? year?.legend ?? []

  return (
    <div>
      <h1 style={{ margin: '0 0 8px 0' }}>Mosquito Risk Dashboard</h1>
      <p style={{ marginTop: 0, color: '#444' }}>
        Default risk overlays for Florida: last 30 days and last 12 months.
      </p>

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
