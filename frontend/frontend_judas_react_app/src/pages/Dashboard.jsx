
import React, { useEffect, useState } from 'react'

function Dashboard() {
  const [shadow, setShadow] = useState(null)
  const [positions, setPositions] = useState([])

  useEffect(() => {
    fetch('/api/shadow').then(res => res.json()).then(setShadow)
    fetch('/api/positions').then(res => res.json()).then(setPositions)
  }, [])

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">📊 Judas Shadow Dashboard</h1>
      <div>
        <h2>💰 Shadow Account</h2>
        <pre>{JSON.stringify(shadow, null, 2)}</pre>
      </div>
      <div>
        <h2>📂 Positions</h2>
        <pre>{JSON.stringify(positions, null, 2)}</pre>
      </div>
    </div>
  )
}

export default Dashboard
