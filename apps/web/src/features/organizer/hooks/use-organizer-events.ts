import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useDebounce } from '@/hooks/use-debounce';
import { getOrganizerEvents } from '../services/organizer-services';

export function useOrganizerEvents() {
  const [page, setPage] = useState(1);
  const [title, setTitle] = useState('');

  const debouncedSearch = useDebounce(title, 500);
  const handleSearchChange = (value: string) => {
    setTitle(value);
    setPage(1);
  };

  const eventsQuery = useQuery({
    queryKey: ['organizer-events', { page, title: debouncedSearch }],
    queryFn: () =>
      getOrganizerEvents({
        page,
        per_page: 5,
        title: debouncedSearch || undefined,
      }),
  });

  return {
    events: eventsQuery.data?.items ?? [],
    eventsData: eventsQuery.data,
    totalEvents: eventsQuery.data?.total ?? 0,
    totalTicketsSold: eventsQuery.data?.total_tickets_sold ?? 0,
    isLoading: eventsQuery.isLoading,
    isRefetching: eventsQuery.isRefetching,
    refetch: eventsQuery.refetch,
    page,
    setPage,
    title,
    setTitle: handleSearchChange,
  };
}
