import { Calendar, MapPin, Ticket } from 'lucide-react';
import type { Event } from '@/features/event/types';

interface CheckoutEventSummaryProps {
  event: Event;
  quantity: number;
}

export function CheckoutEventSummary({ event, quantity }: CheckoutEventSummaryProps) {
  const imageUrl =
    event.media?.poster_url ||
    event.media?.custom_image_url ||
    event.media?.banner_url;

  const formattedDate = event.event_date
    ? new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }).format(new Date(event.event_date))
    : 'Data a definir';

  const ticketPrice = event.ticket_info.ticket_price;
  const serviceFee = event.ticket_info.service_fee;
  const unitTotal = event.ticket_info.total_price;
  const subtotal = unitTotal * quantity;

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  return (
    <div className="bg-background-muted border border-foreground/10 rounded-2xl p-5 space-y-5">
      <h2 className="text-base font-black text-foreground border-b border-foreground/10 pb-3">
        Resumo do Pedido
      </h2>

      <div className="flex gap-3">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={event.title}
            className="w-16 h-16 rounded-xl object-cover shrink-0 bg-background border border-foreground/10"
          />
        ) : (
          <div className="w-16 h-16 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <Calendar className="w-6 h-6" />
          </div>
        )}

        <div className="min-w-0 space-y-1">
          <h3 className="text-sm font-extrabold text-foreground leading-snug line-clamp-2">
            {event.title}
          </h3>
          <div className="flex items-center gap-1.5 text-xs text-foreground-muted">
            <Calendar className="w-3.5 h-3.5 text-primary shrink-0" />
            <span className="truncate">{formattedDate}</span>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-foreground-muted">
            <MapPin className="w-3.5 h-3.5 text-primary shrink-0" />
            <span className="truncate">
              {event.location?.name || `${event.location?.city}, ${event.location?.state}`}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-2 text-xs pt-3 border-t border-foreground/10">
        <div className="flex items-center justify-between text-foreground-muted">
          <span className="flex items-center gap-1">
            <Ticket className="w-3.5 h-3.5" />
            Ingresso ({quantity}x)
          </span>
          <span className="font-semibold text-foreground">
            {formatCurrency(ticketPrice * quantity)}
          </span>
        </div>

        <div className="flex items-center justify-between text-foreground-muted">
          <span>Taxas de Serviço ({quantity}x)</span>
          <span className="font-semibold text-foreground">
            {formatCurrency(serviceFee * quantity)}
          </span>
        </div>

        <div className="flex items-center justify-between text-sm font-black text-foreground pt-3 border-t border-foreground/10">
          <span>Total</span>
          <span className="text-primary text-base">{formatCurrency(subtotal)}</span>
        </div>
      </div>
    </div>
  );
}