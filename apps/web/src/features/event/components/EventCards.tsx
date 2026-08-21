import { Link } from 'react-router-dom'
import type { Event } from '../types';

interface EventCardProps {
  event: Event;
}

export function EventCard({ event }: EventCardProps) {
  const image = event.poster_url || event.custom_image_url || '/placeholder-event.jpg';

  const formattedDate = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(event.event_date));

  return (
    <Link to={`/events/${event.id}`} className="flex items-center gap-3.5 p-1.5">
      <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-2xl overflow-hidden shrink-0 bg-background-muted">
        <img
          src={image}
          alt={event.title}
          className="w-full h-full object-cover"
        />
      </div>

      <div className="flex flex-col justify-center space-y-1 overflow-hidden">
        <h3 className="font-medium text-sm sm:text-base text-fg line-clamp-2 leading-tight">
          {event.title}
        </h3>

        <div className="text-sm font-normal text-destructive capitalize">
          {formattedDate}
        </div>

        {event.city && (
          <div className="inline-flex items-center text-[10px] font-medium text-foreground-muted bg-foreground/5 px-2.5 py-1 rounded-full w-fit uppercase tracking-wider">
            {event.city}
          </div>
        )}
      </div>
    </Link>
  )
}