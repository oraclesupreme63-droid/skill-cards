import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { listSkills, createSkill, getSkillHistory } from '../api/skills'

export function DashboardPage() {
  const { token, logout } = useAuth()

  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [newSkillName, setNewSkillName] = useState('')
  const [createError, setCreateError] = useState(null)

  const [historyBySkill, setHistoryBySkill] = useState({})

  useEffect(() => {
    loadSkills()
  }, [])

  async function loadSkills() {
    setLoading(true)
    try {
      const data = await listSkills(token)
      setSkills(data)
    } catch (err) {
      setLoadError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleCreateSkill(event) {
    event.preventDefault()
    setCreateError(null)

    try {
      await createSkill(token, newSkillName)
      setNewSkillName('')
      await loadSkills()
    } catch (err) {
      setCreateError(err.message)
    }
  }

  async function toggleHistory(skillId) {
    if (historyBySkill[skillId]) {
      setHistoryBySkill((prev) => {
        const next = { ...prev }
        delete next[skillId]
        return next
      })
      return
    }

    const history = await getSkillHistory(token, skillId)
    setHistoryBySkill((prev) => ({ ...prev, [skillId]: history }))
  }

  if (loading) {
    return <p>Cargando...</p>
  }

  return (
    <div>
      <h1>Tus skills</h1>
      <button onClick={logout}>Cerrar sesión</button>

      {loadError && <p>{loadError}</p>}

      <ul>
        {skills.map((skill) => (
          <li key={skill.id}>
            {skill.name} — nivel {skill.level} ({skill.is_core ? 'core' : 'custom'})
            <button onClick={() => toggleHistory(skill.id)}>Ver historial</button>

            {historyBySkill[skill.id] && (
              <ul>
                {historyBySkill[skill.id].length === 0 && (
                  <li>Todavía no subiste de nivel esta skill.</li>
                )}
                {historyBySkill[skill.id].map((entry, index) => (
                  <li key={index}>
                    Nivel {entry.level} — {entry.recorded_at}
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>

      <h2>Crear skill personalizada</h2>
      <form onSubmit={handleCreateSkill}>
        <input
          value={newSkillName}
          onChange={(e) => setNewSkillName(e.target.value)}
          placeholder="Nombre de la skill"
        />
        <button type="submit">Crear</button>
      </form>
      {createError && <p>{createError}</p>}
    </div>
  )
}
