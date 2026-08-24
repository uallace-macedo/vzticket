import { Clock, AlertCircle, ExternalLink } from 'lucide-react';
import type { ClaimResponse, ClaimType } from '../types';

const CLAIM_TYPE_LABELS: Record<ClaimType, string> = {
  deposit: 'Depósito PIX',
  ticket_purchase: 'Compra de Ingresso',
  event_fee: 'Taxa de Evento',
};

interface ClaimItemProps {
  claim: ClaimResponse;
  onClick: (claim: ClaimResponse) => void;
}

export function ClaimItem({ claim, onClick }: ClaimItemProps) {
  const isPending = claim.status === 'pending';

  const amountFloat = Math.abs(parseFloat(claim.amount) || 0);
  const formattedAmount = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(amountFloat);

  const formattedExpiration = new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(claim.expires_at));

  const claimType = ((claim as any).type as ClaimType) || 'deposit';

  return (
    <div
      onClick={() => isPending && onClick(claim)}
      className={`flex items-center justify-between p-3.5 rounded-xl bg-background-muted border transition gap-3 ${
        isPending
          ? 'border-amber-500/20 hover:border-amber-500/50 cursor-pointer group'
          : 'border-foreground/10 opacity-70 cursor-not-allowed'
      }`}
    >
      <div className="flex items-center gap-3 min-w-0">
        <div
          className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
            isPending
              ? 'bg-amber-500/10 text-amber-500'
              : 'bg-rose-500/10 text-rose-500'
          }`}
        >
          {isPending ? (
            <Clock className="w-4 h-4 animate-pulse" />
          ) : (
            <AlertCircle className="w-4 h-4" />
          )}
        </div>

        <div className="min-w-0 space-y-0.5">
          <div className="flex items-center gap-2">
            <p className="text-xs sm:text-sm font-bold text-foreground truncate">
              {CLAIM_TYPE_LABELS[claimType] || 'Cobrança'}
            </p>

            {isPending ? (
              <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-600 border border-amber-500/20">
                Pendente
              </span>
            ) : (
              <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-rose-500/10 text-rose-500 border border-rose-500/20">
                Expirado
              </span>
            )}
          </div>

          <div className="flex items-center gap-1.5 text-[11px] text-foreground-muted">
            <span>{isPending ? 'Expira em:' : 'Expirou em:'}</span>
            <span className="font-semibold text-foreground">
              {formattedExpiration}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3 shrink-0">
        <span
          className={`text-xs sm:text-sm font-bold ${
            isPending ? 'text-foreground' : 'text-foreground-muted line-through'
          }`}
        >
          {formattedAmount}
        </span>
        {isPending && (
          <ExternalLink className="w-4 h-4 text-foreground-muted group-hover:text-primary transition" />
        )}
      </div>
    </div>
  );
}
