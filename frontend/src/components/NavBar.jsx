import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export function NavBar() {
  const { token, logout } = useAuth()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        Skill Cards
      </Link>

      <div className="navbar-links">
        {token ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/cards">Mis cartas</Link>
            <Link to="/reference-cards">Cartas de referencia</Link>
            <button className="btn-ghost" onClick={logout}>
              Cerrar sesión
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Iniciar sesión</Link>
            <Link to="/register">Crear cuenta</Link>
            <Link to="/reference-cards">Cartas de referencia</Link>
          </>
        )}
      </div>
    </nav>
  )
}
