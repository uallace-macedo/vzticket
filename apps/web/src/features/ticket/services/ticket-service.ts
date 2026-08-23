import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { PurchaseTicketInput, PurchaseTicketResponse } from '../types/payment-types';

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
