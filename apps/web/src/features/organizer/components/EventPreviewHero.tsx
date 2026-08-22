import { useState, useEffect } from 'react';

interface EventPreviewHeroProps {
  posterUrl?: string | null;
  bannerUrl?: string | null;
  title?: string;
}

export function EventPreviewHero({ posterUrl, bannerUrl, title }: EventPreviewHeroProps) {
  const [hasPosterError, setHasPosterError] = useState(false);
  const [hasBannerError, setHasBannerError] = useState(false);

  useEffect(() => {
    setHasPosterError(false);
    setHasBannerError(false);
  }, [posterUrl, bannerUrl]);

  const showPoster = posterUrl && !hasPosterError;
  const showBanner = bannerUrl && !hasBannerError;

  return (
    <div className="relative w-full h-36 sm:h-48 overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-primary/20 to-slate-900 flex items-center justify-center border border-foreground/10">
      {showBanner ? (
        <img
          src={bannerUrl!}
          alt="Banner"
          onError={() => setHasBannerError(true)}
          className="absolute inset-0 w-full h-full object-cover blur-sm opacity-60 scale-110 pointer-events-none"
        />
      ) : (
        <div className="absolute inset-0 bg-linear-to-tr from-primary/30 via-background-muted to-background/80" />
      )}

      <div className="absolute inset-0 bg-black/40 pointer-events-none" />

      <div className="relative z-10 flex items-center gap-4 px-4 w-full">
        {showPoster ? (
          <img
            src={posterUrl!}
            alt={title || 'Preview'}
            onError={() => setHasPosterError(true)}
            className="h-28 sm:h-36 w-auto object-contain rounded-xl shadow-lg border border-white/20 shrink-0"
          />
        ) : (
          <div className="h-28 sm:h-36 w-20 sm:w-24 rounded-xl bg-linear-to-br from-primary/40 to-primary-muted border border-white/10 flex items-center justify-center shrink-0 shadow-lg">
            <span className="text-[10px] font-bold text-white/70 uppercase tracking-wider text-center px-1">
              Sem Imagem
            </span>
          </div>
        )}

        <p className="text-white font-extrabold text-sm sm:text-base line-clamp-2 drop-shadow-md">
          {title || 'Título do Evento'}
        </p>
      </div>
    </div>
  );
}