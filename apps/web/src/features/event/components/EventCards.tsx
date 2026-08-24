import { Link, useNavigate } from 'react-router-dom';
import { ScanLine } from 'lucide-react';
import type { Event } from '../types';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { PAGES } from '@/constants/pages';

interface EventCardProps {
  event: Event;
}

export function EventCard({ event }: EventCardProps) {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  const isOrganizer = user?.role === 'organizer' && event.organizer.id === user.id;
  const isGatekeeper = user?.role === 'gatekeeper';
  const canAccessCheckin = isOrganizer || isGatekeeper;

  const image =
    event.media?.poster_url ||
    event.media?.custom_image_url ||
    '/placeholder-event.jpg';

  const formattedDate = new Intl.DateTimeFormat('pt-BR', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(event.event_date));

  const handleOpenCheckin = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    navigate(PAGES.PRIVATE.CHECKIN.SCANNER(event.id));
  };

  return (
    <div className="relative group rounded-2xl transition hover:bg-background-muted/50 p-1">
      <Link to={`/events/${event.id}`} className="flex items-center gap-3.5 p-1.5">
        <div className="relative w-20 h-20 sm:w-24 sm:h-24 rounded-2xl overflow-hidden shrink-0 bg-background-muted">
          <img
            src={image}
            alt={event.title}
            className="w-full h-full object-cover"
          />

          {canAccessCheckin && (
            <button
              type="button"
              onClick={handleOpenCheckin}
              title="Acessar Portaria"
              className="absolute top-1.5 left-1.5 p-1.5 bg-black/60 backdrop-blur-md text-white hover:bg-primary rounded-xl transition-all cursor-pointer shadow-sm z-10 opacity-0 group-hover:opacity-100 duration-200 ease-in-out"
            >
              <ScanLine className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        <div className="flex flex-col justify-center space-y-1 overflow-hidden pr-2">
          <h3 className="font-medium text-sm sm:text-base text-fg line-clamp-2 leading-tight">
            {event.title}
          </h3>

          <div className="text-sm font-normal text-destructive capitalize">
            {formattedDate}
          </div>

          {event.location?.city && (
            <div className="inline-flex items-center text-[10px] font-medium text-foreground-muted bg-foreground/5 px-2.5 py-1 rounded-full w-fit uppercase tracking-wider">
              {event.location.city}
            </div>
          )}
        </div>
      </Link>
    </div>
  );
}