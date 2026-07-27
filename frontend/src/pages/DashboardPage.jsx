import { useAuth } from '../context/AuthContext'

export function DashboardPage() {
  const { logout } = useAuth()

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Estás logueado. Acá vamos a listar tus skills en la próxima fase.</p>
      <button onClick={logout}>Cerrar sesión</button>
    </div>
  )
}
