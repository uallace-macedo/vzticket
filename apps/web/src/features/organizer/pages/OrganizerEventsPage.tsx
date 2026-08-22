import { useState } from 'react';
import { Calendar, Plus, ArrowLeft, CalendarCheck2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { PAGES } from '@/constants/pages';
import { CreateEventModal } from '../components/CreateEventModal';
import type { CreateEventInput } from '../types/event-types';
import { useCreateEvent } from '../hooks/use-create-event';

export function OrganizerEventsPage() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { mutateAsync: createEvent, isPending } = useCreateEvent();

  const handleCreateEvent = async (data: CreateEventInput) => {
    await createEvent(data);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <Link
        to={PAGES.PUBLIC.HOME}
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

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-1">
          <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider">
            Eventos Criados
          </span>
          <p className="text-2xl sm:text-3xl font-black text-foreground">0</p>
        </div>

        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-1">
          <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider">
            Total de Ingressos Vendidos
          </span>
          <p className="text-2xl sm:text-3xl font-black text-foreground">0</p>
        </div>
      </div>

      <div className="flex flex-col items-center justify-center p-8 border border-dashed border-foreground/10 rounded-2xl bg-background-muted/30 text-center min-h-[250px]">
        <CalendarCheck2 className="w-10 h-10 text-foreground-muted mb-3" />
        <p className="text-sm font-bold text-foreground">Você ainda não possui eventos cadastrados.</p>
        <p className="text-xs text-foreground-muted mt-1 max-w-sm">
          Clique no botão &quot;Criar Evento&quot; para publicar e gerenciar ingressos.
        </p>
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