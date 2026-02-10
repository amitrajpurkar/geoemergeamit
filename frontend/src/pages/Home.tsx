import { useEffect, useState } from 'react'

import { ErrorConsole } from '../components/ErrorConsole'
import { FourTileGrid } from '../components/FourTileGrid'
import { RiskQueryForm, type RiskQuery } from '../components/RiskQueryForm'
import { fetchDefaultRisk, fetchRiskQuery, type RiskLayerResponse } from '../services/api'

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
      setMode('query')
      onQuerySuccess({ location_text: q.location_text, start_date: q.start_date, end_date: q.end_date })
    } catch (e) {
      setError(e instanceof Error ? e : String(e))
    } finally {
      setLoading(false)
    }
  }

  const heading = riskData
    ? `${riskData.location_label}  —  ${riskData.date_range.start_date} to ${riskData.date_range.end_date}`
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

      <h2 style={{ margin: '12px 0 8px 0', fontSize: 16, fontWeight: 600 }}>{heading}</h2>

      <FourTileGrid layers={riskData?.layers ?? []} viewport={riskData?.viewport} loading={loading} />
    </div>
  )
}
