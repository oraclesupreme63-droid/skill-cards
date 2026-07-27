import { SkillCard } from './SkillCard'
import { referenceTierStyle } from '../utils/referenceTierStyles'

export function ReferenceCard({ name, photo_url, description, overall_rarity, role, skills }) {
  const style = referenceTierStyle(overall_rarity)

  return (
    <div
      className="reference-card"
      style={{
        background: style.background,
        color: style.color,
        borderColor: style.border,
        boxShadow: `0 0 50px ${style.glow}, 0 10px 30px rgba(0, 0, 0, 0.5)`,
      }}
    >
      <div className="reference-card-shine" />

      <img
        className="reference-card-photo"
        style={{ borderColor: style.border }}
        src={`${import.meta.env.VITE_API_URL}${photo_url}`}
        alt={name}
      />
      <h2>{name}</h2>
      <p className="reference-card-tier" style={{ color: style.color }}>
        {overall_rarity} — {role}
      </p>
      <p className="reference-card-description" style={{ color: style.color }}>
        {description}
      </p>

      <div className="cards-grid">
        {skills.map((skill) => (
          <SkillCard key={skill.name} {...skill} />
        ))}
      </div>
    </div>
  )
}
