import { Filter } from 'lucide-react';
import type { TicketStatus } from '../../types';

interface TicketFiltersProps {
  selectedStatus?: TicketStatus;
  onSelectStatus: (status?: TicketStatus) => void;
}

export function TicketFilters({ selectedStatus, onSelectStatus }: TicketFiltersProps) {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
      <div className="relative shrink-0">
        <select
          value={selectedStatus || ''}
          onChange={(e) => onSelectStatus(e.target.value ? (e.target.value as TicketStatus) : undefined)}
          className="bg-background-muted border border-foreground/10 px-4 py-2 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition cursor-pointer appearance-none pr-8 flex items-center gap-2"
        >
          <option value="valid">Disponíveis</option>
          <option value="used">Utilizados</option>
          <option value="canceled">Cancelados</option>
        </select>
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-[10px] text-foreground-muted">
          <Filter className="w-3 h-3" />
        </div>
      </div>
    </div>
  );
}