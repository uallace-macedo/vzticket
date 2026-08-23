import { useEffect, useRef, useState } from 'react';
import { Html5Qrcode } from 'html5-qrcode';
import { Upload, Camera, AlertCircle, Loader2 } from 'lucide-react';

interface QrScannerProps {
  onScan: (decodedText: string) => void;
}

export function QrScanner({ onScan }: QrScannerProps) {
  const [mode, setMode] = useState<'camera' | 'file'>('camera');
  const [isProcessingFile, setIsProcessingFile] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const [cameraError, setCameraError] = useState<string | null>(null);

  const scannerRef = useRef<Html5Qrcode | null>(null);
  const hasCapturedRef = useRef(false);
  const regionId = 'qr-reader-container';

  useEffect(() => {
    if (mode !== 'camera') return;

    setCameraError(null);
    hasCapturedRef.current = false;
    const html5QrCode = new Html5Qrcode(regionId);
    scannerRef.current = html5QrCode;

    html5QrCode
      .start(
        { facingMode: 'environment' },
        { fps: 10, qrbox: { width: 200, height: 200 } },
        (decodedText) => {
          if (hasCapturedRef.current) return;
          hasCapturedRef.current = true;

          if (scannerRef.current?.isScanning) {
            scannerRef.current.stop().then(() => {
              scannerRef.current?.clear();
              onScan(decodedText);
            }).catch(() => {
              onScan(decodedText);
            });
          } else {
            onScan(decodedText);
          }
        },
        () => {}
      )
      .catch((err) => {
        console.error('Erro ao acessar câmera:', err);
        setCameraError('Câmera indisponível no dispositivo. Alterne para o envio de imagem.');
      });

    return () => {
      if (scannerRef.current?.isScanning) {
        scannerRef.current.stop().then(() => scannerRef.current?.clear());
      }
    };
  }, [mode, onScan]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || isProcessingFile) return;

    setFileError(null);
    setIsProcessingFile(true);

    try {
      const html5QrCode = new Html5Qrcode('qr-reader-file-temp');
      const decodedText = await html5QrCode.scanFile(file, true);
      
      onScan(decodedText);
    } catch (err) {
      console.error('Erro ao ler QR code do arquivo:', err);
      setFileError('Não foi possível ler um QR Code nesta imagem. Tente outra foto.');
    } finally {
      setIsProcessingFile(false);
      e.target.value = '';
    }
  };

  return (
    <div className="space-y-3">
      <div id="qr-reader-file-temp" className="hidden" />

      <div className="flex items-center gap-2 p-1 bg-background border border-foreground/10 rounded-xl">
        <button
          type="button"
          onClick={() => setMode('camera')}
          className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
            mode === 'camera'
              ? 'bg-primary text-primary-foreground'
              : 'text-foreground-muted hover:text-foreground'
          }`}
        >
          <Camera className="w-3.5 h-3.5" />
          <span>Câmera</span>
        </button>

        <button
          type="button"
          onClick={() => setMode('file')}
          className={`flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
            mode === 'file'
              ? 'bg-primary text-primary-foreground'
              : 'text-foreground-muted hover:text-foreground'
          }`}
        >
          <Upload className="w-3.5 h-3.5" />
          <span>Enviar Imagem</span>
        </button>
      </div>

      {mode === 'camera' && (
        <div className="space-y-2">
          {cameraError ? (
            <div className="p-4 bg-rose-500/10 border border-rose-500/20 rounded-xl text-center space-y-1">
              <AlertCircle className="w-5 h-5 text-rose-500 mx-auto" />
              <p className="text-xs font-bold text-rose-500">{cameraError}</p>
            </div>
          ) : (
            <div className="overflow-hidden rounded-xl border border-foreground/10 bg-black">
              <div id={regionId} className="w-full" />
            </div>
          )}
        </div>
      )}

      {mode === 'file' && (
        <div className="space-y-2">
          <label className="flex flex-col items-center justify-center w-full h-36 border-2 border-dashed border-foreground/15 rounded-xl cursor-pointer hover:border-primary/50 transition bg-background">
            {isProcessingFile ? (
              <div className="flex flex-col items-center gap-2">
                <Loader2 className="w-6 h-6 animate-spin text-primary" />
                <span className="text-xs font-bold text-foreground">Lendo imagem...</span>
              </div>
            ) : (
              <>
                <Upload className="w-6 h-6 text-foreground-muted mb-2" />
                <span className="text-xs font-bold text-foreground">Escolher foto do QR Code</span>
                <span className="text-[10px] text-foreground-muted mt-0.5">PNG, JPG ou WEBP</span>
              </>
            )}
            <input
              type="file"
              accept="image/*"
              disabled={isProcessingFile}
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>

          {fileError && (
            <p className="text-xs text-rose-500 font-bold text-center">{fileError}</p>
          )}
        </div>
      )}
    </div>
  );
}