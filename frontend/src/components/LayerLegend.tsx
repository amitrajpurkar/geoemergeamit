import type { LayerLegend as LayerLegendType } from '../services/api'

type LayerLegendProps = {
  legend: LayerLegendType
  layerName?: string
}

export function LayerLegend({ legend, layerName }: LayerLegendProps) {
  return (
    <div style={{ marginTop: 8, padding: 8, backgroundColor: '#f9f9f9', borderRadius: 4 }}>
      {layerName && (
        <h4 style={{ margin: '0 0 8px 0', fontSize: 13, fontWeight: 600 }}>{layerName}</h4>
      )}

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
}
