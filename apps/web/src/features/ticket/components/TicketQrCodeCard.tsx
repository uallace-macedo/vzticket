import QRCode from "react-qr-code";

interface TicketQrCodeCardProps {
  qrCodeHash: string;
}

export function TicketQrCodeCard({ qrCodeHash }: TicketQrCodeCardProps) {
  return (
    <div className="bg-background-muted border border-foreground/10 rounded-3xl p-8 max-w-md mx-auto flex flex-col items-center text-center space-y-4 shadow-sm relative overflow-hidden">
      <div className="bg-white p-4 rounded-2xl shadow-inner border border-black/5">
        <QRCode
          value={qrCodeHash || 'ticket-placeholder-hash'}
          size={180}
          bgColor="#FFFFFF"
          fgColor="#000000"
          level="H"
        />
      </div>

      <div className="space-y-1 pt-2">
        <h2 className="text-base font-black text-foreground tracking-tight">
          SEU INGRESSO
        </h2>
        <p className="text-xs text-foreground-muted font-medium max-w-[220px]">
          Mostre este QR Code na entrada e aproveite o evento!
        </p>
      </div>
    </div>
  );
}