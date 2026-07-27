import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function NavBar() {
  const { token, logout } = useAuth()

  return (
    <nav className="navbar">
      {token ? (
        <>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/cards">Mis cartas</Link>
          <Link to="/reference-cards">Cartas de referencia</Link>
          <button onClick={logout}>Cerrar sesión</button>
        </>
      ) : (
        <>
          <Link to="/login">Iniciar sesión</Link>
          <Link to="/register">Crear cuenta</Link>
          <Link to="/reference-cards">Cartas de referencia</Link>
        </>
      )}
    </nav>
  )
}
