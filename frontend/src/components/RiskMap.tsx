import { useEffect } from 'react'

import { Circle, MapContainer, TileLayer, useMap } from 'react-leaflet'
import type { RiskLayerResponse } from '../services/api'

function ViewportController({ layer }: { layer: RiskLayerResponse }) {
  const map = useMap()

  const vp = layer.viewport
  useEffect(() => {
    if (vp && typeof vp.center_lat === 'number' && typeof vp.center_lng === 'number') {
      map.setView([vp.center_lat, vp.center_lng], 8)
    } else {
      map.setView([27.8, -81.7], 6)
    }
  }, [map, vp])
  return null
}

export function RiskMap({ layer, overlayUrl, overlayAttribution }: { layer: RiskLayerResponse; overlayUrl: string; overlayAttribution?: string }) {
  const vp = layer.viewport

  return (
    <MapContainer className="map" center={[27.8, -81.7]} zoom={6} scrollWheelZoom>
      <ViewportController layer={layer} />
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <TileLayer attribution={overlayAttribution ?? layer.attribution} url={overlayUrl} opacity={0.55} />
      {vp ? (
        <Circle
          center={[vp.center_lat, vp.center_lng]}
          radius={vp.radius_meters}
          pathOptions={{ color: '#1565C0', weight: 2, fillOpacity: 0.05 }}
        />
      ) : null}
    </MapContainer>
  )
}
