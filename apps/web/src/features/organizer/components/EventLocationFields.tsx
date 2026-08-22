import { useEffect, useState } from 'react';
import type { UseFormRegister, FieldErrors, UseFormSetValue, UseFormWatch } from 'react-hook-form';
import { MapPin, Loader2, Globe } from 'lucide-react';
import type { CreateEventFormInput } from '../types/event-types';
import { useAddressByCep } from '../hooks/use-address-by-cep';

interface EventLocationFieldsProps {
  register: UseFormRegister<CreateEventFormInput>;
  errors: FieldErrors<CreateEventFormInput>;
  setValue: UseFormSetValue<CreateEventFormInput>;
  watch: UseFormWatch<CreateEventFormInput>;
}

export function EventLocationFields({ register, errors, setValue, watch }: EventLocationFieldsProps) {
  const cepValue = watch('cep') || '';
  const [isAddressLocked, setIsAddressLocked] = useState(false);

  const { data: addressData, isLoading: isFetchingCep } = useAddressByCep(cepValue);

  const handleCepChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 8) value = value.slice(0, 8);
    if (value.length > 5) {
      value = `${value.slice(0, 5)}-${value.slice(5)}`;
    }
    setValue('cep', value, { shouldValidate: true });
  };

  useEffect(() => {
    if (addressData && !addressData.erro) {
      setValue('address', addressData.logradouro || '', { shouldValidate: true });
      setValue('neighborhood', addressData.bairro || '', { shouldValidate: true });
      setValue('city', addressData.localidade || '', { shouldValidate: true });
      setValue('state', addressData.uf || '', { shouldValidate: true });
      setIsAddressLocked(true);
    }
  }, [addressData, setValue]);

  return (
    <div className="space-y-4 pt-4 border-t border-foreground/10">
      <h3 className="text-xs font-bold text-primary uppercase tracking-wider flex items-center gap-2">
        <MapPin className="w-4 h-4" /> Localização
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-bold text-foreground mb-1">CEP *</label>
          <div className="relative">
            <input
              {...register('cep')}
              onChange={handleCepChange}
              maxLength={9}
              placeholder="00000-000"
              className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
            />
            {isFetchingCep && (
              <Loader2 className="w-4 h-4 animate-spin absolute right-3 top-3 text-primary" />
            )}
          </div>
          {errors.cep && <span className="text-xs text-destructive mt-1 block">{errors.cep.message}</span>}
        </div>

        <div className="sm:col-span-2">
          <label className="block text-xs font-bold text-foreground mb-1">Nome do Local *</label>
          <input
            {...register('location_name')}
            placeholder="Ex: Arena Fonte Nova"
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
          {errors.location_name && <span className="text-xs text-destructive mt-1 block">{errors.location_name.message}</span>}
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="sm:col-span-2">
          <label className="block text-xs font-bold text-foreground mb-1">Endereço *</label>
          <input
            {...register('address')}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Número *</label>
          <input
            {...register('number')}
            placeholder="123 ou S/N"
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Bairro *</label>
          <input
            {...register('neighborhood')}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">Cidade *</label>
          <input
            {...register('city')}
            disabled={isAddressLocked}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition disabled:opacity-60 disabled:cursor-not-allowed"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-foreground mb-1">UF *</label>
          <input
            {...register('state')}
            maxLength={2}
            disabled={isAddressLocked}
            className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm uppercase outline-none focus:border-primary transition disabled:opacity-60 disabled:cursor-not-allowed"
          />
        </div>
      </div>

      <div>
        <label className="block text-xs font-bold text-foreground mb-1 flex items-center gap-1.5">
          <Globe className="w-3.5 h-3.5 text-primary" /> Link do Google Maps (URL) *
        </label>
        <input
          {...register('maps_url')}
          placeholder="https://maps.google.com/..."
          className="w-full bg-background-muted border border-foreground/10 rounded-xl px-3.5 py-2.5 text-sm outline-none focus:border-primary transition"
        />
        {errors.maps_url && <span className="text-xs text-destructive mt-1 block">{errors.maps_url.message}</span>}
      </div>
    </div>
  );
}