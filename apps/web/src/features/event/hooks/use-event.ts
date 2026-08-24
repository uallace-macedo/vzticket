import { useQuery } from '@tanstack/react-query'
import { fetchEventById } from '../services/event-services'

export function useEvent(id: string) {
  return useQuery({
    queryKey: ['event', id],
    queryFn: () => fetchEventById(id),
    enabled: Boolean(id),
    staleTime: 1000 * 60 * 5,
  })
}
