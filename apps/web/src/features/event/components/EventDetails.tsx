import { Calendar, MapPin, Share2 } from 'lucide-react';
import type { Event } from '../types';
import { useState } from 'react';
import { ShareModal } from './ShareModal';

interface EventDetailsProps {
  event: Event;
}

export function EventDetails({ event }: EventDetailsProps) {
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  const formattedDate = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'long',
    day: '2-digit',
    month: 'long',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(event.event_date));

  const location = event.location;
  const fullAddress = `${location?.address || ''}${
    location?.number ? `, ${location.number}` : ''
  } - ${location?.city || ''} / ${location?.state || ''}`;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl sm:text-3xl font-black text-foreground uppercase tracking-tight">
        {event.title}
      </h1>

      <div className="space-y-3 text-sm font-semibold text-foreground-muted">
        <div className="flex items-center gap-2.5">
          <Calendar className="w-4 h-4 text-primary shrink-0" />
          <span className="capitalize">{formattedDate}</span>
        </div>

        <div className="flex items-center gap-2.5">
          <MapPin className="w-4 h-4 text-primary shrink-0" />
          {location?.maps_url ? (
            <a
              href={location.maps_url}
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-primary transition line-clamp-1"
            >
              {location.name} ({fullAddress})
            </a>
          ) : (
            <span className="line-clamp-1">
              {location?.name} ({fullAddress})
            </span>
          )}
        </div>
      </div>

      <div className="flex items-center gap-2 pt-2">
        <button
          onClick={() => setIsShareModalOpen(true)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-foreground/10 text-xs font-bold hover:bg-foreground/5 transition cursor-pointer"
        >
          <Share2 className="w-3.5 h-3.5" />
          <span>Compartilhar</span>
        </button>
      </div>

      <div className="space-y-2 pt-4 border-t border-foreground/10">
        <h2 className="text-lg font-extrabold text-foreground">Descrição</h2>
        <p className="text-sm text-foreground-muted leading-relaxed whitespace-pre-line">
          {event.description || 'Nenhuma descrição informada para este evento.'}
        </p>
      </div>

      <ShareModal
        isOpen={isShareModalOpen}
        onClose={() => setIsShareModalOpen(false)}
        eventTitle={event.title}
      />
    </div>
  );
}
