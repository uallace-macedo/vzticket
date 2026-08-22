import type { UseFormRegister, FieldErrors } from 'react-hook-form';
import { Calendar } from 'lucide-react';
import type { CreateEventFormInput } from '../types/event-types';

interface EventDateFieldsProps {
  register: UseFormRegister<CreateEventFormInput>;
  errors: FieldErrors<CreateEventFormInput>;
}

export function EventDateFields({ register, errors }: EventDateFieldsProps) {
  return (
    <div className="space-y-4 pt-4 border-t border-foreground/10">
      <h3 className="text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-2">
        <Calendar className="w-4 h-4" /> Datas do Evento e Vendas
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Data do Evento *</label>
          <input
            type="datetime-local"
            {...register('event_date')}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
          {errors.event_date && <span className="text-xs text-destructive mt-1 block">{errors.event_date.message}</span>}
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Início das Vendas (Opcional)</label>
          <input
            type="datetime-local"
            {...register('sales_start_at')}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Término das Vendas (Opcional)</label>
          <input
            type="datetime-local"
            {...register('sales_end_at')}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
        </div>
      </div>
    </div>
  );
}