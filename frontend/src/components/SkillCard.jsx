import { rarityStyle } from '../utils/rarityColors'

export function SkillCard({ name, level, rarity, is_core }) {
  const style = rarityStyle(rarity)

  return (
    <div
      className="skill-card"
      style={{
        background: style.background,
        color: style.color,
        boxShadow: `0 0 24px ${style.glow}, 0 8px 16px rgba(0, 0, 0, 0.35)`,
      }}
    >
      <span className="skill-card-tag">{is_core ? 'CORE' : 'CUSTOM'}</span>
      <h3>{name}</h3>
      <p className="skill-card-level">Nivel {level}</p>
      <p className="skill-card-rarity">{rarity.toUpperCase()}</p>
    </div>
  )
}
