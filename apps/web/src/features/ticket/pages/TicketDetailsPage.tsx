import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Loader2 } from 'lucide-react';
import { useTicketDetails } from '../hooks/use-ticket-details';
import { TicketQrCodeCard } from '../components/ticket/TicketQrCodeCard';
import { TicketDetailsSection } from '../components/ticket/TicketDetailsSection';
import { TicketOptionsSection } from '../components/ticket/TicketOptionsSection';
import { PAGES } from '@/constants/pages';

export function TicketDetailsPage() {
  const { ticket_id } = useParams<{ ticket_id: string }>();
  const navigate = useNavigate();

  const { data: ticket, isLoading, isError } = useTicketDetails(ticket_id);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (isError || !ticket) {
    return (
      <div className="max-w-md mx-auto text-center py-20 space-y-4 px-4">
        <h2 className="text-xl font-black text-foreground">Ingresso não encontrado</h2>
        <p className="text-xs text-foreground-muted">
          Não foi possível carregar as informações deste ingresso.
        </p>
        <Link
          to={PAGES.PRIVATE.TICKETS.BASE}
          className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 sm:py-8 space-y-8">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </button>

      <TicketQrCodeCard qrCodeHash={ticket.qr_code_hash} />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-4">
        <TicketDetailsSection ticket={ticket} />
        <TicketOptionsSection ticket={ticket} />
      </div>
    </div>
  );
}