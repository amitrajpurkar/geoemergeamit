export type DateRange = {
  start_date: string
  end_date: string
}

export type RiskBand = {
  code: 'low' | 'medium' | 'high'
  label: string
  color: string
}

export type OverlayLayer = {
  layer_id: string
  label: string
  tile_url_template: string
  attribution?: string
}

export type Viewport = {
  center_lat: number
  center_lng: number
  radius_meters: number
}

export type RiskLayerResponse = {
  location_label: string
  date_range: DateRange
  tile_url_template: string
  attribution?: string
  legend: RiskBand[]
  layers?: OverlayLayer[]
  viewport?: Viewport | null
}

export type RiskQueryRequest = {
  location_text: string
  date_range: DateRange
}

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://127.0.0.1:8000'

export async function fetchDefaultRisk(window: 'last_30_days' | 'last_12_months'): Promise<RiskLayerResponse> {
  const url = new URL('/api/risk/default', API_BASE)
  url.searchParams.set('window', window)

  const resp = await fetch(url.toString())
  if (!resp.ok) {
    const body = await resp.json().catch(() => null)
    const detail = body?.detail ?? `Request failed (${resp.status})`
    throw new Error(detail)
  }
  return resp.json()
}

export async function fetchRiskQuery(body: RiskQueryRequest): Promise<RiskLayerResponse> {
  const url = new URL('/api/risk/query', API_BASE)

  const resp = await fetch(url.toString(), {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body)
  })

  if (!resp.ok) {
    const bodyJson = await resp.json().catch(() => null)
    const detail = bodyJson?.detail ?? `Request failed (${resp.status})`
    throw new Error(detail)
  }
  return resp.json()
}
