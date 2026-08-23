export type TicketStatus = 'valid' | 'used' | 'canceled';

export interface EventMedia {
  poster_url?: string | null;
  banner_url?: string | null;
  custom_image_url?: string | null;
}

export interface TicketEventInfo {
  id: string;
  title: string;
  event_date: string;
  location_name: string;
  city: string;
  state: string;
  ticket_title: string;
  ticket_description?: string | null;
  media: EventMedia;
}

export interface UserTicket {
  id: string;
  event_id: string;
  user_id: string;
  qr_code_hash: string;
  share_token: string;
  status: TicketStatus;
  purchased_at: string;
  validated_at?: string | null;
  event: TicketEventInfo;
}

export interface TicketFilters {
  status?: TicketStatus;
  page?: number;
  per_page?: number;
}

export interface PaginatedTicketsResponse {
  items: UserTicket[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
