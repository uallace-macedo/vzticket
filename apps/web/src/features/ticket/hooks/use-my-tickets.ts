import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { TicketFilters, PaginatedTicketsResponse } from '../types';

export function useMyTickets(filters: TicketFilters = {}) {
  return useQuery<PaginatedTicketsResponse>({
    queryKey: ['my-tickets', filters],
    queryFn: async () => {
      const response = await api.get(ROUTES.TICKETS.MY, {
        params: {
          status: filters.status || undefined,
          page: filters.page || 1,
          per_page: filters.per_page || 10,
        },
      });
      return response.data;
    },
  });
}
