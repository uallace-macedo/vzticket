import { Wallet, QrCode, Loader2, AlertCircle } from 'lucide-react';
import type { PaymentMethod } from '../../types/payment-types';

interface CheckoutPaymentMethodProps {
  selectedMethod: PaymentMethod;
  onSelectMethod: (method: PaymentMethod) => void;
  onSubmit: () => void;
  isPending: boolean;
  errorMessage: string | null;
}

export function CheckoutPaymentMethod({
  selectedMethod,
  onSelectMethod,
  onSubmit,
  isPending,
  errorMessage,
}: CheckoutPaymentMethodProps) {
  return (
    <div className="bg-background-muted border border-foreground/10 rounded-2xl p-5 space-y-5">
      <h2 className="text-base font-black text-foreground border-b border-foreground/10 pb-3">
        Forma de Pagamento
      </h2>

      {errorMessage && (
        <div className="flex items-center gap-2 p-3 bg-red-500/10 border border-red-500/20 text-red-500 rounded-xl text-xs font-medium">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <div className="grid grid-cols-1 gap-3">
        <button
          type="button"
          onClick={() => onSelectMethod('balance')}
          className={`flex items-center gap-3 p-4 rounded-xl border text-left transition cursor-pointer ${
            selectedMethod === 'balance'
              ? 'border-primary bg-primary/10 text-foreground'
              : 'border-foreground/10 hover:border-foreground/20 bg-background text-foreground-muted'
          }`}
        >
          <div
            className={`p-2.5 rounded-lg shrink-0 ${
              selectedMethod === 'balance'
                ? 'bg-primary text-white'
                : 'bg-foreground/5 text-foreground-muted'
            }`}
          >
            <Wallet className="w-5 h-5" />
          </div>
          <div>
            <p className="text-sm font-extrabold text-foreground">Saldo da Carteira</p>
            <p className="text-xs text-foreground-muted">
              Pague diretamente com o saldo interno da sua conta.
            </p>
          </div>
        </button>

        <button
          type="button"
          onClick={() => onSelectMethod('pix')}
          className={`flex items-center gap-3 p-4 rounded-xl border text-left transition cursor-pointer ${
            selectedMethod === 'pix'
              ? 'border-primary bg-primary/10 text-foreground'
              : 'border-foreground/10 hover:border-foreground/20 bg-background text-foreground-muted'
          }`}
        >
          <div
            className={`p-2.5 rounded-lg shrink-0 ${
              selectedMethod === 'pix'
                ? 'bg-primary text-white'
                : 'bg-foreground/5 text-foreground-muted'
            }`}
          >
            <QrCode className="w-5 h-5" />
          </div>
          <div>
            <p className="text-sm font-extrabold text-foreground">PIX</p>
            <p className="text-xs text-foreground-muted">
              Aprovação instantânea via QR Code ou Copia e Cola.
            </p>
          </div>
        </button>
      </div>

      <button
        type="button"
        onClick={onSubmit}
        disabled={isPending}
        className="w-full bg-primary text-primary-foreground font-extrabold py-3.5 rounded-xl hover:bg-primary/90 transition flex items-center justify-center gap-2 disabled:opacity-50 text-sm cursor-pointer shadow-lg shadow-primary/20"
      >
        {isPending ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Processando Compra...</span>
          </>
        ) : (
          <span>Finalizar Compra</span>
        )}
      </button>
    </div>
  );
}