import { LucideTicket } from 'lucide-react';

interface EventFooterProps {
  totalPricePerUnit: number;
  quantity: number;
  onCheckout: () => void;
}

export function EventFooter({ totalPricePerUnit, quantity, onCheckout }: EventFooterProps) {
  const totalAmount = totalPricePerUnit * quantity;

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-background/95 backdrop-blur-md border-t border-t-foreground/15 p-5 z-50">
      <div className="max-w-6xl mx-auto flex items-center justify-center lg:justify-end">
        <button
          onClick={onCheckout}
          className="w-full max-w-md bg-primary text-white font-medium px-5 py-3 cursor-pointer rounded-xl hover:brightness-90 transition disabled:opacity-40 flex items-center justify-between"
          disabled={quantity === 0}
        >
          <div className="flex items-center gap-3">
            <LucideTicket className="size-5 text-white" />
            <span className="text-sm">
              {quantity > 0
                ? quantity === 1
                  ? 'Comprar ingresso'
                  : 'Comprar ingressos'
                : 'Garantir meu ingresso'}
            </span>
          </div>
          <span className="text-xs font-normal">
            {quantity === 1
              ? `${formatCurrency(totalPricePerUnit)}`
              : `${formatCurrency(totalAmount)}`}
          </span>
        </button>
      </div>
    </div>
  );
}
