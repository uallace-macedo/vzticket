import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Loader2, ArrowLeft } from 'lucide-react';
import { useEvent } from '../hooks/use-event';
import { EventHero } from '../components/EventHero';
import { EventDetails } from '../components/EventDetails';
import { TicketSelector } from '../components/TicketSelector';
import { EventFooter } from '../components/EventFooter';
import { EventOrganizerInfo } from '../components/EventOrganizerInfo';

export function EventDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: event, isLoading, isError } = useEvent(id || '');
  
  const [quantity, setQuantity] = useState(0);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    )
  }

  if (isError || !event) {
    return (
      <div className="max-w-md mx-auto text-center py-20 space-y-4 px-4">
        <h2 className="text-2xl font-black text-foreground">Evento não encontrado</h2>
        <p className="text-sm text-foreground-muted">
          O evento solicitado não existe ou foi removido.
        </p>
        <Link
          to="/"
          className="inline-flex items-center gap-2 bg-primary text-white font-bold text-sm px-5 py-2.5 rounded-full hover:opacity-90 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar para eventos</span>
        </Link>
      </div>
    )
  }

  const handleCheckout = () => {
    alert(`Iniciando checkout de ${quantity} ingresso(s) para ${event.title}`);
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-8">
      <Link
        to="/"
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </Link>

      <EventHero event={event} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        
        <div className="lg:col-span-2 space-y-8 order-1">
          <EventDetails event={event} />
          
          {event.organizer && (
            <div className="hidden lg:block">
              <EventOrganizerInfo organizer={event.organizer} />
            </div>
          )}
        </div>

        <div className="space-y-4 order-2">
          <h2 className="text-xl font-black text-foreground">Ingressos</h2>
          <TicketSelector
            price={event.ticket_price}
            availableTickets={event.available_tickets}
            quantity={quantity}
            onQuantityChange={setQuantity}
          />
        </div>

        {event.organizer && (
          <div className="order-3 lg:hidden col-span-1">
            <EventOrganizerInfo organizer={event.organizer} />
          </div>
        )}
      </div>

      <EventFooter
        ticketPrice={event.ticket_price}
        quantity={quantity}
        onCheckout={handleCheckout}
      />
    </div>
  )
}