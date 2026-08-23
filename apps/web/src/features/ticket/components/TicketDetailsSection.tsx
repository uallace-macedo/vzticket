import { Ticket, Calendar, ExternalLink } from 'lucide-react';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import type { UserTicket } from '../types';

interface TicketDetailsSectionProps {
  ticket: UserTicket;
}

const STATUS_MAP = {
  valid: { label: 'DISPONÍVEL', className: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' },
  used: { label: 'UTILIZADO', className: 'bg-foreground/10 text-foreground-muted border-foreground/10' },
  canceled: { label: 'CANCELADO', className: 'bg-rose-500/10 text-rose-500 border-rose-500/20' },
};

export function TicketDetailsSection({ ticket }: TicketDetailsSectionProps) {
  const { event } = ticket;

  const user = useAuthStore((state) => state.user);
  
  const userName = user?.name || user?.email || 'Usuário';

  const shortId = `#${ticket.id.slice(0, 7).toUpperCase()}`;
  const statusInfo = STATUS_MAP[ticket.status] || STATUS_MAP.valid;

  const formattedStartDate = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(event.event_date));

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-black text-foreground">Detalhes</h3>

      <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 space-y-3">
        <div className="flex items-start gap-3">
          <Ticket className="w-5 h-5 text-foreground shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h4 className="font-extrabold text-sm text-foreground">Ingresso</h4>
            <p className="text-xs text-foreground-muted leading-relaxed">
              {event.ticket_title} {event.ticket_description && `• ${event.ticket_description}`}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2 pt-1">
          <span className="text-[11px] font-bold text-foreground-muted bg-foreground/5 px-2.5 py-1 rounded-md border border-foreground/5">
            {shortId}
          </span>
          <span className={`text-[10px] font-black px-2.5 py-1 rounded-md border ${statusInfo.className}`}>
            {statusInfo.label}
          </span>
        </div>
      </div>

      <div className="bg-background-muted border border-foreground/10 rounded-2xl overflow-hidden divide-y divide-foreground/5">
        <div className="p-4 flex items-center gap-3 bg-foreground/[0.02]">
          <Calendar className="w-4 h-4 text-foreground-muted shrink-0" />
          <span className="text-xs font-semibold text-foreground-muted">
            Este ingresso pode ser válido para dias específicos do evento
          </span>
        </div>

        <div className="p-4 space-y-3 text-xs">
          <div className="flex justify-between items-center gap-4">
            <span className="font-bold text-foreground-muted">Evento</span>
            <span className="font-extrabold text-foreground text-right">{event.title}</span>
          </div>

          <div className="flex justify-between items-center gap-4">
            <span className="font-bold text-foreground-muted">Endereço</span>
            <span className="font-extrabold text-foreground text-right inline-flex items-center gap-1">
              {event.location_name}, {event.city} - {event.state}
              <ExternalLink className="w-3 h-3 text-foreground-muted" />
            </span>
          </div>

          <div className="flex justify-between items-center gap-4">
            <span className="font-bold text-foreground-muted">Começa</span>
            <span className="font-extrabold text-foreground text-right capitalize">{formattedStartDate}</span>
          </div>

          <div className="flex justify-between items-center gap-4">
            <span className="font-bold text-foreground-muted">Titular</span>
            <span className="font-extrabold text-foreground text-right uppercase">{userName}</span>
          </div>
        </div>
      </div>
    </div>
  );
}