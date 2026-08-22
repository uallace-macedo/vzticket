import { useState, useRef } from 'react';
import { Search, Loader2, ChevronLeft, ChevronRight, Film, Check } from 'lucide-react';
import { useTmdbSearch } from '../hooks/use-tmdb-search';
import type { TmdbMovie } from '../types/event-types';

interface TmdbSearchSidebarProps {
  onSelectMovie: (movie: TmdbMovie) => void;
  selectedMovieId?: number;
}

export function TmdbSearchSidebar({ onSelectMovie, selectedMovieId }: TmdbSearchSidebarProps) {
  const [query, setQuery] = useState('');
  const [page, setPage] = useState(1);
  const [isOpen, setIsOpen] = useState(false);
  const blurTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const { data, isLoading } = useTmdbSearch(query, page);

  const handleFocus = () => {
    if (blurTimeoutRef.current) clearTimeout(blurTimeoutRef.current);
    setIsOpen(true);
  };

  const handleBlur = () => {
    blurTimeoutRef.current = setTimeout(() => {
      setIsOpen(false);
    }, 200);
  };

  const handleSelect = (movie: TmdbMovie) => {
    onSelectMovie(movie);
    setIsOpen(false);
  };

  return (
    <div className="w-full lg:w-80 bg-background-muted/40 border-b lg:border-b-0 lg:border-r border-foreground/10 p-4 flex flex-col space-y-3 shrink-0">
      <div className="space-y-1">
        <h3 className="text-sm font-bold text-foreground flex items-center gap-1.5">
          <Film className="w-4 h-4 text-primary" /> Buscar no TMDB
        </h3>
        <p className="text-[11px] text-foreground-muted">Clique na busca para ver os resultados.</p>
      </div>

      <div className="relative">
        <Search className="w-4 h-4 absolute left-3 top-3 text-foreground-muted" />
        <input
          value={query}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onChange={(e) => {
            setQuery(e.target.value);
            setPage(1);
            setIsOpen(true);
          }}
          placeholder="Ex: O Hobbit, Matrix..."
          className="w-full bg-background border border-foreground/10 rounded-xl pl-9 pr-3 py-2 text-xs outline-none focus:border-primary transition"
        />
        {isLoading && <Loader2 className="w-4 h-4 animate-spin absolute right-3 top-2.5 text-primary" />}
      </div>

      {isOpen && (
        <div
          onMouseDown={(e) => e.preventDefault()}
          className="flex-1 overflow-y-auto space-y-2 max-h-[300px] lg:max-h-none"
        >
          {!data && !isLoading && (
            <div className="text-center py-6 text-xs text-foreground-muted">
              Digite o nome de uma obra para buscar.
            </div>
          )}

          {data?.results.map((movie) => {
            const isSelected = selectedMovieId === movie.id;

            return (
              <div
                key={movie.id}
                onClick={() => handleSelect(movie)}
                className={`flex items-center gap-3 p-2 rounded-xl border transition cursor-pointer ${
                  isSelected
                    ? 'border-primary bg-primary/10'
                    : 'border-foreground/5 bg-background hover:border-foreground/20'
                }`}
              >
                <img
                  src={movie.poster_url || '/placeholder-event.jpg'}
                  alt={movie.title}
                  className="w-10 h-14 object-cover rounded-lg shrink-0 bg-background-muted"
                />
                <div className="min-w-0 flex-1 space-y-0.5">
                  <p className="text-xs font-bold text-foreground line-clamp-1">{movie.title}</p>
                  <p className="text-[10px] text-foreground-muted line-clamp-2">{movie.overview}</p>
                </div>
                {isSelected && <Check className="w-4 h-4 text-primary shrink-0 mr-1" />}
              </div>
            );
          })}

          {data && data.total_pages > 1 && (
            <div className="flex items-center justify-between pt-2 border-t border-foreground/10">
              <span className="text-[11px] text-foreground-muted">
                Pág. {data.page} de {data.total_pages}
              </span>
              <div className="flex items-center gap-1">
                <button
                  type="button"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}
                  className="p-1 rounded-lg border border-foreground/10 disabled:opacity-30 cursor-pointer"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  disabled={page >= data.total_pages}
                  onClick={() => setPage((p) => p + 1)}
                  className="p-1 rounded-lg border border-foreground/10 disabled:opacity-30 cursor-pointer"
                >
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}