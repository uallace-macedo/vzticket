import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createOrganizerEvent } from '../services/organizer-services';
import type { CreateEventInput } from '../types/event-types';

export function useCreateEvent() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateEventInput) => createOrganizerEvent(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['organizer-events'] });
    },
  });
}
