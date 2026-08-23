import { useNavigate } from 'react-router-dom';
import { Info, Ticket, QrCode } from 'lucide-react';
import type { UserTicket } from '../types';
import { PAGES } from '@/constants/pages';

interface TicketCardProps {
  ticket: UserTicket;
  onViewTicket?: (ticket: UserTicket) => void;
}

const STATUS_MAP = {
  valid: { label: 'DISPONÍVEL', className: 'bg-emerald-500/10 text-emerald-600 border-emerald-500/20' },
  used: { label: 'UTILIZADO', className: 'bg-foreground/10 text-foreground-muted border-foreground/10' },
  canceled: { label: 'CANCELADO', className: 'bg-rose-500/10 text-rose-500 border-rose-500/20' },
};

export function TicketCard({ ticket, onViewTicket }: TicketCardProps) {
  const navigate = useNavigate();
  const { event } = ticket;

  const media = event.media;
  const imageUrl = media.banner_url || media.custom_image_url || media.poster_url;

  const formattedDate = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(event.event_date));

  const statusInfo = STATUS_MAP[ticket.status] || STATUS_MAP.valid;
  const shortId = `#${ticket.id.slice(0, 7).toUpperCase()}`;

  return (
    <div className="bg-background-muted border border-foreground/10 rounded-2xl overflow-hidden flex flex-col justify-between hover:border-foreground/20 transition group">
      <div>
        <div className="relative aspect-video w-full overflow-hidden bg-foreground/5">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={event.title}
              className="w-full h-full object-cover group-hover:scale-105 transition duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-foreground-muted">
              <Ticket className="w-10 h-10 opacity-30" />
            </div>
          )}
        </div>

        <div className="p-4 space-y-3">
          <div>
            <h3 className="text-base font-black text-foreground line-clamp-1">
              {event.title}
            </h3>
            <div className="flex items-center gap-1.5 text-xs text-foreground-muted font-medium mt-0.5">
              <span>{formattedDate}</span>
              <Info className="w-3.5 h-3.5" />
            </div>
          </div>

          <div className="bg-background/60 border border-foreground/5 rounded-xl p-3 space-y-2">
            <div className="flex items-start gap-2.5">
              <Ticket className="w-4 h-4 text-foreground shrink-0 mt-0.5" />
              <div className="text-xs min-w-0">
                <p className="font-extrabold text-foreground truncate">{event.ticket_title}</p>
                <p className="text-foreground-muted line-clamp-2 leading-relaxed text-[11px]">
                  {event.ticket_description}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 pt-1">
              <span className="text-[11px] font-bold text-foreground-muted bg-foreground/5 px-2 py-0.5 rounded-md border border-foreground/5">
                {shortId}
              </span>
              <span
                className={`text-[10px] font-black px-2 py-0.5 rounded-md border ${statusInfo.className}`}
              >
                {statusInfo.label}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-4 pt-0">
        <button
          onClick={() => onViewTicket ? onViewTicket(ticket) : navigate(PAGES.PRIVATE.TICKETS.TICKET(ticket.id))}
          className="w-full bg-foreground text-background font-extrabold py-3 px-4 rounded-xl hover:opacity-90 transition flex items-center justify-center gap-2 text-xs cursor-pointer"
        >
          <span>Ver Ingresso</span>
          <QrCode className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}