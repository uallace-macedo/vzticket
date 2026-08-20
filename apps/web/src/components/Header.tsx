import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Search, LogOut } from 'lucide-react'
import { useAuthStore } from '../features/auth/store/use-auth-store'
import { useAuth } from '../features/auth/hooks/use-auth'

interface HeaderProps {
  showSearch?: boolean
}

export function Header({ showSearch = true }: HeaderProps) {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const { user, openAuthModal } = useAuthStore()
  const { logout } = useAuth()

  function handleSearch(e: React.SubmitEvent) {
    e.preventDefault()
    if (!query.trim()) return
    navigate(`/events?query=${encodeURIComponent(query)}`)
  }

  return (
    <header className="w-full bg-background border-b border-foreground/10 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
        <Link to="/" className="text-2xl font-black text-primary tracking-tight shrink-0">
          VzTicket
        </Link>

        {showSearch ? (
          <form onSubmit={handleSearch} className="flex-1 max-w-md relative hidden sm:block">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted" />
            <input
              type="text"
              placeholder="Busque por eventos, festas, cidades..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full bg-background-muted pl-9 pr-4 py-2 rounded-full text-sm outline-none border border-transparent focus:border-primary transition"
            />
          </form>
        ) : (
          <div className="flex-1" />
        )}

        <div className="flex items-center gap-3">
          <Link to="/events" className="text-sm font-medium hover:text-primary transition hidden md:block">
            Eventos
          </Link>

          {user ? (
            <div className="flex items-center gap-3">
              <span className="text-sm font-bold text-foreground">Olá, {user.name.split(' ')[0]}</span>
              <button
                onClick={logout}
                title="Sair"
                className="p-2 text-foreground-muted hover:text-red-500 transition cursor-pointer"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button 
              onClick={openAuthModal}
              className="bg-primary text-primary-foreground text-sm font-bold px-5 py-2 rounded-xl hover:bg-primary/90 transition cursor-pointer"
            >
              Entrar
            </button>
          )}
        </div>
      </div>
    </header>
  )
}