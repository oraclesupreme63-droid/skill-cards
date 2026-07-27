const BASE_URL = import.meta.env.VITE_API_URL

export async function apiFetch(path, { token, ...options } = {}) {
  const headers = { ...options.headers }

  // URLSearchParams (form-urlencoded) sets its own Content-Type automatically.
  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers['Content-Type'] = 'application/json'
  }
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const message = data?.detail ?? 'Something went wrong'
    throw new Error(typeof message === 'string' ? message : 'Something went wrong')
  }

  return data
}
