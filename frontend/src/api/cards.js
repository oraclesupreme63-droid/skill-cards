import { apiFetch } from './client'

export function getCards(token) {
  return apiFetch('/cards', { token })
}

export function getReferenceCards() {
  return apiFetch('/reference-cards')
}
