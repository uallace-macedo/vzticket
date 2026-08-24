import { useState, useMemo } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Loader2, Sparkles, ArrowDown, MapPin } from 'lucide-react'
import { useEvents } from '../hooks/use-events'
import { EventCard } from '../components/EventCards'
import { useDebounce } from '@/hooks/use-debounce'

const UF_LIST = [
  'AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN',
  'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO'
]

export function EventsPage() {
  const [searchParams] = useSearchParams()
  const searchQuery = searchParams.get('query') || ''
  
  const [cityInput, setCityInput] = useState('')
  const [selectedState, setSelectedState] = useState('')

  const debouncedCity = useDebounce(cityInput, 500)

  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
  } = useEvents({
    title: searchQuery,
    city: debouncedCity || undefined,
    state: selectedState || undefined,
  })

  const allEvents = useMemo(() => {
    return data?.pages.flat() || []
  }, [data])

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <div className="flex items-center gap-2">
        <h1 className="text-2xl sm:text-3xl font-black text-foreground tracking-tight">
          EVENTOS
        </h1>
        <Sparkles className="w-6 h-6 text-primary animate-pulse" />
      </div>

      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        <div className="relative shrink-0">
          <select
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
            className="bg-background-muted border border-foreground/10 px-3 py-2 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition cursor-pointer appearance-none pr-8"
          >
            <option value="">Todos os estados</option>
            {UF_LIST.map((uf) => (
              <option key={uf} value={uf}>
                {uf}
              </option>
            ))}
          </select>
          <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px] text-foreground-muted">
            ▼
          </div>
        </div>

        <div className="relative shrink-0">
          <MapPin className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-foreground-muted pointer-events-none" />
          <input
            type="text"
            placeholder="Todas as cidades"
            value={cityInput}
            onChange={(e) => setCityInput(e.target.value)}
            className="bg-background-muted border border-foreground/10 pl-8 pr-4 py-2 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition placeholder:font-normal"
          />
        </div>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      ) : isError ? (
        <div className="text-center py-12 text-foreground-muted font-medium">
          Erro ao carregar eventos. Tente novamente mais tarde.
        </div>
      ) : allEvents.length === 0 ? (
        <div className="text-center py-12 text-foreground-muted font-medium">
          Nenhum evento encontrado.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-2">
          {allEvents.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      )}

      {hasNextPage && (
        <div className="flex justify-center pt-6">
          <button
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
            className="flex items-center gap-2 bg-background-muted border border-foreground/10 px-6 py-2.5 rounded-full font-bold text-sm hover:bg-foreground/5 transition cursor-pointer disabled:opacity-50"
          >
            {isFetchingNextPage ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
                <span>Carregando...</span>
              </>
            ) : (
              <>
                <ArrowDown className="w-4 h-4 text-foreground-muted" />
                <span>Ver mais</span>
              </>
            )}
          </button>
        </div>
      )}
    </div>
  )
}