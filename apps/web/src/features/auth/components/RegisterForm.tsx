import { Loader2 } from 'lucide-react'
import { useAuth } from '../hooks/use-auth'

interface RegisterFormProps {
  onSuccess: () => void
}

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const { create } = useAuth();

  return (
    <form
      onSubmit={(e) => {
        create.handleSubmit(e)
        if (create.isSuccess) onSuccess()
      }}
      className="space-y-4 pt-4"
    >
      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          Nome Completo
        </label>
        <input
          type="text"
          placeholder="Seu nome"
          {...create.register('name')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {create.errors.name && (
          <span className="text-xs text-red-500 mt-1 block">
            {create.errors.name.message}
          </span>
        )}
      </div>

      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          E-mail
        </label>
        <input
          type="email"
          placeholder="seu@email.com"
          {...create.register('email')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {create.errors.email && (
          <span className="text-xs text-red-500 mt-1 block">
            {create.errors.email.message}
          </span>
        )}
      </div>

      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          Tipo de Conta
        </label>
        <select
          {...create.register('role')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition cursor-pointer"
        >
          <option value="client">Cliente / Comprador</option>
          <option value="organizer">Organizador de Eventos</option>
          <option value="gatekeeper">Portaria / Validador</option>
        </select>
        {create.errors.role && (
          <span className="text-xs text-red-500 mt-1 block">
            {create.errors.role.message}
          </span>
        )}
      </div>

      <div>
        <label className="text-xs font-bold uppercase text-foreground-muted block mb-1">
          Senha
        </label>
        <input
          type="password"
          placeholder="Mínimo 6 caracteres"
          {...create.register('password')}
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-4 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {create.errors.password && (
          <span className="text-xs text-red-500 mt-1 block">
            {create.errors.password.message}
          </span>
        )}
      </div>

      <button
        type="submit"
        disabled={create.isPending}
        className="w-full bg-primary text-primary-foreground font-bold py-3 rounded-xl hover:bg-primary/90 transition flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
      >
        {create.isPending ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Criando conta...</span>
          </>
        ) : (
          <span>Cadastrar</span>
        )}
      </button>
    </form>
  )
}