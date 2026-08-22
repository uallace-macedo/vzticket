import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type {
  CreateEventInput,
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

export async function createOrganizerEvent(data: CreateEventInput): Promise<void> {
  await api.post(ROUTES.EVENTS.CREATE, data);
}
