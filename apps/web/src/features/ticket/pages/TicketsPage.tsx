import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader2, Ticket as TicketIcon } from 'lucide-react';
import { useMyTickets } from '../hooks/use-my-tickets';
import { TicketCard } from '../components/TicketCard';
import { TicketFilters } from '../components/TicketFilters';
import type { TicketStatus } from '../types';
import { PAGES } from '@/constants/pages';

export function TicketsPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState<TicketStatus | undefined>('valid');
  const [page, setPage] = useState(1);

  const { data, isLoading, isError } = useMyTickets({
    status,
    page,
    per_page: 12,
  });

  const tickets = data?.items || [];

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <div className="flex items-center gap-2 pb-4">
        <h1 className="text-2xl sm:text-3xl font-black text-foreground tracking-tight">
          MEUS INGRESSOS
        </h1>
        <TicketIcon className="w-6 h-6 text-primary" />
      </div>

      <TicketFilters selectedStatus={status} onSelectStatus={setStatus} />

      {isLoading ? (
        <div className="flex justify-center py-20">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      ) : isError ? (
        <div className="text-center py-16 text-foreground-muted font-medium">
          Erro ao carregar seus ingressos. Tente novamente mais tarde.
        </div>
      ) : tickets.length === 0 ? (
        <div className="text-center py-16 space-y-2">
          <p className="text-foreground font-bold text-base">Nenhum ingresso encontrado</p>
          <p className="text-foreground-muted text-xs">
            Você ainda não possui ingressos cadastrados nesta categoria.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tickets.map((ticket) => (
            <TicketCard
              key={ticket.id}
              ticket={ticket}
              onViewTicket={(t) => {
                navigate(PAGES.PRIVATE.TICKETS.TICKET(t.id))
              }}
            />
          ))}
        </div>
      )}

      {data && data.pages > 1 && (
        <div className="flex justify-center items-center gap-2 pt-6">
          <button
            onClick={() => setPage((p) => Math.max(p - 1, 1))}
            disabled={page === 1}
            className="px-4 py-2 text-xs font-bold bg-background-muted border border-foreground/10 rounded-lg disabled:opacity-40"
          >
            Anterior
          </button>
          <span className="text-xs font-bold text-foreground-muted">
            Página {page} de {data.pages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(p + 1, data.pages))}
            disabled={page === data.pages}
            className="px-4 py-2 text-xs font-bold bg-background-muted border border-foreground/10 rounded-lg disabled:opacity-40"
          >
            Próxima
          </button>
        </div>
      )}
    </div>
  );
}