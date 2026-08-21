export interface EventOrganizer {
  id: string
  name: string
  email: string
}

export interface Event {
  id: string
  title: string
  description: string
  available_tickets: number
  ticket_price: number
  event_date: string
  location_name: string
  cep: string
  address: string
  number: string
  neighborhood: string
  city: string
  state: string
  complement?: string
  maps_url: string
  poster_url?: string
  banner_url?: string
  custom_image_url?: string
  organizer: EventOrganizer
}

export interface FetchEventsParams {
  title?: string
  city?: string
  state?: string
  limit?: number
  offset?: number
}
