import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState('cargando...')

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('error'))
  }, [])

  return (
    <div>
      <h1>Skill Cards</h1>
      <p>Backend status: {status}</p>
    </div>
  )
}

export default App
