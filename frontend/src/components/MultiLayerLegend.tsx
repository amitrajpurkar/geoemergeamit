type LegendCategory = {
  value: number
  label: string
  color: string
}

type LayerLegend = {
  type: 'categorical' | 'continuous'
  min: number
  max: number
  palette: string[]
  unit?: string
  categories?: LegendCategory[]
}

type LayerWithLegend = {
  layer_id?: string
  driver_type?: string
  label?: string
  title?: string
  legend?: LayerLegend
}

export function MultiLayerLegend({ layers }: { layers: LayerWithLegend[] }) {
  if (!layers?.length) return null

  return (
    <div style={{ marginTop: 12 }}>
      <h3 style={{ margin: '0 0 8px 0', fontSize: 14, fontWeight: 600 }}>Layer Legends</h3>
      <div style={{ display: 'grid', gap: 12 }}>
        {layers.map((layer) => {
          if (!layer.legend) return null

          const legend = layer.legend
          const layerKey = layer.layer_id || layer.driver_type || 'unknown'
          const layerName = layer.label || layer.title || 'Unknown Layer'

          return (
            <div key={layerKey} className="panel" style={{ padding: 12 }}>
              <h4 style={{ margin: '0 0 8px 0', fontSize: 13, fontWeight: 600 }}>{layerName}</h4>

              {legend.type === 'categorical' && legend.categories ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  {legend.categories.map((cat) => (
                    <div key={cat.value} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <div
                        style={{
                          width: 20,
                          height: 20,
                          backgroundColor: cat.color,
                          border: '1px solid #ccc',
                          borderRadius: 2
                        }}
                      />
                      <span style={{ fontSize: 12 }}>{cat.label}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <div>
                  <div
                    style={{
                      height: 20,
                      background: `linear-gradient(to right, ${legend.palette.join(', ')})`,
                      border: '1px solid #ccc',
                      borderRadius: 2,
                      marginBottom: 4
                    }}
                  />
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: '#666' }}>
                    <span>
                      {legend.min} {legend.unit || ''}
                    </span>
                    <span>
                      {legend.max} {legend.unit || ''}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
