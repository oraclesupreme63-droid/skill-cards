import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { getCards } from '../api/cards'
import { SkillCard } from '../components/SkillCard'

export function CardsPage() {
  const { token } = useAuth()
  const [cards, setCards] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getCards(token)
      .then(setCards)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="loading">Cargando...</p>
  if (error) return <p className="error-message">{error}</p>

  return (
    <div className="page">
      <h1>Tus cartas</h1>
      <div className="cards-stage">
        <div className="cards-grid">
          {cards.map((card) => (
            <SkillCard key={card.id} {...card} />
          ))}
        </div>
      </div>
    </div>
  )
}
