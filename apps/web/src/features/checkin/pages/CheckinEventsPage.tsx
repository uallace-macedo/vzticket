import { Link } from 'react-router-dom';
import { ScanLine, Loader2, Search, ArrowLeft } from 'lucide-react';
import { useCheckinEvents } from '../hooks/use-checkin-events';
import { EventCard } from '@/features/event/components/EventCards';
import { PAGES } from '@/constants/pages';

export function CheckinEventsPage() {
  const { events, isLoading, isError, search, setSearch, isOrganizer } = useCheckinEvents();

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <Link
        to={PAGES.PUBLIC.EVENTS}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </Link>

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl sm:text-3xl font-black text-foreground tracking-tight uppercase">
            PORTARIA & CHECK-IN
          </h1>
          <ScanLine className="w-6 h-6 text-primary shrink-0" />
        </div>

        {isOrganizer && setSearch !== undefined && (
          <div className="relative w-full sm:w-64 shrink-0">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted pointer-events-none" />
            <input
              type="text"
              placeholder="Buscar evento..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-background-muted border border-foreground/10 pl-8 pr-4 py-2 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition placeholder:font-normal"
            />
          </div>
        )}
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      ) : isError ? (
        <div className="text-center py-12 text-foreground-muted font-medium">
          Erro ao carregar eventos da portaria. Tente novamente mais tarde.
        </div>
      ) : events.length === 0 ? (
        <div className="text-center py-12 text-foreground-muted font-medium">
          Nenhum evento encontrado para check-in.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-2">
          {events.map((event) => (
            <Link
              key={event.id}
              to={PAGES.PRIVATE.CHECKIN.SCANNER(event.id)}
              className="block group"
            >
              <div className='pointer-events-none'>
                <EventCard event={event} />
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}