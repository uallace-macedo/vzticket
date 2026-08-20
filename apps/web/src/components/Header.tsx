import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Search, ChevronDown, User } from 'lucide-react';
import { useAuthStore } from '@/features/auth/store/use-auth-store'
import { AccountDrawer } from '@/components/AccountDrawer'

interface HeaderProps {
  showSearch?: boolean;
}

export function Header({ showSearch = true }: HeaderProps) {
  const [query, setQuery] = useState('');
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const navigate = useNavigate();

  const { user, openAuthModal } = useAuthStore();

  function handleSearch(e: React.SubmitEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    navigate(`/events?query=${encodeURIComponent(query)}`);
  }

  return (
    <>
      <header className="w-full bg-background border-b border-foreground/10 sticky top-0 z-40 py-3 sm:py-0">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row sm:items-center sm:justify-between sm:h-16 gap-3 sm:gap-4">
          <div className="flex items-center justify-between w-full sm:w-auto shrink-0">
            <Link to="/" className="text-2xl font-black text-primary tracking-tight">
              VzTicket
            </Link>

            <div className="flex items-center gap-3 sm:hidden">
              {user ? (
                <button
                  onClick={() => setIsDrawerOpen(true)}
                  className="flex items-center gap-1.5 bg-background-muted border border-foreground/10 px-3 py-1.5 rounded-xl font-bold text-sm cursor-pointer"
                >
                  <User className="w-4 h-4 text-primary" />
                  <span>Conta</span>
                  <ChevronDown className="w-3.5 h-3.5 text-foreground-muted" />
                </button>
              ) : (
                <button
                  onClick={openAuthModal}
                  className="bg-primary text-primary-foreground text-sm font-bold px-4 py-2 rounded-md hover:bg-primary/90 transition cursor-pointer"
                >
                  Entrar
                </button>
              )}
            </div>
          </div>

          {showSearch && (
            <form onSubmit={handleSearch} className="w-full sm:flex-1 sm:max-w-md relative">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted" />
              <input
                type="text"
                placeholder="Busque por eventos, festas, cidades..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-background-muted pl-9 pr-4 py-2.5 sm:py-2 rounded-xl sm:rounded-full text-sm outline-none border border-foreground/5 sm:border-transparent focus:border-primary transition"
              />
            </form>
          )}

          <div className="hidden sm:flex items-center gap-7">
            <Link to="/events" className="text-sm font-medium hover:text-primary transition hidden md:block">
              Eventos
            </Link>

            {user ? (
              <button
                onClick={() => setIsDrawerOpen(true)}
                className="flex items-center gap-2 bg-background-muted border border-foreground/10 px-4 py-2 rounded-xl hover:bg-foreground/5 transition font-bold text-sm cursor-pointer"
              >
                <User className="w-4 h-4 text-primary" />
                <span>Conta</span>
                <ChevronDown className="w-4 h-4 text-foreground-muted" />
              </button>
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

      <AccountDrawer isOpen={isDrawerOpen} onClose={() => setIsDrawerOpen(false)} />
    </>
  )
}