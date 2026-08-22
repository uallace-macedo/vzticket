export const PAGES = {
  PUBLIC: {
    HOME: '/',
    EVENTS: '/events',
    EVENT: '/events/:id'
  },
  PRIVATE: {
    PROFILE: '/profile',
    WALLET: '/wallet',
    TICKETS: '/tickets',
    ORGANIZER: {
      EVENTS: '/organizer/events'
    },
    EVENTS: {
      CHECKOUT: (event_id: string) => `/events/${event_id}/checkout`,
      CHECKOUT_BASE: '/events/:event_id/checkout'
    }
  }
}