import type { UseFormRegister, FieldErrors } from 'react-hook-form';
import type { CreateEventInput } from '../types/event-types';

interface EventInfoFieldsProps {
  register: UseFormRegister<CreateEventInput>;
  errors: FieldErrors<CreateEventInput>;
}

export function EventInfoFields({ register, errors }: EventInfoFieldsProps) {
  return (
    <div className="space-y-4">
      <h3 className="text-xs font-bold text-primary uppercase tracking-wider">
        Informações do Evento
      </h3>

      <div>
        <label className="block text-xs font-bold text-foreground mb-1">Título do Evento *</label>
        <input
          {...register('title')}
          placeholder="Ex: Festival de Verão 2026"
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {errors.title && <span className="text-xs text-destructive mt-1 block">{errors.title.message}</span>}
      </div>

      <div>
        <label className="block text-xs font-bold text-foreground mb-1">Descrição *</label>
        <textarea
          {...register('description')}
          rows={3}
          placeholder="Descreva detalhes sobre o seu evento..."
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {errors.description && <span className="text-xs text-destructive mt-1 block">{errors.description.message}</span>}
      </div>
    </div>
  );
}