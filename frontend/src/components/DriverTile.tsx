import { MapContainer, TileLayer } from 'react-leaflet'

import type { DriverTile as DriverTileType } from '../services/api'
import type { Viewport } from '../services/api'

export function DriverTile({ tile, viewport }: { tile: DriverTileType; viewport: Viewport | null }) {
  const center: [number, number] = viewport ? [viewport.center_lat, viewport.center_lng] : [27.8, -81.7]
  return (
    <div className="panel">
      <div className="panel-header">
        <h2 className="panel-title">{tile.title}</h2>
      </div>
      <div style={{ padding: 12 }}>
        <div style={{ color: '#444', fontSize: 14 }}>{tile.summary}</div>
        {tile.tile_url_template ? (
          <div style={{ marginTop: 12 }}>
            <MapContainer className="map" center={center} zoom={8} scrollWheelZoom={false} style={{ height: 240 }}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <TileLayer url={tile.tile_url_template} opacity={0.7} />
            </MapContainer>
          </div>
        ) : null}
        {tile.attribution ? (
          <div style={{ marginTop: 8, fontSize: 12, color: '#666' }}>{tile.attribution}</div>
        ) : null}
      </div>
    </div>
  )
}
