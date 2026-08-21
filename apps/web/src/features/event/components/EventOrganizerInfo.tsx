import type { EventOrganizer } from '../types';

interface EventOrganizerInfoProps {
  organizer: EventOrganizer;
}

export function EventOrganizerInfo({ organizer }: EventOrganizerInfoProps) {
  const initialLetter = organizer?.name ? organizer.name.charAt(0).toUpperCase() : 'O';

  return (
    <div className="pt-6 border-t border-foreground/10 space-y-3">
      <h3 className="text-sm font-extrabold text-foreground-muted uppercase tracking-wider">
        Organizado por
      </h3>

      <div className="flex items-center gap-3 bg-background-muted p-3.5 rounded-2xl border border-foreground/5">
        <div className="w-11 h-11 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center text-primary font-black text-base shrink-0">
          {initialLetter}
        </div>

        <div className="overflow-hidden">
          <h4 className="font-extrabold text-sm text-foreground truncate">
            {organizer?.name || 'Organizador sem nome'}
          </h4>
          <p className="text-xs text-foreground-muted font-medium truncate">
            {organizer?.email || 'Contato indisponível'}
          </p>
        </div>
      </div>
    </div>
  )
}
