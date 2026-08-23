import { useState, useEffect } from 'react';
import { Copy, Check, X, RefreshCw } from 'lucide-react';
import QRCode from 'react-qr-code';

interface PixPaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  paymentToken: string;
  onPaidClick: () => void;
}

export function PixPaymentModal({
  isOpen,
  onClose,
  paymentToken,
  onPaidClick,
}: PixPaymentModalProps) {
  const [copied, setCopied] = useState(false);
  const [timeLeft, setTimeLeft] = useState<number>(15 * 60);

  const apiBaseUrl = import.meta.env.VITE_API_URL || '';
  const payUrl = `${apiBaseUrl}/api/v1/wallet/claims/pay?token=${paymentToken}`;

  useEffect(() => {
    if (!isOpen) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isOpen]);

  if (!isOpen) return null;

  const formatTimer = (seconds: number) => {
    const m = Math.floor(seconds / 60)
      .toString()
      .padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(payUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-background border border-foreground/10 rounded-2xl w-full max-w-sm p-5 space-y-4 relative shadow-xl"
      >
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-foreground">Pagamento via PIX</h3>
          <button
            onClick={onClose}
            className="text-foreground-muted hover:text-foreground transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="flex items-center justify-between text-xs bg-background-muted p-2.5 rounded-xl border border-foreground/10">
            <span className="font-bold text-foreground-muted">Expira em:</span>
            <span className="font-mono font-bold text-primary">{formatTimer(timeLeft)}</span>
          </div>

          <div className="flex flex-col items-center justify-center p-4 bg-white rounded-xl border border-foreground/10">
            <QRCode value={payUrl} size={160} />
            <span className="text-[10px] font-bold text-zinc-500 uppercase mt-2">
              Escaneie com o app do seu banco
            </span>
          </div>

          <div>
            <label className="text-[10px] font-bold uppercase text-foreground-muted block mb-1">
              Link de Pagamento / Copia e Cola
            </label>
            <div className="flex items-center gap-2 bg-background-muted border border-foreground/10 rounded-xl p-1 pl-3">
              <input
                type="text"
                readOnly
                value={payUrl}
                className="w-full bg-transparent text-xs font-mono text-foreground-muted outline-none truncate"
              />
              <button
                type="button"
                onClick={handleCopy}
                className="p-2 text-foreground-muted hover:text-foreground transition shrink-0 cursor-pointer"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-emerald-500" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>

          <button
            type="button"
            onClick={onPaidClick}
            className="w-full bg-primary text-primary-foreground font-bold py-2.5 rounded-xl hover:bg-primary/90 transition flex items-center justify-center gap-2 text-sm cursor-pointer"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Já efetuei o pagamento</span>
          </button>
        </div>
      </div>
    </div>
  );
}