import { z } from 'zod';

export const paymentMethodSchema = z.enum(['balance', 'pix']);

export const createEventSchema = z
  .object({
    title: z.string().min(3, 'Mínimo de 3 caracteres').max(150),
    description: z.string().min(10, 'Mínimo de 10 caracteres'),

    available_tickets: z.number('Informe a quantidade').int().min(1, 'Mínimo 1 ingresso'),
    ticket_price: z.number('Informe o valor').min(0, 'O valor não pode ser negativo'),
    ticket_title: z.string().max(100).default('Ingresso Geral'),
    ticket_description: z.string().optional().nullable(),

    event_date: z.string().min(1, 'Data e hora são obrigatórias'),
    sales_start_at: z.string().optional().nullable(),
    sales_end_at: z.string().optional().nullable(),

    location_name: z.string().min(1, 'Nome do local é obrigatório').max(150),
    cep: z.string().regex(/^\d{5}-\d{3}$/, 'Formato de CEP inválido (00000-000)'),
    address: z.string().min(1, 'Endereço é obrigatório').max(255),
    number: z.string().min(1, 'Número é obrigatório').max(20),
    neighborhood: z.string().min(1, 'Bairro é obrigatório').max(100),
    city: z.string().min(1, 'Cidade é obrigatória').max(100),
    state: z.string().length(2, 'UF deve ter 2 letras'),
    complement: z.string().optional().nullable(),

    poster_url: z.string().optional().nullable(),
    banner_url: z.string().optional().nullable(),
    custom_image_url: z.string().optional().nullable(),
    maps_url: z.url('URL do Google Maps inválida').min(1, 'URL do mapa é obrigatória'),

    payment_method: paymentMethodSchema.default('balance'),
  })
  .refine(
    (data) => {
      if (!data.poster_url && !data.banner_url) {
        return !!data.custom_image_url && data.custom_image_url.trim().length > 0;
      }
      return true;
    },
    {
      message: 'Imagem personalizada é obrigatória para eventos customizados',
      path: ['custom_image_url'],
    }
  );

export type CreateEventFormInput = z.input<typeof createEventSchema>;
export type CreateEventInput = z.infer<typeof createEventSchema>;

export interface TmdbMovie {
  id: number;
  title: string;
  original_title: string;
  overview: string;
  poster_url: string;
  backdrop_url: string;
}

export interface TmdbSearchResponse {
  page: number;
  total_pages: number;
  total_results: number;
  results: TmdbMovie[];
}

export interface ViaCepResponse {
  cep: string;
  logradouro: string;
  complemento: string;
  bairro: string;
  localidade: string;
  uf: string;
  ibge: string;
  gia: string;
  ddd: string;
  siafi: string;
  erro?: boolean;
}

export interface EventTicketInfo {
  title: string;
  description: string | null;
  available_tickets: number;
  ticket_price: number;
  service_fee: number;
  total_price: number;
}

export interface EventLocation {
  name: string;
  cep: string;
  address: string;
  number: string;
  neighborhood: string;
  city: string;
  state: string;
  complement: string | null;
  maps_url: string;
}

export interface EventMedia {
  poster_url: string | null;
  banner_url: string | null;
  custom_image_url: string | null;
}

export interface OrganizerEvent {
  id: string;
  title: string;
  description: string;
  status: 'active' | 'inactive' | 'cancelled';
  event_date: string;
  sales_start_at: string | null;
  sales_end_at: string | null;
  ticket_info: EventTicketInfo;
  location: EventLocation;
  media: EventMedia;
  created_at: string;
}

export interface PaginatedEventsResponse {
  items: OrganizerEvent[];
  total: number;
  page: number;
  pages: number;
  per_page: number;
  total_tickets_sold?: number;
}

export interface GetOrganizerEventsParams {
  page?: number;
  per_page?: number;
  title?: string;
}