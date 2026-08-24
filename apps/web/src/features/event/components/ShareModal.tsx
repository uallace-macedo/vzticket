import { useState } from 'react';
import { X, Copy, Check, MessageCircle } from 'lucide-react';
import { toast } from 'sonner';

interface ShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  eventTitle: string;
}

export function ShareModal({ isOpen, onClose, eventTitle }: ShareModalProps) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;
  const currentUrl = window.location.href;

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(currentUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      toast.error('Falha ao copiar o link');
    }
  }

  const whatsappMessage = encodeURIComponent(
    `Confira esse evento: *${eventTitle}*\n${currentUrl}`
  )
  const whatsappUrl = `https://api.whatsapp.com/send?text=${whatsappMessage}`

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="absolute inset-0" onClick={onClose} />

      <div className="relative z-10 w-full max-w-md bg-background border border-foreground/10 rounded-3xl p-6 shadow-2xl space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-black text-foreground">
            Compartilhar Evento
          </h3>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-foreground/5 text-foreground-muted transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-bold text-foreground-muted uppercase tracking-wider">
            Link do evento
          </label>
          <div className="flex items-center gap-2 bg-background-muted border border-foreground/10 rounded-2xl p-1.5 pl-3">
            <input
              type="text"
              readOnly
              value={currentUrl}
              className="w-full bg-transparent text-xs font-medium text-foreground-muted outline-none truncate select-all"
            />
            <button
              onClick={handleCopyLink}
              className="flex items-center gap-1.5 bg-primary text-white text-xs font-extrabold px-3.5 py-2 rounded-xl hover:opacity-90 transition shrink-0 cursor-pointer"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>Copiado!</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copiar</span>
                </>
              )}
            </button>
          </div>
        </div>

        <div className="pt-2">
          <a
            href={whatsappUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2.5 w-full bg-[#25D366] hover:bg-[#20bd5a] text-white font-extrabold text-sm py-3 rounded-2xl transition shadow-md cursor-pointer"
          >
            <MessageCircle className="w-5 h-5 fill-current" />
            <span>Compartilhar no WhatsApp</span>
          </a>
        </div>
      </div>
    </div>
  )
}
