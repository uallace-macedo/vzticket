export const ROUTES = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    LOGOUT: '/api/v1/auth/logout'
  },
  EVENTS: {
    GET_ALL: '/api/v1/events',
    GET_BY_ID: (id: string) => `/api/v1/events/${id}`,
  }
}