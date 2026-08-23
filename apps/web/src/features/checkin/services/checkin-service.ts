import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type { ValidateTicketParams, ValidateTicketResponse } from '../types';

export const checkinService = {
  async validateTicket(payload: ValidateTicketParams): Promise<ValidateTicketResponse> {
    const { data } = await api.post<ValidateTicketResponse>(
      ROUTES.GATEKEEPER.VALIDATE_TICKET,
      payload
    );
    return data;
  },
};
