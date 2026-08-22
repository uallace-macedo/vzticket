import type { UseFormRegister, FieldErrors, UseFormWatch } from 'react-hook-form';
import { Ticket, Percent } from 'lucide-react';
import type { CreateEventFormInput } from '../types/event-types';

interface EventTicketFieldsProps {
  register: UseFormRegister<CreateEventFormInput>;
  errors: FieldErrors<CreateEventFormInput>;
  watch: UseFormWatch<CreateEventFormInput>;
}

export function EventTicketFields({ register, errors, watch }: EventTicketFieldsProps) {
  const ticketPrice = watch('ticket_price') || 0;
  
  const feePercentage = Number(import.meta.env.VITE_EVENT_CREATION_FEE_PERCENTAGE || 0.05);
  const calculatedFee = (Number(ticketPrice) * feePercentage).toFixed(2);
  const feePercentageFormatted = (feePercentage * 100).toLocaleString('pt-BR');

  return (
    <div className="space-y-4 pt-4 border-t border-foreground/10">
      <h3 className="text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-2">
        <Ticket className="w-4 h-4" /> Ingressos & Taxas
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Título do Ingresso *</label>
          <input
            {...register('ticket_title')}
            placeholder="Ex: Pista / Geral"
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
          {errors.ticket_title && (
            <span className="text-xs text-destructive mt-1 block">{errors.ticket_title.message}</span>
          )}
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Preço Unitário (R$) *</label>
          <input
            type="number"
            step="0.01"
            min="0"
            {...register('ticket_price', { valueAsNumber: true })}
            placeholder="0.00"
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
          {errors.ticket_price && (
            <span className="text-xs text-destructive mt-1 block">{errors.ticket_price.message}</span>
          )}
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Total Disponível *</label>
          <input
            type="number"
            min="1"
            {...register('available_tickets', { valueAsNumber: true })}
            placeholder="100"
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
          {errors.available_tickets && (
            <span className="text-xs text-destructive mt-1 block">{errors.available_tickets.message}</span>
          )}
        </div>
      </div>

      <div className="bg-primary/5 border border-primary/20 rounded-xl p-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Percent className="w-4 h-4 text-primary" />
          <span className="text-xs text-foreground-muted">
            Taxa da Plataforma ({feePercentageFormatted}%):
          </span>
        </div>
        <span className="text-xs font-extrabold text-primary">
          R$ {isNaN(Number(calculatedFee)) ? '0,00' : Number(calculatedFee).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
        </span>
      </div>
    </div>
  );
}