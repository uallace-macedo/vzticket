import { useState } from 'react';
import { Share2, Ban, ChevronRight } from 'lucide-react';
import { CancelTicketModal } from './CancelTicketModal';
import { ShareTicketModal } from './ShareTicketModal';
import type { UserTicket } from '../../types';

interface TicketOptionsSectionProps {
  ticket: UserTicket;
}

export function TicketOptionsSection({ ticket }: TicketOptionsSectionProps) {
  const [isCancelModalOpen, setIsCancelModalOpen] = useState(false);
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-black text-foreground">Mais opções</h3>

      <div className="space-y-2.5">
        <button
          type="button"
          onClick={() => setIsShareModalOpen(true)}
          className="w-full flex items-center justify-between p-4 bg-background-muted border border-foreground/10 rounded-2xl hover:border-foreground/20 transition cursor-pointer group"
        >
          <div className="flex items-center gap-3">
            <Share2 className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
            <span className="text-xs font-extrabold text-foreground">Compartilhar ou Baixar Ingresso</span>
          </div>
          <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
        </button>

        <button
          type="button"
          onClick={() => setIsCancelModalOpen(true)}
          className="w-full flex items-center justify-between p-4 bg-background-muted border border-foreground/10 rounded-2xl hover:border-rose-500/30 transition cursor-pointer group"
        >
          <div className="flex items-center gap-3">
            <Ban className="w-5 h-5 text-foreground-muted group-hover:text-rose-500 transition" />
            <span className="text-xs font-extrabold text-foreground group-hover:text-rose-500 transition">
              Cancelar Ingresso
            </span>
          </div>
          <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
        </button>
      </div>

      <div className="pt-2 text-[11px] text-foreground-muted">
        <p>
          A plataforma não se responsabiliza pela organização e segurança dos eventos.{' '}
          <span className="underline font-bold cursor-pointer">Saiba mais</span>
        </p>
      </div>

      <ShareTicketModal
        isOpen={isShareModalOpen}
        ticket={ticket}
        onClose={() => setIsShareModalOpen(false)}
      />

      <CancelTicketModal
        isOpen={isCancelModalOpen}
        ticketId={ticket.id}
        onClose={() => setIsCancelModalOpen(false)}
      />
    </div>
  );
}