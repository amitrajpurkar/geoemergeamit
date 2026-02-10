import { useEffect, useState } from 'react'
import type { OverlayLayer, Viewport } from '../services/api'
import { LayerTile } from './LayerTile'

type FourTileGridProps = {
  layers: OverlayLayer[]
  viewport?: Viewport | null
  loading?: boolean
}

export function FourTileGrid({ layers, viewport, loading }: FourTileGridProps) {
  const initialCenter: [number, number] = viewport
    ? [viewport.center_lat, viewport.center_lng]
    : [27.8, -81.7]
  const initialZoom = viewport ? 8 : 6

  const [center, setCenter] = useState<[number, number]>(initialCenter)
  const [zoom, setZoom] = useState<number>(initialZoom)

  useEffect(() => {
    if (viewport) {
      setCenter([viewport.center_lat, viewport.center_lng])
      setZoom(8)
    } else {
      setCenter([27.8, -81.7])
      setZoom(6)
    }
  }, [viewport])

  const handleViewportChange = (newCenter: [number, number], newZoom: number) => {
    setCenter(newCenter)
    setZoom(newZoom)
  }

  if (loading) {
    return (
      <div className="four-tile-grid">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="panel" style={{ padding: 16, textAlign: 'center', color: '#666' }}>
            Loading tile {i}...
          </div>
        ))}
      </div>
    )
  }

  if (!layers || layers.length === 0) {
    return (
      <div style={{ padding: 16, textAlign: 'center', color: '#666' }}>
        No layer data available.
      </div>
    )
  }

  return (
    <div className="four-tile-grid">
      {layers.map((layer) => (
        <LayerTile
          key={layer.layer_id}
          layer={layer}
          center={center}
          zoom={zoom}
          radius={viewport?.radius_meters}
          onViewportChange={handleViewportChange}
        />
      ))}
    </div>
  )
}
