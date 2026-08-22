import { ArrowDownLeft, ArrowUpRight } from 'lucide-react'
import type { WalletTransactionResponse, TransactionType } from '../types'

const TRANSACTION_LABELS: Record<TransactionType, string> = {
  deposit: 'Depósito PIX',
  event_payout: 'Recebimento',
  ticket_refund: 'Reembolso',
  ticket_purchase: 'Compra Ingresso',
  event_creation_fee: 'Taxa Evento',
}

interface TransactionItemProps {
  transaction: WalletTransactionResponse
}

export function TransactionItem({ transaction }: TransactionItemProps) {
  const isPositive = Number(transaction.amount) >= 0

  const formattedAmount = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Math.abs(Number(transaction.amount)))

  const formattedDate = new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(transaction.created_at))

  return (
    <div className="flex items-center justify-between p-3.5 rounded-xl bg-background-muted/40 border border-foreground/5 hover:border-foreground/10 transition gap-3">
      <div className="flex items-center gap-3 min-w-0">
        <div
          className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
            isPositive ? 'bg-emerald-500/10 text-emerald-500' : 'bg-rose-500/10 text-rose-500'
          }`}
        >
          {isPositive ? (
            <ArrowDownLeft className="w-4 h-4" />
          ) : (
            <ArrowUpRight className="w-4 h-4" />
          )}
        </div>

        <div className="min-w-0 space-y-0.5">
          <div className="flex items-center gap-2">
            <p className="text-xs sm:text-sm font-bold text-foreground truncate">
              {transaction.description}
            </p>
          </div>
          <div className="flex items-center gap-2 text-[11px] text-foreground-muted">
            <span className="font-semibold text-foreground-muted/80">
              {TRANSACTION_LABELS[transaction.type] || transaction.type}
            </span>
            <span>•</span>
            <span>{formattedDate}</span>
          </div>
        </div>
      </div>

      <span
        className={`text-xs sm:text-sm font-bold shrink-0 ${
          isPositive ? 'text-emerald-500' : 'text-foreground'
        }`}
      >
        {isPositive ? '+' : '-'} {formattedAmount}
      </span>
    </div>
  )
}