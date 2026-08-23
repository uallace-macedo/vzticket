import { useState } from 'react';
import { useParams, useLocation, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { useEvent } from '@/features/event/hooks/use-event';
import { usePurchaseTicket } from '../hooks/use-purchase-ticket';
import { CheckoutEventSummary } from '../components/CheckoutEventSummary';
import { CheckoutPaymentMethod } from '../components/CheckoutPaymentMethod';
import { PixPaymentModal } from '../components/PixPaymentModal';
import type { PaymentMethod } from '../types/payment-types';
import type { Event } from '@/features/event/types';

export function CheckoutPage() {
  const { eventId = '' } = useParams<{ eventId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, openAuthModal } = useAuthStore();

  const stateData = location.state as { quantity?: number; event?: Event } | null;
  const quantity = stateData?.quantity || 1;

  const { data: fetchedEvent, isLoading: isLoadingEvent } = useEvent(
    stateData?.event ? '' : eventId
  );

  const event = stateData?.event || fetchedEvent;
  const currentEventId = eventId || event?.id || '';

  const purchaseMutation = usePurchaseTicket({ eventId: currentEventId });

  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>('balance');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [paymentToken, setPaymentToken] = useState<string | null>(null);
  const [isPixModalOpen, setIsPixModalOpen] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleFinishPurchase = () => {
    if (!user) {
      toast.error('Você precisa estar logado para comprar ingressos.');
      openAuthModal();
      return;
    }

    if (!currentEventId) {
      toast.error('ID do evento inválido.');
      return;
    }

    setErrorMessage(null);

    purchaseMutation.mutate(
      { quantity, payment_method: paymentMethod },
      {
        onSuccess: (data) => {
          if (paymentMethod === 'pix' && data.payment_token) {
            setPaymentToken(data.payment_token);
            setIsPixModalOpen(true);
          } else {
            setIsSuccess(true);
          }
        },
        onError: (error) => {
          console.error("Erro na requisição de compra:", error);
          console.error("Dados da resposta do servidor:", error.response?.data);
          const code = error.response?.data?.code;
          const detail = error.response?.data?.detail;

          if (code === 'INSUFFICIENT_BALANCE_FOR_TICKET') {
            setErrorMessage('Saldo insuficiente na carteira para concluir a compra.');
          } else if (code === 'INSUFFICIENT_TICKETS') {
            setErrorMessage('A quantidade de ingressos solicitada não está mais disponível.');
          } else {
            setErrorMessage(detail || 'Ocorreu um erro ao processar sua compra.');
          }
        },
      }
    );
  };

  if (isLoadingEvent && !event) {
    return (
      <div className="max-w-2xl mx-auto py-20 text-center font-bold text-foreground-muted">
        Carregando informações do checkout...
      </div>
    );
  }

  if (!event) {
    return (
      <div className="max-w-md mx-auto text-center py-20 space-y-4 px-4">
        <h2 className="text-xl font-black text-foreground">Evento não encontrado</h2>
        <Link
          to="/"
          className="inline-flex items-center gap-2 bg-primary text-white font-bold text-xs px-4 py-2 rounded-full"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar ao início</span>
        </Link>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="max-w-md mx-auto py-16 px-4 text-center space-y-5 animate-in fade-in duration-300">
        <div className="w-16 h-16 bg-emerald-500/10 text-emerald-500 rounded-full flex items-center justify-center mx-auto">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-black text-foreground">Compra Confirmada!</h2>
        <p className="text-xs text-foreground-muted">
          Seus ingressos já foram gerados e estão disponíveis na sua carteira de ingressos.
        </p>
        <button
          onClick={() => navigate('/my-tickets')}
          className="w-full bg-primary text-white font-extrabold py-3 rounded-xl hover:opacity-90 transition text-sm cursor-pointer"
        >
          Ver meus ingressos
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar ao evento</span>
      </button>

      <h1 className="text-2xl font-black text-foreground">Checkout</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <CheckoutEventSummary event={event} quantity={quantity} />

        <CheckoutPaymentMethod
          selectedMethod={paymentMethod}
          onSelectMethod={setPaymentMethod}
          onSubmit={handleFinishPurchase}
          isPending={purchaseMutation.isPending}
          errorMessage={errorMessage}
        />
      </div>

      {paymentToken && (
        <PixPaymentModal
          isOpen={isPixModalOpen}
          onClose={() => setIsPixModalOpen(false)}
          paymentToken={paymentToken}
          onPaidClick={() => {
            setIsPixModalOpen(false);
            navigate('/my-tickets');
          }}
        />
      )}
    </div>
  );
}