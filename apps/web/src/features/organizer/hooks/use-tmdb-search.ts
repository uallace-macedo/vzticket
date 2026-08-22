import { useQuery } from '@tanstack/react-query';
import { searchTmdbEvents } from '../services/organizer-services';
import { useDebounce } from '@/hooks/use-debounce';

export function useTmdbSearch(title: string, page = 1) {
  const debouncedTitle = useDebounce(title, 500);

  return useQuery({
    queryKey: ['tmdb-search', debouncedTitle, page],
    queryFn: () => searchTmdbEvents(debouncedTitle, page),
    enabled: Boolean(debouncedTitle.trim()),
    staleTime: 1000 * 60 * 5,
  });
}
