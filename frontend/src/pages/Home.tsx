import { useEffect, useState } from 'react'

import { ErrorConsole } from '../components/ErrorConsole'
import { RiskLegend } from '../components/RiskLegend'
import { RiskMap } from '../components/RiskMap'
import { RiskQueryForm, type RiskQuery } from '../components/RiskQueryForm'
import { fetchDefaultRisk, fetchRiskQuery, type OverlayLayer, type RiskLayerResponse } from '../services/api'

export function Home({
  onOpenDrivers,
  onQuerySuccess
}: {
  onOpenDrivers: () => void
  onQuerySuccess: (q: { location_text: string; start_date: string; end_date: string }) => void
}) {
  const [month, setMonth] = useState<RiskLayerResponse | null>(null)
  const [year, setYear] = useState<RiskLayerResponse | null>(null)
  const [error, setError] = useState<Error | string | null>(null)
  const [loading, setLoading] = useState(false)
  const [monthLayerId, setMonthLayerId] = useState('risk')
  const [yearLayerId, setYearLayerId] = useState('risk')
  const [mode, setMode] = useState<'default' | 'query'>('default')

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
        setMode('default')
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
      setMonthLayerId('risk')
      setYearLayerId('risk')
      setMode('query')
      onQuerySuccess({ location_text: q.location_text, start_date: q.start_date, end_date: q.end_date })
    } catch (e) {
      setError(e instanceof Error ? e : String(e))
    } finally {
      setLoading(false)
    }
  }

  const legend = month?.legend ?? year?.legend ?? []

  function pickLayer(resp: RiskLayerResponse | null, layerId: string): OverlayLayer | null {
    const layers = resp?.layers ?? []
    return layers.find((l) => l.layer_id === layerId) ?? (layers.length ? layers[0] : null)
  }

  const monthOverlay = pickLayer(month, monthLayerId)
  const yearOverlay = pickLayer(year, yearLayerId)

  const monthTitle =
    mode === 'query' && month
      ? `${month.location_label}  -  ${month.date_range.start_date} to ${month.date_range.end_date}`
      : 'Florida - Last 30 days'

  const yearTitle =
    mode === 'query' && year
      ? `${year.location_label}  -  ${year.date_range.start_date} to ${year.date_range.end_date}`
      : 'Florida - Last 12 months'

  return (
    <div>
      <h1 style={{ margin: '0 0 8px 0' }}>Mosquito Risk Dashboard</h1>
      <p style={{ marginTop: 0, color: '#444' }}>
        Default risk overlays for Florida: last 30 days and last 12 months.
      </p>

      <button onClick={onOpenDrivers} style={{ padding: 8, marginBottom: 12 }} disabled={loading}>
        View environmental drivers
      </button>

      <RiskQueryForm onSubmit={onQuery} disabled={loading} />

      <ErrorConsole error={error} />

      {legend.length ? <RiskLegend legend={legend} /> : null}

      <div className="grid" style={{ marginTop: 12 }}>
        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title">{monthTitle}</h2>
            {month?.layers?.length ? (
              <select value={monthLayerId} onChange={(e) => setMonthLayerId(e.target.value)} disabled={loading}>
                {month.layers.map((l) => (
                  <option key={l.layer_id} value={l.layer_id}>
                    {l.label}
                  </option>
                ))}
              </select>
            ) : null}
          </div>
          {month && monthOverlay ? (
            <RiskMap layer={month} overlayUrl={monthOverlay.tile_url_template} overlayAttribution={monthOverlay.attribution} />
          ) : (
            <div style={{ padding: 12 }}>Loading…</div>
          )}
        </div>

        <div className="panel">
          <div className="panel-header">
            <h2 className="panel-title">{yearTitle}</h2>
            {year?.layers?.length ? (
              <select value={yearLayerId} onChange={(e) => setYearLayerId(e.target.value)} disabled={loading}>
                {year.layers.map((l) => (
                  <option key={l.layer_id} value={l.layer_id}>
                    {l.label}
                  </option>
                ))}
              </select>
            ) : null}
          </div>
          {year && yearOverlay ? (
            <RiskMap layer={year} overlayUrl={yearOverlay.tile_url_template} overlayAttribution={yearOverlay.attribution} />
          ) : (
            <div style={{ padding: 12 }}>Loading…</div>
          )}
        </div>
      </div>
    </div>
  )
}
