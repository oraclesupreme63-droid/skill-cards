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

  if (loading) return <p>Cargando...</p>
  if (error) return <p>{error}</p>

  return (
    <div>
      <h1>Cartas de referencia</h1>
      {cards.map((card) => (
        <ReferenceCard key={card.id} {...card} />
      ))}
    </div>
  )
}
