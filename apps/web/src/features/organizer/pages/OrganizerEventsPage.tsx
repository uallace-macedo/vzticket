import { useState } from 'react';
import {
  Calendar,
  Plus,
  ArrowLeft,
  CalendarCheck2,
  Search,
  Loader2,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { PAGES } from '@/constants/pages';
import { CreateEventModal } from '../components/CreateEventModal';
import { EventItem } from '../components/EventItem';
import type { CreateEventInput } from '../types/event-types';
import { useCreateEvent } from '../hooks/use-create-event';
import { useOrganizerEvents } from '../hooks/use-organizer-events';

export function OrganizerEventsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const {
    events,
    eventsData,
    totalEvents,
    totalTicketsSold,
    isLoading,
    isRefetching,
    refetch,
    page,
    setPage,
    title,
    setTitle,
  } = useOrganizerEvents();

  const { mutateAsync: createEvent, isPending } = useCreateEvent();

  const handleCreateEvent = async (data: CreateEventInput) => {
    await createEvent(data);
    setIsModalOpen(false);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <Link
        to={PAGES.PUBLIC.EVENTS}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </Link>

      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl sm:text-3xl font-black text-foreground tracking-tight uppercase">
            Meus Eventos
          </h1>
          <Calendar className="w-6 h-6 text-primary" />
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center gap-1.5 bg-primary text-primary-foreground font-bold text-xs px-3.5 py-2 rounded-full hover:bg-primary/90 transition cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Criar Evento</span>
        </button>
      </div>

      <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 flex items-center justify-between">
        <div className="space-y-1">
          <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider">
            Eventos Criados
          </span>
          <p className="text-2xl sm:text-3xl font-black text-foreground">
            {isLoading ? '---' : totalEvents}
          </p>
        </div>

        <button
          onClick={() => refetch()}
          title="Atualizar dados"
          className="p-2 rounded-xl hover:bg-foreground/5 text-foreground-muted hover:text-foreground transition cursor-pointer"
        >
          <RefreshCw
            className={`w-4 h-4 ${isRefetching ? 'animate-spin text-primary' : ''}`}
          />
        </button>
      </div>

      <div className="space-y-3">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pb-2 border-b border-foreground/10 min-h-[38px]">
          <h2 className="text-base font-bold text-foreground">
            Lista de Eventos
          </h2>

          <div className="relative w-full sm:w-64">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted" />
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Buscar evento por nome..."
              className="w-full bg-background-muted border border-foreground/10 rounded-full pl-9 pr-3 py-1.5 text-xs font-semibold text-foreground placeholder:text-foreground-muted outline-none focus:border-primary transition"
            />
          </div>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <Loader2 className="w-6 h-6 animate-spin text-primary" />
          </div>
        ) : events.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 border border-dashed border-foreground/10 rounded-2xl bg-background-muted/30 text-center min-h-[250px]">
            <CalendarCheck2 className="w-10 h-10 text-foreground-muted mb-3" />
            <p className="text-sm font-bold text-foreground">
              {title ? 'Nenhum evento encontrado.' : 'Você ainda não possui eventos cadastrados.'}
            </p>
            <p className="text-xs text-foreground-muted mt-1 max-w-sm">
              {title
                ? 'Tente buscar por outro termo ou limpe a caixa de pesquisa.'
                : 'Clique no botão "Criar Evento" para publicar e gerenciar ingressos.'}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {events.map((event) => (
              <EventItem key={event.id} event={event} />
            ))}
          </div>
        )}

        {eventsData && eventsData.pages > 1 && (
          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-foreground-muted font-medium">
              Página {eventsData.page} de {eventsData.pages}
            </span>

            <div className="flex items-center gap-1">
              <button
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                disabled={page >= eventsData.pages}
                onClick={() => setPage(page + 1)}
                className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      <CreateEventModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateEvent}
        isLoading={isPending}
      />
    </div>
  );
}