import type { RiskBand } from '../services/api'

export function RiskLegend({ legend }: { legend: RiskBand[] }) {
  return (
    <div className="legend" aria-label="Risk legend">
      {legend.map((b) => (
        <div className="legend-item" key={b.code}>
          <span className="legend-swatch" style={{ background: b.color }} />
          <span>{b.label}</span>
        </div>
      ))}
    </div>
  )
}
