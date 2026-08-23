import { useRef, useState } from 'react';
import { ShieldAlert, Download, Loader2, X, CheckCircle2 } from 'lucide-react';
import { toPng } from 'html-to-image';
import { toast } from 'sonner';
import type { UserTicket } from '../../types';

interface ShareTicketModalProps {
  isOpen: boolean;
  ticket: UserTicket;
  onClose: () => void;
}

export function ShareTicketModal({ isOpen, ticket, onClose }: ShareTicketModalProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  if (!isOpen) return null;

  const handleDownload = async () => {
    if (!cardRef.current) return;

    try {
      setIsGenerating(true);

      const dataUrl = await toPng(cardRef.current, {
        cacheBust: true,
        pixelRatio: 2,
      });

      if (navigator.share && navigator.canShare) {
        const response = await fetch(dataUrl);
        const blob = await response.blob();
        const file = new File([blob], `ingresso-${ticket.id}.png`, { type: 'image/png' });

        if (navigator.canShare({ files: [file] })) {
          await navigator.share({
            title: 'Meu Ingresso',
            files: [file],
          });
          toast.success('Ingresso compartilhado com sucesso!');
          onClose();
          return;
        }
      }

      const link = document.createElement('a');
      link.download = `ingresso-${ticket.id}.png`;
      link.href = dataUrl;
      link.click();

      toast.success('Ingresso baixado com sucesso!');
      onClose();
    } catch (error) {
      console.error('Erro ao gerar imagem do ingresso:', error);
      toast.error('Não foi possível gerar a imagem do ingresso.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-background border border-foreground/10 rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl animate-in zoom-in-95 duration-200 max-h-[90vh] overflow-y-auto relative">        
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-foreground-muted hover:text-foreground transition cursor-pointer p-1"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3">
          <div className="p-3 bg-amber-500/10 text-amber-500 rounded-2xl">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-black text-foreground">Baixar ou Compartilhar Ingresso</h3>
            <p className="text-xs text-foreground-muted">Gerar imagem do seu ingresso</p>
          </div>
        </div>

        <div className="p-2 bg-background-muted rounded-2xl border border-foreground/10 flex justify-center">
          <div
            ref={cardRef}
            className="w-full max-w-xs bg-background p-5 rounded-xl border border-foreground/10 shadow-sm flex flex-col items-center text-center space-y-4"
          >
            <div className="space-y-1">
              <span className="text-[10px] uppercase tracking-wider font-extrabold text-primary">
                Ingresso Digital
              </span>
              <h4 className="text-sm font-black text-foreground line-clamp-1">
                {ticket.event.title || 'Evento Confirmado'}
              </h4>
            </div>

            <div className="p-3 bg-white rounded-xl shadow-inner border border-gray-100">
              <img
                src={`https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=${encodeURIComponent(
                  ticket.qr_code_hash
                )}`}
                alt="QR Code do Ingresso"
                className="w-36 h-36 object-contain"
              />
            </div>

            <div className="space-y-0.5 text-xs">
              <p className="font-bold text-foreground">Cód: {ticket.qr_code_hash.slice(0, 12)}...</p>
              <div className="flex items-center justify-center gap-1 text-[11px] text-emerald-500 font-semibold">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Válido</span>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2.5 bg-amber-500/5 p-4 rounded-2xl border border-amber-500/10 text-xs text-foreground-muted">
          <p className="font-bold text-amber-500 text-[11px] uppercase tracking-wider">
            Avisos Importantes de Segurança
          </p>
          <ul className="space-y-2 text-[11px] leading-relaxed">
            <li className="flex gap-2">
              <span className="text-amber-500 font-bold">•</span>
              <span>
                <strong className="text-foreground">Cuidado com duplicatas:</strong> Este QR Code é único e dá acesso a apenas 1 pessoa.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-500 font-bold">•</span>
              <span>
                <strong className="text-foreground">Entrada por leitura:</strong> A primeira pessoa que apresentar este código na portaria garantirá o acesso.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-500 font-bold">•</span>
              <span>
                <strong className="text-foreground">Não publique em redes abertas:</strong> Evite postar fotos onde o QR Code apareça claramente para evitar cópias não autorizadas.
              </span>
            </li>
          </ul>
        </div>

        <div className="flex items-center justify-end gap-3 pt-1">
          <button
            type="button"
            onClick={onClose}
            disabled={isGenerating}
            className="px-4 py-2.5 rounded-full text-xs font-bold text-foreground-muted hover:text-foreground transition disabled:opacity-50 cursor-pointer"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={handleDownload}
            disabled={isGenerating}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary hover:opacity-90 text-white text-xs font-extrabold rounded-full transition disabled:opacity-50 cursor-pointer shadow-md shadow-primary/20"
          >
            {isGenerating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Gerando Imagem...</span>
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                <span>Baixar / Compartilhar</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
