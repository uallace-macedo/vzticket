import { CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { PAGES } from '@/constants/pages';

export function CheckoutSuccess() {
  const navigate = useNavigate();

  return (
    <div className="max-w-md mx-auto py-16 px-4 text-center space-y-5 animate-in fade-in duration-300">
      <div className="w-16 h-16 bg-emerald-500/10 text-emerald-500 rounded-full flex items-center justify-center mx-auto">
        <CheckCircle2 className="w-10 h-10" />
      </div>
      <h2 className="text-2xl font-black text-foreground">Compra Confirmada!</h2>
      <p className="text-xs text-foreground-muted">
        Seus ingressos já foram gerados e estão disponíveis na sua carteira de ingressos.
      </p>
      <button
        onClick={() => navigate(PAGES.PRIVATE.TICKETS.BASE)}
        className="w-full bg-primary text-white font-extrabold py-3 rounded-xl hover:opacity-90 transition text-sm cursor-pointer"
      >
        Ver meus ingressos
      </button>
    </div>
  );
}