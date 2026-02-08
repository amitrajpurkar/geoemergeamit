import { useEffect, useState } from 'react'

import { ErrorConsole } from '../components/ErrorConsole'
import { MultiLayerLegend } from '../components/MultiLayerLegend'
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
  const [riskData, setRiskData] = useState<RiskLayerResponse | null>(null)
  const [error, setError] = useState<Error | string | null>(null)
  const [loading, setLoading] = useState(false)
  const [layerId, setLayerId] = useState('risk')
  const [mode, setMode] = useState<'default' | 'query'>('default')

  useEffect(() => {
    let alive = true

    async function load() {
      try {
        setLoading(true)
        setError(null)
        const data = await fetchDefaultRisk()
        if (!alive) return
        setRiskData(data)
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
      setRiskData(layer)
      setLayerId('risk')
      setMode('query')
      onQuerySuccess({ location_text: q.location_text, start_date: q.start_date, end_date: q.end_date })
    } catch (e) {
      setError(e instanceof Error ? e : String(e))
    } finally {
      setLoading(false)
    }
  }

  function pickLayer(resp: RiskLayerResponse | null, layerId: string): OverlayLayer | null {
    const layers = resp?.layers ?? []
    return layers.find((l) => l.layer_id === layerId) ?? (layers.length ? layers[0] : null)
  }

  const overlay = pickLayer(riskData, layerId)

  const mapTitle = riskData
    ? `${riskData.location_label}  -  ${riskData.date_range.start_date} to ${riskData.date_range.end_date}`
    : 'Loading...'

  return (
    <div>
      <h1 style={{ margin: '0 0 8px 0' }}>Mosquito Risk Dashboard</h1>
      <p style={{ marginTop: 0, color: '#444' }}>
        Default location: ZIP 33172 (2023-01-01 to 2024-12-31)
      </p>

      <button onClick={onOpenDrivers} style={{ padding: 8, marginBottom: 12 }} disabled={loading}>
        View environmental drivers
      </button>

      <RiskQueryForm onSubmit={onQuery} disabled={loading} />

      <ErrorConsole error={error} />

      {riskData?.layers ? <MultiLayerLegend layers={riskData.layers} /> : null}

      <div className="panel" style={{ marginTop: 12 }}>
        <div className="panel-header">
          <h2 className="panel-title">{mapTitle}</h2>
          {riskData?.layers?.length ? (
            <select value={layerId} onChange={(e) => setLayerId(e.target.value)} disabled={loading}>
              {riskData.layers.map((l) => (
                <option key={l.layer_id} value={l.layer_id}>
                  {l.label}
                </option>
              ))}
            </select>
          ) : null}
        </div>
        {riskData && overlay ? (
          <RiskMap layer={riskData} overlayUrl={overlay.tile_url_template} overlayAttribution={overlay.attribution} />
        ) : (
          <div style={{ padding: 12 }}>Loading…</div>
        )}
      </div>
    </div>
  )
}
