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

export function getSkillQuestion(token, skillId) {
  return apiFetch(`/skills/${skillId}/question`, { token })
}

export function levelUpSkill(token, skillId, { questionId, answerText, selfConfirmed }) {
  return apiFetch(`/skills/${skillId}/level`, {
    method: 'PATCH',
    token,
    body: JSON.stringify({
      question_id: questionId,
      answer_text: answerText,
      self_confirmed: selfConfirmed,
    }),
  })
}
