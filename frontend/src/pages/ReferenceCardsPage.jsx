import { useState, useEffect } from 'react'
import { getReferenceCards } from '../api/cards'
import { ReferenceCard } from '../components/ReferenceCard'

export function ReferenceCardsPage() {
  const [cards, setCards] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getReferenceCards()
      .then(setCards)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="loading">Cargando...</p>
  if (error) return <p className="error-message">{error}</p>

  return (
    <div className="page">
      <h1>Cartas de referencia</h1>
      <div className="cards-stage">
        {cards.map((card) => (
          <ReferenceCard key={card.id} {...card} />
        ))}
      </div>
    </div>
  )
}
