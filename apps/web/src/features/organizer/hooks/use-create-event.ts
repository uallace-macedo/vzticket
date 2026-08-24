import { useMutation, useQueryClient } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { toast } from 'sonner';
import { createOrganizerEvent } from '../services/organizer-services';
import type { CreateEventInput, CreateEventResponse } from '../types/event-types';
import type { ErrorResponse } from '@/constants/types';
import { useNavigate } from 'react-router-dom';
import { PAGES } from '@/constants/pages';

export function useCreateEvent() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateEventInput) => createOrganizerEvent(data),
    onSuccess: (res: CreateEventResponse) => {
      queryClient.invalidateQueries({ queryKey: ['organizer-events'] });
      const msg = res.payment_method == 'balance' 
        ? 'Evento criado com sucesso!'
        : 'Pix gerado. Confira-o em sua conta digital!'
      toast.success(msg, { duration: 2000 });

      if (res.payment_method == 'pix') {
        navigate(PAGES.PRIVATE.WALLET)
      }
    },
    onError: (error: unknown) => {
      let message = 'Ocorreu um erro ao processar os dados do evento.';

      if (error instanceof AxiosError && error.response?.data) {
        const data = error.response.data as ErrorResponse;
        if (typeof data.detail === 'string') {
          message = data.detail;
        } else if (Array.isArray(data.detail) && data.detail) {
          message = data.detail;
        }
      }

      toast.error(message);
    },
  });
}