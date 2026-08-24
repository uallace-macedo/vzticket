import { useInfiniteQuery } from '@tanstack/react-query';
import { fetchEvents } from '../services/event-services';
import type { Event } from '../types';

const LIMIT = 9;

interface UseEventsFilters {
  title?: string
  city?: string
  state?: string
}

export function useEvents(filters?: UseEventsFilters) {
  return useInfiniteQuery<Event[], Error>({
    queryKey: ['events', filters],
    queryFn: ({ pageParam = 0 }) =>
      fetchEvents({
        title: filters?.title || undefined,
        city: filters?.city || undefined,
        state: filters?.state || undefined,
        limit: LIMIT,
        offset: pageParam as number,
      }),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      if (lastPage.length < LIMIT) return undefined;
      return allPages.length * LIMIT;
    },
    staleTime: 1000 * 60 * 5,
  })
}
