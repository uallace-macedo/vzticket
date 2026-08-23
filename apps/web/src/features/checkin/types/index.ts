export interface ValidateTicketParams {
  qr_code_hash: string;
  event_id: string;
}

export interface ValidateTicketResponse {
  message?: string;
  ticket?: {
    id: string;
    status: string;
    user_name?: string;
    ticket_info?: {
      title: string;
    };
  };
}