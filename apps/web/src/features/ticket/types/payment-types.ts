export type PaymentMethod = 'balance' | 'pix';

export interface PurchaseTicketInput {
  quantity: number;
  payment_method: PaymentMethod;
}

export interface PurchasedTicket {
  id: string;
  event_id: string;
  user_id: string;
  qr_code_hash: string;
  share_token: string;
  status: 'valid' | 'used' | 'cancelled';
  purchased_at: string;
  validated_at: string | null;
}

export interface PurchaseTicketResponse {
  tickets: PurchasedTicket[];
  payment_method: PaymentMethod;
  payment_token: string | null;
}

export interface PurchaseTicketError {
  code: 'INSUFFICIENT_TICKETS' | 'INSUFFICIENT_BALANCE_FOR_TICKET' | 'EVENT_NOT_FOUND' | string;
  detail: string;
}
