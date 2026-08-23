import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { UserTicket } from '../types';

export function useTicketDetails(ticketId?: string) {
  return useQuery<UserTicket>({
    queryKey: ['ticket', ticketId],
    queryFn: async () => {
      if (!ticketId) throw new Error('ID do ingresso não informado');
      const response = await api.get(ROUTES.TICKETS.TICKET(ticketId));
      return response.data;
    },
    enabled: !!ticketId,
  });
}