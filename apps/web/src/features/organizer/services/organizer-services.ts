import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type {
  CreateEventInput,
  CreateEventResponse,
  GetOrganizerEventsParams,
  PaginatedEventsResponse,
  TmdbSearchResponse,
  ViaCepResponse,
} from '../types/event-types';

export async function searchTmdbEvents(title: string, page = 1): Promise<TmdbSearchResponse> {
  const response = await api.get<TmdbSearchResponse>(ROUTES.EVENTS.TMDB, {
    params: { title, page },
  });
  return response.data;
}

export async function fetchAddressByCep(cep: string): Promise<ViaCepResponse> {
  const cleanCep = cep.replace(/\D/g, '');
  const response = await fetch(`https://viacep.com.br/ws/${cleanCep}/json/`);
  return response.json();
}

export async function createOrganizerEvent(data: CreateEventInput): Promise<CreateEventResponse> {
  const response = await api.post(ROUTES.EVENTS.CREATE, data);
  return response.data;
}

export async function getOrganizerEvents(params: GetOrganizerEventsParams): Promise<PaginatedEventsResponse> {
  const response = await api.get<PaginatedEventsResponse>(ROUTES.EVENTS.MY_EVENTS, {
    params,
  });
  return response.data;
}