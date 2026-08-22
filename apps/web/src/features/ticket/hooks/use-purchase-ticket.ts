import { useMutation } from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { PaymentMethod } from '../types';

interface PurchasePayload {
  quantity: number;
  payment_method: PaymentMethod;
}

export interface PurchaseResponse {
  message?: string;
  payment_token?: string;
  ticket_ids?: string[];
}

interface ApiErrorResponse {
  code?: string;
  detail?: string;
}

export function usePurchaseTicket({ eventId }: { eventId: string }) {
  return useMutation<PurchaseResponse, AxiosError<ApiErrorResponse>, PurchasePayload>({
    mutationFn: async (payload: PurchasePayload) => {
      const response = await api.post(ROUTES.TICKETS.PURCHASE(eventId), payload);
      return response.data;
    },
  });
}