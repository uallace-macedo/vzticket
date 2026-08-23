import { useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useEvent } from '@/features/event/hooks/use-event';
import { useValidateTicket } from './use-validate-ticket';

export function useCheckin() {
  const { event_id = '' } = useParams<{ event_id: string }>();
  const [hashInput, setHashInput] = useState('');
  const [isScannerOpen, setIsScannerOpen] = useState(false);
  const [lastValidation, setLastValidation] = useState<{
    success: boolean;
    message: string;
    ticketInfo?: string;
  } | null>(null);

  const { data: event, isLoading: isLoadingEvent } = useEvent(event_id);
  const validateMutation = useValidateTicket();

  const handleValidate = useCallback(
    (customHash?: string) => {
      const targetHash = (customHash || hashInput).trim();
      if (!targetHash || !event_id || validateMutation.isPending) return;

      setIsScannerOpen(false);
      setLastValidation(null);

      validateMutation.mutate(
        {
          qr_code_hash: targetHash,
          event_id,
        },
        {
          onSuccess: (data) => {
            setLastValidation({
              success: true,
              message: data.message || 'Ingresso validado com sucesso!',
              ticketInfo: data.ticket?.user_name || data.ticket?.ticket_info?.title,
            });
            setHashInput('');
          },
          onError: (error: any) => {
            const apiMessage = error?.response?.data?.detail || error?.response?.data?.message;
            setLastValidation({
              success: false,
              message: apiMessage || 'Ingresso inválido ou já utilizado.',
            });
          },
        }
      );
    },
    [event_id, hashInput, validateMutation]
  );

  const handleNewScan = useCallback(() => {
    setLastValidation(null);
    setHashInput('');
    setIsScannerOpen(true);
  }, []);

  return {
    event,
    isLoadingEvent,
    hashInput,
    setHashInput,
    isScannerOpen,
    setIsScannerOpen,
    lastValidation,
    isPending: validateMutation.isPending,
    handleValidate,
    handleNewScan,
  };
}