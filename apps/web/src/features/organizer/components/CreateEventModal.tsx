import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { X, Loader2, Sparkles, Image as ImageIcon } from 'lucide-react';
import { toast } from 'sonner';
import {
  createEventSchema,
  type CreateEventInput,
  type CreateEventFormInput,
  type TmdbMovie,
} from '../types/event-types';

import { EventInfoFields } from './EventInfoFields';
import { EventLocationFields } from './EventLocationFields';
import { EventTicketFields } from './EventTicketFields';
import { EventDateFields } from './EventDateFields';
import { TmdbSearchSidebar } from './TmdbSearchSidebar';
import { EventPreviewHero } from './EventPreviewHero';

interface CreateEventModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: CreateEventInput) => Promise<void>;
  isLoading?: boolean;
}

export function CreateEventModal({ isOpen, onClose, onSubmit, isLoading }: CreateEventModalProps) {
  const [mode, setMode] = useState<'tmdb' | 'custom'>('tmdb');
  const [selectedMovie, setSelectedMovie] = useState<TmdbMovie | null>(null);

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
    reset,
  } = useForm<CreateEventFormInput>({
    resolver: zodResolver(createEventSchema),
    defaultValues: {
      ticket_title: 'Ingresso Geral',
      payment_method: 'balance',
    },
  });

  if (!isOpen) return null;

  const currentTitle = watch('title');
  const currentPoster = watch('poster_url') || watch('custom_image_url');
  const currentBanner = watch('banner_url') || currentPoster;

  const handleSelectMovie = (movie: TmdbMovie) => {
    setSelectedMovie(movie);
    setValue('title', movie.title, { shouldValidate: true });
    setValue('description', movie.overview, { shouldValidate: true });
    setValue('poster_url', movie.poster_url, { shouldValidate: true });
    setValue('banner_url', movie.backdrop_url, { shouldValidate: true });
  };

  const handleSwitchToTmdb = () => {
    setMode('tmdb');
    setValue('custom_image_url', '', { shouldValidate: false });
  };

  const handleSwitchToCustom = () => {
    setMode('custom');
    setSelectedMovie(null);
    setValue('title', '', { shouldValidate: false });
    setValue('description', '', { shouldValidate: false });
    setValue('poster_url', null, { shouldValidate: false });
    setValue('banner_url', null, { shouldValidate: false });
  };

  const handleFormSubmit = async (data: CreateEventFormInput) => {
    try {
      const eventDateIso = data.event_date ? new Date(data.event_date).toISOString() : new Date().toISOString();
      const salesStartAtIso = data.sales_start_at
        ? new Date(data.sales_start_at).toISOString()
        : new Date().toISOString();

      const salesEndAtIso = data.sales_end_at
        ? new Date(data.sales_end_at).toISOString()
        : eventDateIso;

      const payloadData: CreateEventFormInput = {
        ...data,
        event_date: eventDateIso,
        sales_start_at: salesStartAtIso,
        sales_end_at: salesEndAtIso,
        poster_url: mode === 'custom' ? data.custom_image_url : data.poster_url,
        banner_url: mode === 'custom' ? data.custom_image_url : data.banner_url,
      };

      const parsedData = createEventSchema.parse(payloadData);

      await onSubmit(parsedData);
      reset();
      setSelectedMovie(null);
      onClose();
    } catch (error) {
      toast.error('Ocorreu um erro ao processar os dados do evento.');
    }
  };

  const handleFormInvalid = () => {
    toast.error('Por favor, preencha corretamente todos os campos obrigatórios.');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm overflow-y-auto">
      <div className="bg-background border border-foreground/10 w-full max-w-5xl rounded-3xl shadow-2xl overflow-hidden my-6 flex flex-col max-h-[90vh]">
        <div className="p-4 sm:p-5 border-b border-foreground/10 flex items-center justify-between bg-background-muted/50 shrink-0">
          <div className="flex items-center gap-3">
            <h2 className="text-base sm:text-lg font-black text-foreground">Criar Evento</h2>
            <div className="flex bg-background border border-foreground/10 rounded-xl p-1 gap-1">
              <button
                type="button"
                onClick={handleSwitchToTmdb}
                className={`px-3 py-1 text-xs font-bold rounded-lg flex items-center gap-1.5 transition cursor-pointer ${
                  mode === 'tmdb' ? 'bg-primary text-white' : 'text-foreground-muted hover:text-foreground'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" /> TMDB
              </button>
              <button
                type="button"
                onClick={handleSwitchToCustom}
                className={`px-3 py-1 text-xs font-bold rounded-lg flex items-center gap-1.5 transition cursor-pointer ${
                  mode === 'custom' ? 'bg-primary text-white' : 'text-foreground-muted hover:text-foreground'
                }`}
              >
                <ImageIcon className="w-3.5 h-3.5" /> Personalizado
              </button>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-full hover:bg-foreground/5 text-foreground-muted transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex flex-col lg:flex-row flex-1 overflow-hidden">
          {mode === 'tmdb' && (
            <TmdbSearchSidebar onSelectMovie={handleSelectMovie} selectedMovieId={selectedMovie?.id} />
          )}

          <form
            onSubmit={handleSubmit(handleFormSubmit, handleFormInvalid)}
            className="flex-1 p-6 overflow-y-auto space-y-6"
          >
            <EventPreviewHero posterUrl={currentPoster} bannerUrl={currentBanner} title={currentTitle} />

            <EventInfoFields register={register as any} errors={errors as any} />

            {mode === 'custom' && (
              <div>
                <label className="block text-xs font-bold text-foreground mb-1">
                  URL da Imagem da Capa (Custom Image URL) *
                </label>
                <input
                  {...register('custom_image_url')}
                  placeholder="https://sua-imagem.com/poster.jpg"
                  className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
                />
                {errors.custom_image_url && (
                  <span className="text-xs text-destructive mt-1 block">{errors.custom_image_url.message}</span>
                )}
              </div>
            )}

            <EventLocationFields
              register={register as any}
              errors={errors as any}
              setValue={setValue as any}
              watch={watch as any}
            />

            <EventTicketFields register={register as any} errors={errors as any} watch={watch as any} />

            <EventDateFields register={register as any} errors={errors as any} />

            <div className="pt-4 border-t border-foreground/10 flex justify-end gap-3">
              <button
                type="button"
                onClick={onClose}
                className="px-5 py-2.5 rounded-xl border border-foreground/10 font-bold text-xs hover:bg-foreground/5 transition cursor-pointer"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="px-5 py-2.5 rounded-xl bg-primary text-white font-bold text-xs hover:brightness-90 transition disabled:opacity-50 cursor-pointer flex items-center gap-2"
              >
                {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
                <span>Criar Evento</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}