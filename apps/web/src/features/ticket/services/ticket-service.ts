import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { PurchaseTicketInput, PurchaseTicketResponse } from '../types/payment-types';
import type { UserTicket } from '../types';

export async function purchaseTickets(
  eventId: string,
  data: PurchaseTicketInput
): Promise<PurchaseTicketResponse> {
  const response = await api.post<PurchaseTicketResponse>(
    ROUTES.TICKETS.PURCHASE(eventId),
    data
  );
  return response.data;
}

export async function cancelTicket(
  ticket_id: string
): Promise<UserTicket> {
  const response = await api.patch<UserTicket>(
    ROUTES.TICKETS.CANCEL(ticket_id)
  );
  return response.data;
}
