import { useQuery } from '@tanstack/react-query';
import { fetchAddressByCep } from '../services/organizer-services';
import { useDebounce } from '@/hooks/use-debounce';

export function useAddressByCep(cep: string) {
  const debouncedCep = useDebounce(cep, 500);
  const cleanCep = debouncedCep.replace(/\D/g, '');

  return useQuery({
    queryKey: ['via-cep', cleanCep],
    queryFn: () => fetchAddressByCep(cleanCep),
    enabled: cleanCep.length === 8,
    staleTime: Infinity,
  });
}
