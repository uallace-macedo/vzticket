import type { Event } from '../types';

interface EventHeroProps {
  event: Event;
}

export function EventHero({ event }: EventHeroProps) {
  const poster =
    event.media?.poster_url ||
    event.media?.custom_image_url ||
    '/placeholder-event.jpg';
  const banner = event.media?.banner_url || poster;

  return (
    <div className="relative w-full min-h-[300px] sm:min-h-[420px] overflow-hidden rounded-3xl bg-background-muted flex items-center justify-center">
      <img
        src={banner}
        alt="Banner Background"
        className="absolute inset-0 w-full h-full object-cover blur-sm opacity-100 scale-125 pointer-events-none select-none"
      />

      <div className="absolute inset-0 bg-black/30 pointer-events-none" />

      <div className="relative z-10 p-4 sm:p-8">
        <img
          src={poster}
          alt={event.title}
          className="max-h-[340px] sm:max-h-[420px] w-auto object-contain rounded-2xl shadow-2xl"
        />
      </div>
    </div>
  );
}
