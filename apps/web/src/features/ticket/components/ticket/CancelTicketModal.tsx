import { AlertTriangle, Loader2 } from 'lucide-react';
import { useCancelTicket } from '../../hooks/use-cancel-ticket';

interface CancelTicketModalProps {
  isOpen: boolean;
  ticketId: string;
  onClose: () => void;
}

export function CancelTicketModal({ isOpen, ticketId, onClose }: CancelTicketModalProps) {
  const { mutate: cancelTicket, isPending } = useCancelTicket();

  if (!isOpen) return null;

  const handleConfirm = () => {
    cancelTicket(
      { ticketId },
      {
        onSuccess: () => {
          onClose();
        },
      }
    );
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-background border border-foreground/10 rounded-3xl max-w-md w-full p-6 space-y-6 shadow-xl animate-in zoom-in-95 duration-200">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-rose-500/10 text-rose-500 rounded-2xl">
            <AlertTriangle className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-black text-foreground">Cancelar Ingresso</h3>
            <p className="text-xs text-foreground-muted">Leia os termos antes de confirmar</p>
          </div>
        </div>

        <div className="space-y-3 bg-background-muted p-4 rounded-2xl border border-foreground/5 text-xs text-foreground-muted">
          <div className="space-y-1">
            <span className="font-bold text-foreground block">Prazo Legal</span>
            <p>Você pode solicitar o cancelamento em até 7 dias corridos a contar da data da compra.</p>
          </div>

          <div className="space-y-1">
            <span className="font-bold text-foreground block">Limite do Evento</span>
            <p>A solicitação precisa ser feita com no mínimo 24 horas de antecedência do horário de início do evento.</p>
          </div>

          <div className="space-y-1">
            <span className="font-bold text-foreground block">Taxa de Cancelamento</span>
            <ul className="list-disc list-inside space-y-0.5 pl-1">
              <li>Reembolso integral (100%) para solicitações com mais de 48h de antecedência.</li>
              <li>Reembolso de 80% do valor para solicitações entre 48h e 24h antes do evento (taxa administrativa de 20%).</li>
            </ul>
          </div>

          <div className="space-y-1">
            <span className="font-bold text-foreground block">Bloqueio</span>
            <p>Não são permitidos cancelamentos com menos de 24 horas para o evento ou após a sua realização.</p>
          </div>

          <div className="space-y-1">
            <span className="font-bold text-foreground block">Estorno</span>
            <p>O valor reembolsado será creditado imediatamente no seu saldo da plataforma.</p>
          </div>
        </div>

        <div className="flex items-center justify-end gap-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            disabled={isPending}
            className="px-4 py-2.5 rounded-full text-xs font-bold text-foreground-muted hover:text-foreground transition disabled:opacity-50 cursor-pointer"
          >
            Voltar
          </button>
          <button
            type="button"
            onClick={handleConfirm}
            disabled={isPending}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-rose-500 hover:bg-rose-600 text-white text-xs font-extrabold rounded-full transition disabled:opacity-50 cursor-pointer shadow-md shadow-rose-500/20"
          >
            {isPending ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Cancelando...</span>
              </>
            ) : (
              <span>Confirmar Cancelamento</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}