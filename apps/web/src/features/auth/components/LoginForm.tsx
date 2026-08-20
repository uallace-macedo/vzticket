import { Loader2 } from 'lucide-react'
import { useAuth } from '../hooks/use-auth'

export function LoginForm() {
  const { login } = useAuth()

  return (
    <form onSubmit={login.handleSubmit} className="space-y-4 pt-4">
      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          E-mail
        </label>
        <input
          type="email"
          placeholder="seu@email.com"
          {...login.register('username')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {login.errors.username && (
          <span className="text-xs text-red-500 mt-1 block">
            {login.errors.username.message}
          </span>
        )}
      </div>

      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          Senha
        </label>
        <input
          type="password"
          placeholder="••••••••"
          {...login.register('password')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {login.errors.password && (
          <span className="text-xs text-red-500 mt-1 block">
            {login.errors.password.message}
          </span>
        )}
      </div>

      <button
        type="submit"
        disabled={login.isPending}
        className="w-full bg-primary text-primary-foreground font-bold py-3 rounded-xl hover:bg-primary/90 transition flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
      >
        {login.isPending ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Entrando...</span>
          </>
        ) : (
          <span>Entrar na conta</span>
        )}
      </button>
    </form>
  )
}