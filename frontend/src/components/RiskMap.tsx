import { MapContainer, TileLayer } from 'react-leaflet'
import type { RiskLayerResponse } from '../services/api'

export function RiskMap({ layer }: { layer: RiskLayerResponse }) {
  // Rough Florida viewport
  const center: [number, number] = [27.8, -81.7]
  const zoom = 6

  return (
    <MapContainer className="map" center={center} zoom={zoom} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <TileLayer attribution={layer.attribution} url={layer.tile_url_template} opacity={0.55} />
    </MapContainer>
  )
}
