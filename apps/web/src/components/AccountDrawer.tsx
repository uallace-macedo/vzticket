import { useNavigate } from 'react-router-dom';
import { Ticket, LogOut, ChevronRight, Wallet, Calendar, ScanLine } from 'lucide-react';
import { PAGES } from '@/constants/pages';
import { useAuth } from '@/features/auth/hooks/use-auth';
import { useAuthStore } from '@/features/auth/store/use-auth-store';

interface AccountDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function AccountDrawer({ isOpen, onClose }: AccountDrawerProps) {
  const { user } = useAuthStore();
  const isOrganizer = user?.role === 'organizer';
  const isGatekeeper = user?.role === 'gatekeeper';
  
  const navigate = useNavigate();
  const { logout } = useAuth();

  function handleNavigate(path: string) {
    navigate(path);
    onClose();
  }

  function handleLogout() {
    logout();
    onClose();
  }

  return (
    <div
      className={`fixed inset-0 z-100 transition-all duration-300 ease-out ${
        isOpen
          ? 'pointer-events-auto bg-black/1 backdrop-blur-md opacity-98'
          : 'pointer-events-none bg-black/0 backdrop-blur-none opacity-0'
      }`}
    >
      <div className="absolute inset-0" onClick={onClose} />
      <div
        className={`absolute bg-background p-6 shadow-2xl transition-transform duration-300 ease-out flex flex-col justify-between z-10
          /* Mobile */
          bottom-0 left-0 right-0 rounded-t-3xl border-t border-foreground/10 max-h-[85vh]
          ${isOpen ? 'translate-y-0' : 'translate-y-full'}

          /* Desktop */
          sm:top-0 sm:bottom-0 sm:right-0 sm:left-auto sm:w-full sm:max-w-sm sm:h-screen sm:max-h-none sm:rounded-none sm:border-l sm:border-foreground/10 sm:border-t-0
          ${isOpen ? 'sm:translate-y-0 sm:translate-x-0' : 'sm:translate-y-0 sm:translate-x-full'}
        `}
      >
        <div>
          <div className="w-12 h-1.5 bg-foreground/15 rounded-full mx-auto mb-4 sm:hidden" />
          <div className="mt-6 bg-background-muted/60 border border-foreground/5 rounded-2xl p-2 space-y-1">
            <button
              onClick={() => handleNavigate(PAGES.PRIVATE.WALLET)}
              className="w-full flex items-center justify-between p-3.5 rounded-xl hover:bg-background transition cursor-pointer group"
            >
              <div className="flex items-center gap-3">
                <Wallet className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
                <span className="text-sm font-bold text-foreground">Carteira Digital</span>
              </div>
              <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
            </button>

            <button
              onClick={() => handleNavigate(PAGES.PRIVATE.TICKETS.BASE)}
              className="w-full flex items-center justify-between p-3.5 rounded-xl hover:bg-background transition cursor-pointer group"
            >
              <div className="flex items-center gap-3">
                <Ticket className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
                <span className="text-sm font-bold text-foreground">Meus Ingressos</span>
              </div>
              <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
            </button>

            {isOrganizer && (
              <button
                onClick={() => handleNavigate(PAGES.PRIVATE.ORGANIZER.EVENTS)}
                className="w-full flex items-center justify-between p-3.5 rounded-xl hover:bg-background transition cursor-pointer group"
              >
                <div className="flex items-center gap-3">
                  <Calendar className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
                  <span className="text-sm font-bold text-foreground">Meus Eventos</span>
                </div>
                <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
              </button>
            )}

            {(isOrganizer || isGatekeeper) && (
              <button
                onClick={() => handleNavigate(PAGES.PRIVATE.CHECKIN.BASE)}
                className="w-full flex items-center justify-between p-3.5 rounded-xl hover:bg-background transition cursor-pointer group"
              >
                <div className="flex items-center gap-3">
                  <ScanLine className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
                  <span className="text-sm font-bold text-foreground">Portaria / Check-in</span>
                </div>
                <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
              </button>
            )}
          </div>
        </div>

        <div className="bg-background-muted/60 p-2 rounded-xl border border-foreground/5 mt-4 hover:bg-red-500/10 text-red-500 transition">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-between p-3.5 cursor-pointer group"
          >
            <div className="flex items-center gap-3">
              <LogOut className="w-5 h-5" />
              <span className="text-sm font-bold">Sair</span>
            </div>
            <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition" />
          </button>
        </div>
      </div>
    </div>
  )
}