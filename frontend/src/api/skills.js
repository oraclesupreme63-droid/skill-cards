import { apiFetch } from './client'

export function listSkills(token) {
  return apiFetch('/skills', { token })
}

export function createSkill(token, name) {
  return apiFetch('/skills', {
    method: 'POST',
    token,
    body: JSON.stringify({ name }),
  })
}

export function getSkillHistory(token, skillId) {
  return apiFetch(`/skills/${skillId}/history`, { token })
}
