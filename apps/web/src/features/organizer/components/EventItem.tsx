import { Calendar, MapPin, Ticket } from 'lucide-react';
import type { OrganizerEvent } from '../types/event-types';

interface EventItemProps {
  event: OrganizerEvent;
}

export function EventItem({ event }: EventItemProps) {
  const formattedDate = event.event_date
    ? new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      }).format(new Date(event.event_date))
    : 'Data não informada';

  const imageUrl =
    event.media?.poster_url ||
    event.media?.custom_image_url ||
    event.media?.banner_url;

  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3.5 rounded-xl bg-background-muted border border-foreground/10 hover:border-foreground/20 transition gap-3">
      <div className="flex items-center gap-3 min-w-0 w-full sm:w-auto">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={event.title}
            className="w-12 h-12 rounded-lg object-cover shrink-0 bg-background"
          />
        ) : (
          <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center shrink-0">
            <Calendar className="w-5 h-5" />
          </div>
        )}

        <div className="min-w-0 space-y-0.5">
          <p className="text-xs sm:text-sm font-bold text-foreground truncate">
            {event.title}
          </p>

          <div className="flex items-center gap-2 text-[11px] text-foreground-muted flex-wrap">
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3 text-primary" />
              {formattedDate}
            </span>
            <span>•</span>
            <span className="flex items-center gap-1 truncate max-w-[200px]">
              <MapPin className="w-3 h-3 text-primary" />
              {event.location?.name || `${event.location?.city}, ${event.location?.state}`}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between sm:justify-end gap-3 w-full sm:w-auto shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-foreground/5">
        <div className="flex items-center gap-1.5 text-xs font-semibold text-foreground-muted bg-background/50 px-2.5 py-1 rounded-lg border border-foreground/5">
          <Ticket className="w-3.5 h-3.5 text-primary" />
          <span className="text-foreground font-bold">
            {event.ticket_info?.available_tickets ?? 0}
          </span>
          <span>disp.</span>
        </div>
      </div>
    </div>
  );
}