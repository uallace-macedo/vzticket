export type EventStatus = 'pending_fee' | 'active' | 'cancelled' | 'finished';

export interface EventTicketInfo {
  title: string;
  description: string;
  available_tickets: number;
  ticket_price: number;
  service_fee: number;
  total_price: number;
}

export interface EventLocation {
  name: string;
  cep: string;
  address: string;
  number: string;
  neighborhood: string;
  city: string;
  state: string;
  complement?: string | null;
  maps_url: string;
}

export interface EventMedia {
  poster_url?: string | null;
  banner_url?: string | null;
  custom_image_url?: string | null;
}

export interface EventOrganizer {
  id: string;
  name: string;
  email: string;
  image_url?: string | null;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  status: EventStatus;
  event_date: string;
  sales_start_at: string;
  sales_end_at: string;
  ticket_info: EventTicketInfo;
  location: EventLocation;
  media: EventMedia;
  organizer: EventOrganizer;
  created_at: string;
}

export interface FetchEventsParams {
  title?: string;
  city?: string;
  state?: string;
  limit?: number;
  offset?: number;
}
