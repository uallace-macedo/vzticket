export const PAGES = {
  PUBLIC: {
    HOME: '/',
    EVENTS: '/events',
    EVENT: '/events/:id',
    SHARED_TICKET: '/'
  },
  PRIVATE: {
    PROFILE: '/profile',
    WALLET: '/wallet',
    TICKETS: {
      BASE: '/tickets',
      TICKET: (ticket_id: string) => `/tickets/${ticket_id}`,
      TICKET_BASE: '/tickets/:ticket_id'
    },
    ORGANIZER: {
      EVENTS: '/organizer/events'
    },
    EVENTS: {
      CHECKOUT: (event_id: string) => `/events/${event_id}/checkout`,
      CHECKOUT_BASE: '/events/:event_id/checkout'
    },
  }
}