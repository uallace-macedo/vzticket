import { useMemo } from 'react';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { useOrganizerEvents } from '@/features/organizer/hooks/use-organizer-events';
import { useEvents } from '@/features/event/hooks/use-events';
import type { Event } from '@/features/event/types';

export function useCheckinEvents() {
  const { user } = useAuthStore();
  const isOrganizer = user?.role === 'organizer';

  const organizerQuery = useOrganizerEvents();
  const gatekeeperQuery = useEvents();

  const events = useMemo<Event[]>(() => {
    if (isOrganizer) {
      return (organizerQuery.events || []).map((item: any) => {
        const normalizedEvent: Event = {
          id: item.id,
          title: item.title,
          description: item.description || '',
          status: item.status || 'active',
          event_date: item.event_date || item.date || new Date().toISOString(),
          sales_start_at: item.sales_start_at || new Date().toISOString(),
          sales_end_at: item.sales_end_at || new Date().toISOString(),
          created_at: item.created_at || new Date().toISOString(),
          media: {
            poster_url: item.media?.poster_url || item.poster_url || item.banner_url,
            custom_image_url: item.media?.custom_image_url,
            banner_url: item.media?.banner_url,
          },
          location: {
            name: item.location?.name || '',
            cep: item.location?.cep || '',
            address: item.location?.address || item.address || '',
            number: item.location?.number || '',
            neighborhood: item.location?.neighborhood || '',
            city: item.location?.city || item.city || '',
            state: item.location?.state || item.state || '',
            complement: item.location?.complement || null,
            maps_url: item.location?.maps_url || '',
          },
          ticket_info: item.ticket_info || {
            title: '',
            description: '',
            available_tickets: 0,
            ticket_price: 0,
            service_fee: 0,
            total_price: 0,
          },
          organizer: item.organizer || {
            id: user?.id || '',
            name: user?.name || '',
            email: user?.email || '',
            image_url: null,
          },
        };

        return normalizedEvent;
      });
    }

    return gatekeeperQuery.data?.pages.flat() || [];
  }, [isOrganizer, organizerQuery.events, gatekeeperQuery.data, user]);

  const isLoading = isOrganizer ? organizerQuery.isLoading : gatekeeperQuery.isLoading;
  const isError = isOrganizer ? false : gatekeeperQuery.isError;

  return {
    events,
    isLoading,
    isError,
    isOrganizer,
    search: isOrganizer ? organizerQuery.title : '',
    setSearch: isOrganizer ? organizerQuery.setTitle : undefined,
  };
}