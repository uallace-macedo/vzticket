import { useState } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { useEvent } from '@/features/event/hooks/use-event';
import { usePurchaseTicket } from './use-purchase-ticket';
import type { PaymentMethod } from '../types/payment-types';
import type { Event } from '@/features/event/types';
import { useQueryClient } from '@tanstack/react-query';

export function useCheckout() {
  const queryClient = useQueryClient();
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
            queryClient.invalidateQueries({ queryKey: ['my-tickets'] })
          }
        },
        onError: (error) => {
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

  return {
    event,
    isLoadingEvent,
    quantity,
    paymentMethod,
    setPaymentMethod,
    errorMessage,
    paymentToken,
    isPixModalOpen,
    setIsPixModalOpen,
    isSuccess,
    isPending: purchaseMutation.isPending,
    handleFinishPurchase,
    navigate,
  };
}
