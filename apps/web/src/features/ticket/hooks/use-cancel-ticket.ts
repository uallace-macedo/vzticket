import { useMutation, useQueryClient } from "@tanstack/react-query";
import type { UserTicket } from "../types";
import { AxiosError } from "axios";
import type { ErrorResponse } from "@/constants/types";
import { cancelTicket } from "../services/ticket-service";
import { toast } from "sonner";
import { useNavigate } from "react-router-dom";
import { PAGES } from "@/constants/pages";

export function useCancelTicket() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  return useMutation<UserTicket, AxiosError<ErrorResponse>, { ticketId: string }>({
    mutationFn: async ({ ticketId }) => {
      return await cancelTicket(ticketId);
    },
    onSuccess: (updatedTicket) => {
      queryClient.invalidateQueries({ queryKey: ['user-tickets'] });
      queryClient.invalidateQueries({ queryKey: ['wallet', 'wallet-claims'] });
      queryClient.setQueryData(['ticket', updatedTicket.id], updatedTicket);

      toast.success('Ingresso cancelado com sucesso!', {
        description: 'O reembolso do valor foi processado para a sua conta.',
        duration: 2000
      });

      navigate(PAGES.PRIVATE.TICKETS.BASE);
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Não foi possível cancelar o ingresso.';

      toast.error('Erro ao cancelar', {
        description: message,
        duration: 2000
      })
    }
  })
}
