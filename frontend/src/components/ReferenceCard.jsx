import { SkillCard } from './SkillCard'

export function ReferenceCard({ name, photo_url, description, overall_rarity, role, skills }) {
  return (
    <div className="reference-card">
      <img
        className="reference-card-photo"
        src={`${import.meta.env.VITE_API_URL}${photo_url}`}
        alt={name}
      />
      <h2>{name}</h2>
      <p className="reference-card-tier">
        {overall_rarity} — {role}
      </p>
      <p className="reference-card-description">{description}</p>

      <div className="cards-grid">
        {skills.map((skill) => (
          <SkillCard key={skill.name} {...skill} />
        ))}
      </div>
    </div>
  )
}
