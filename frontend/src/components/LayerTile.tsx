import { useEffect } from 'react'
import { Circle, MapContainer, TileLayer, useMap, useMapEvents } from 'react-leaflet'
import type { OverlayLayer } from '../services/api'
import { LayerLegend } from './LayerLegend'

type LayerTileProps = {
  layer: OverlayLayer
  center: [number, number]
  zoom: number
  radius?: number
  onViewportChange: (center: [number, number], zoom: number) => void
}

function ViewportSync({ center, zoom, onViewportChange }: Pick<LayerTileProps, 'center' | 'zoom' | 'onViewportChange'>) {
  const map = useMap()

  useEffect(() => {
    const currentCenter = map.getCenter()
    const currentZoom = map.getZoom()
    if (
      Math.abs(currentCenter.lat - center[0]) > 0.0001 ||
      Math.abs(currentCenter.lng - center[1]) > 0.0001 ||
      currentZoom !== zoom
    ) {
      map.setView(center, zoom, { animate: false })
    }
  }, [map, center, zoom])

  useMapEvents({
    moveend: () => {
      const c = map.getCenter()
      onViewportChange([c.lat, c.lng], map.getZoom())
    }
  })

  return null
}

export function LayerTile({ layer, center, zoom, radius, onViewportChange }: LayerTileProps) {
  return (
    <div className="panel">
      <div className="panel-header">
        <h3 className="panel-title">{layer.label}</h3>
      </div>
      <MapContainer className="tile-map" center={center} zoom={zoom} scrollWheelZoom>
        <ViewportSync center={center} zoom={zoom} onViewportChange={onViewportChange} />
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <TileLayer attribution={layer.attribution} url={layer.tile_url_template} opacity={0.55} />
        {radius ? (
          <Circle
            center={center}
            radius={radius}
            pathOptions={{ color: '#1565C0', weight: 2, fillOpacity: 0.05 }}
          />
        ) : null}
      </MapContainer>
      {layer.legend && <LayerLegend legend={layer.legend} />}
    </div>
  )
}
