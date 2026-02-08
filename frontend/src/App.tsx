import { useState } from 'react'

import { Drivers } from './pages/Drivers'
import { Home } from './pages/Home'

export function App() {
  const [page, setPage] = useState<'home' | 'drivers'>('home')
  const [lastQuery, setLastQuery] = useState<{ location_text: string; start_date: string; end_date: string } | null>(null)

  return (
    <div className="app">
      {page === 'home' ? (
        <Home
          onOpenDrivers={() => setPage('drivers')}
          onQuerySuccess={(q) => setLastQuery(q)}
        />
      ) : (
        <Drivers onBack={() => setPage('home')} initialQuery={lastQuery} />
      )}
    </div>
  )
}
