import { Share2, Ban, ChevronRight } from 'lucide-react';
import { toast } from 'sonner';

interface TicketOptionsSectionProps {
  eventId: string;
}

export function TicketOptionsSection({ eventId }: TicketOptionsSectionProps) {
  const handleCancel = () => {
    toast.info('Funcionalidade de cancelamento em breve!');
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Meu Ingresso',
        text: 'Confira meu ingresso para o evento!',
        url: window.location.href,
      }).catch(() => {});
    } else {
      navigator.clipboard.writeText(window.location.href);
      toast.success('Link do ingresso copiado para a área de transferência!');
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-black text-foreground">Mais opções</h3>

      <div className="space-y-2.5">
        <button
          onClick={handleShare}
          className="w-full flex items-center justify-between p-4 bg-background-muted border border-foreground/10 rounded-2xl hover:border-foreground/20 transition cursor-pointer group"
        >
          <div className="flex items-center gap-3">
            <Share2 className="w-5 h-5 text-foreground-muted group-hover:text-primary transition" />
            <span className="text-xs font-extrabold text-foreground">Compartilhar Ingresso</span>
          </div>
          <ChevronRight className="w-4 h-4 text-foreground-muted group-hover:translate-x-0.5 transition" />
        </button>

        <button
          onClick={handleCancel}
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
    </div>
  );
}