import { Plus, Minus, Ticket, Clock } from 'lucide-react';
import type { EventTicketInfo } from '../types';

interface TicketSelectorProps {
  ticketInfo: EventTicketInfo;
  quantity: number;
  salesStartAt?: string;
  onQuantityChange: (qty: number) => void;
}

export function TicketSelector({
  ticketInfo,
  quantity,
  salesStartAt,
  onQuantityChange,
}: TicketSelectorProps) {
  const { ticket_price, service_fee, available_tickets, title } = ticketInfo;

  const isSalesStarted = salesStartAt
    ? new Date(salesStartAt).getTime() <= new Date().getTime()
    : true;

  const formattedSalesStartDate = salesStartAt
    ? new Date(salesStartAt).toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      })
    : '';

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  if (!isSalesStarted) {
    return (
      <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-3">
        <div className="flex items-center gap-2 text-amber-500 font-bold text-sm">
          <Clock className="w-4 h-4" />
          <span>Vendas não iniciadas</span>
        </div>
        <p className="text-xs text-foreground-muted font-medium">
          As vendas para este ingresso começam em{' '}
          <strong className="text-foreground">{formattedSalesStartDate}</strong>.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-4">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2.5 min-w-0 flex-1">
          <Ticket className="w-5 h-5 text-primary shrink-0 mt-0.5" />
          <h3
            className="font-extrabold text-sm sm:text-base text-foreground leading-snug line-clamp-2"
            title={title || 'Ingresso'}
          >
            {title || 'Ingresso'}
          </h3>
        </div>

        <span className="shrink-0 whitespace-nowrap text-[11px] sm:text-xs font-bold text-foreground-muted bg-foreground/5 px-2.5 py-1 rounded-full text-center">
          {available_tickets > 0 ? `${available_tickets} disponíveis` : 'Esgotado'}
        </span>
      </div>

      <div className="flex items-center justify-between pt-1 gap-2">
        <div>
          <div className="text-lg sm:text-xl font-black text-foreground">
            {formatCurrency(ticket_price)}
          </div>
          <div className="text-xs font-semibold text-foreground-muted">
            + {formatCurrency(service_fee)} taxa de serviço
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 bg-background border border-foreground/10 p-1 rounded-xl shrink-0">
          <button
            onClick={() => onQuantityChange(Math.max(0, quantity - 1))}
            disabled={quantity === 0}
            className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-foreground/5 transition disabled:opacity-30 cursor-pointer"
          >
            <Minus className="w-4 h-4" />
          </button>

          <span className="font-black text-sm w-4 text-center">{quantity}</span>

          <button
            onClick={() => onQuantityChange(Math.min(available_tickets, quantity + 1))}
            disabled={quantity >= available_tickets}
            className="w-8 h-8 flex items-center justify-center rounded-lg bg-foreground text-background hover:opacity-90 transition disabled:opacity-30 cursor-pointer"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}