import { Plus, Minus, Ticket } from 'lucide-react';

interface TicketSelectorProps {
  price: number;
  availableTickets: number;
  quantity: number;
  onQuantityChange: (qty: number) => void;
}

export function TicketSelector({
  price,
  availableTickets,
  quantity,
  onQuantityChange,
}: TicketSelectorProps) {
  const fee = price * 0.05;

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  return (
    <div className="bg-background-muted border border-foreground/10 rounded-2xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Ticket className="w-5 h-5 text-primary" />
          <h3 className="font-extrabold text-base text-foreground">Ingresso Único</h3>
        </div>
        <span className="text-xs font-bold text-foreground-muted bg-foreground/5 px-2.5 py-1 rounded-full">
          {availableTickets > 0 ? `${availableTickets} disponíveis` : 'Esgotado'}
        </span>
      </div>

      <div className="flex items-center justify-between pt-2">
        <div>
          <div className="text-xl font-black text-foreground">{formatCurrency(price)}</div>
          <div className="text-xs font-semibold text-foreground-muted">
            + taxa de {formatCurrency(fee)} (5%)
          </div>
        </div>

        <div className="flex items-center gap-3 bg-background border border-foreground/10 p-1 rounded-xl">
          <button
            onClick={() => onQuantityChange(Math.max(0, quantity - 1))}
            disabled={quantity === 0}
            className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-foreground/5 transition disabled:opacity-30 cursor-pointer"
          >
            <Minus className="w-4 h-4" />
          </button>
          
          <span className="font-black text-sm w-4 text-center">{quantity}</span>

          <button
            onClick={() => onQuantityChange(Math.min(availableTickets, quantity + 1))}
            disabled={quantity >= availableTickets}
            className="w-8 h-8 flex items-center justify-center rounded-lg bg-foreground text-background hover:opacity-90 transition disabled:opacity-30 cursor-pointer"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="text-[11px] font-medium text-foreground-muted bg-foreground/5 p-2.5 rounded-xl">
        Pagamento via <strong>PIX</strong> com aprovação imediata.
      </div>
    </div>
  )
}
