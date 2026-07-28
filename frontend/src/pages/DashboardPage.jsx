import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import {
  listSkills,
  createSkill,
  getSkillHistory,
  getSkillQuestion,
  levelUpSkill,
} from '../api/skills'

export function DashboardPage() {
  const { token } = useAuth()

  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  const [newSkillName, setNewSkillName] = useState('')
  const [createError, setCreateError] = useState(null)

  const [historyBySkill, setHistoryBySkill] = useState({})

  // Guarda la pregunta activa de cada skill (null si el panel está cerrado).
  const [questionBySkill, setQuestionBySkill] = useState({})
  const [answerBySkill, setAnswerBySkill] = useState({})
  const [levelUpError, setLevelUpError] = useState(null)

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

  async function openLevelUp(skillId) {
    setLevelUpError(null)
    const question = await getSkillQuestion(token, skillId)
    setQuestionBySkill((prev) => ({ ...prev, [skillId]: question }))
    setAnswerBySkill((prev) => ({ ...prev, [skillId]: '' }))
  }

  function closeLevelUp(skillId) {
    setQuestionBySkill((prev) => {
      const next = { ...prev }
      delete next[skillId]
      return next
    })
  }

  async function submitLevelUp(skillId, selfConfirmed) {
    setLevelUpError(null)
    try {
      await levelUpSkill(token, skillId, {
        questionId: questionBySkill[skillId].id,
        answerText: answerBySkill[skillId],
        selfConfirmed,
      })
      closeLevelUp(skillId)
      await loadSkills()
    } catch (err) {
      setLevelUpError(err.message)
    }
  }

  if (loading) {
    return <p className="loading">Cargando...</p>
  }

  return (
    <div className="page">
      <h1>Tus skills</h1>

      {loadError && <p className="error-message">{loadError}</p>}
      {levelUpError && <p className="error-message">{levelUpError}</p>}

      <ul className="skill-list">
        {skills.map((skill) => (
          <li className="skill-row" key={skill.id}>
            <div className="skill-row-main">
              <span className="skill-row-name">
                {skill.name} — nivel {skill.level} ({skill.is_core ? 'core' : 'custom'})
              </span>
              <div className="skill-row-actions">
                <button className="btn-ghost" onClick={() => toggleHistory(skill.id)}>
                  Ver historial
                </button>
                <button onClick={() => openLevelUp(skill.id)}>Subir de nivel</button>
              </div>
            </div>

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

            {questionBySkill[skill.id] && (
              <div className="level-up-panel">
                <p>{questionBySkill[skill.id].prompt}</p>
                <textarea
                  value={answerBySkill[skill.id]}
                  onChange={(e) =>
                    setAnswerBySkill((prev) => ({
                      ...prev,
                      [skill.id]: e.target.value,
                    }))
                  }
                  placeholder="Contá tu situación..."
                />
                <div className="level-up-panel-actions">
                  <button onClick={() => submitLevelUp(skill.id, true)}>
                    Sí, lo logré
                  </button>
                  <button className="btn-ghost" onClick={() => submitLevelUp(skill.id, false)}>
                    Todavía no
                  </button>
                  <button className="btn-ghost" onClick={() => closeLevelUp(skill.id)}>
                    Cancelar
                  </button>
                </div>
              </div>
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
      {createError && <p className="error-message">{createError}</p>}
    </div>
  )
}
