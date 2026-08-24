import { useMutation } from '@tanstack/react-query';
import { checkinService } from '../services/checkin-service';
import type { ValidateTicketParams } from '../types';

export function useValidateTicket() {
  return useMutation({
    mutationFn: (payload: ValidateTicketParams) => checkinService.validateTicket(payload),
  });
}
