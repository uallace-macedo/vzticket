import { useState } from 'react'
import { X } from 'lucide-react'
import { useAuthStore } from '../store/use-auth-store'
import { LoginForm } from './LoginForm'
import { RegisterForm } from './RegisterForm'

export function AuthModal() {
  const { isAuthModalOpen, closeAuthModal } = useAuthStore()
  const [tab, setTab] = useState<'login' | 'register'>('login')

  if (!isAuthModalOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4">
      <div className="bg-background w-full max-w-md rounded-2xl p-6 shadow-xl border border-foreground/10 relative animate-in fade-in zoom-in-95 duration-200">
        <button
          onClick={closeAuthModal}
          className="absolute right-4 top-4 text-foreground-muted hover:text-foreground transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex border-b border-foreground/10 mb-2">
          <button
            onClick={() => setTab('login')}
            className={`flex-1 py-3 text-sm font-bold border-b-2 transition cursor-pointer ${
              tab === 'login'
                ? 'border-primary text-primary'
                : 'border-transparent text-foreground-muted hover:text-foreground'
            }`}
          >
            Entrar
          </button>
          <button
            onClick={() => setTab('register')}
            className={`flex-1 py-3 text-sm font-bold border-b-2 transition cursor-pointer ${
              tab === 'register'
                ? 'border-primary text-primary'
                : 'border-transparent text-foreground-muted hover:text-foreground'
            }`}
          >
            Criar Conta
          </button>
        </div>

        {tab === 'login' ? (
          <LoginForm />
        ) : (
          <RegisterForm onSuccess={() => setTab('login')} />
        )}
      </div>
    </div>
  )
}