import { Link } from 'react-router-dom';
import {
  ArrowLeft,
  ScanLine,
  Loader2,
  QrCode,
  Send,
  CheckCircle2,
  XCircle,
  Camera,
  CameraOff,
  RotateCcw,
} from 'lucide-react';
import { PAGES } from '@/constants/pages';
import { useCheckin } from '../hooks/use-checkin';
import { QrScanner } from '../compontents/QrScanner';

export function CheckinPage() {
  const {
    event,
    isLoadingEvent,
    hashInput,
    setHashInput,
    isScannerOpen,
    setIsScannerOpen,
    lastValidation,
    isPending,
    handleValidate,
    handleNewScan,
  } = useCheckin();

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <Link
        to={PAGES.PRIVATE.CHECKIN.BASE}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </Link>

      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2 min-w-0 flex-1">
          <h1 className="text-xl sm:text-3xl font-black text-foreground tracking-tight uppercase leading-tight line-clamp-2 break-words">
            {isLoadingEvent ? 'CARREGANDO...' : event?.title || 'VALIDAÇÃO'}
          </h1>
          <ScanLine className="w-6 h-6 text-primary shrink-0 mt-0.5" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 items-start">
        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-foreground/10">
            <div className="flex items-center gap-2">
              <QrCode className="w-4 h-4 text-primary shrink-0" />
              <h2 className="text-sm sm:text-base font-bold text-foreground">Leitura de QR Code</h2>
            </div>

            <button
              type="button"
              onClick={() => setIsScannerOpen((prev) => !prev)}
              className="flex items-center gap-1.5 bg-background border border-foreground/10 px-3 py-1.5 rounded-full text-xs font-bold text-foreground hover:border-primary transition cursor-pointer"
            >
              {isScannerOpen ? (
                <>
                  <CameraOff className="w-3.5 h-3.5 text-rose-500" />
                  <span>Fechar Câmera</span>
                </>
              ) : (
                <>
                  <Camera className="w-3.5 h-3.5 text-primary" />
                  <span>Câmera</span>
                </>
              )}
            </button>
          </div>

          {isScannerOpen && <QrScanner onScan={(code) => handleValidate(code)} />}

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleValidate();
            }}
            className="space-y-3"
          >
            <div className="space-y-1.5">
              <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider block">
                Digitação Manual (Hash)
              </span>
              <input
                type="text"
                value={hashInput}
                onChange={(e) => setHashInput(e.target.value)}
                placeholder="Cole ou escaneie o hash..."
                disabled={isPending}
                className="w-full bg-background border border-foreground/10 px-3.5 py-2.5 rounded-xl text-xs font-bold text-foreground outline-none focus:border-primary transition placeholder:font-normal"
              />
            </div>

            <button
              type="submit"
              disabled={!hashInput.trim() || isPending}
              className="w-full flex items-center justify-center gap-2 bg-primary text-primary-foreground font-bold text-xs py-2.5 px-4 rounded-full hover:bg-primary/90 transition cursor-pointer disabled:opacity-40"
            >
              {isPending ? (
                <Loader2 className="w-4 h-4 animate-spin text-primary-foreground" />
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Validar Ingresso</span>
                </>
              )}
            </button>
          </form>
        </div>

        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 min-h-[220px] flex flex-col justify-center items-center text-center">
          {isPending ? (
            <div className="flex flex-col items-center gap-2">
              <Loader2 className="w-6 h-6 animate-spin text-primary" />
              <span className="text-xs font-bold text-foreground">Validando no servidor...</span>
            </div>
          ) : lastValidation ? (
            <div className="space-y-4 w-full flex flex-col items-center">
              {lastValidation.success ? (
                <div className="flex flex-col items-center space-y-1">
                  <CheckCircle2 className="w-10 h-10 text-emerald-500 mb-1 shrink-0" />
                  <p className="text-base font-black text-emerald-500">Liberação Confirmada!</p>
                  <p className="text-xs font-bold text-foreground px-2">
                    {lastValidation.message}
                  </p>
                  {lastValidation.ticketInfo && (
                    <p className="text-[11px] font-medium text-foreground-muted">
                      Comprador: {lastValidation.ticketInfo}
                    </p>
                  )}
                </div>
              ) : (
                <div className="flex flex-col items-center space-y-1">
                  <XCircle className="w-10 h-10 text-rose-500 mb-1 shrink-0" />
                  <p className="text-base font-black text-rose-500">Acesso Recusado</p>
                  <p className="text-xs font-bold text-foreground px-2">
                    {lastValidation.message}
                  </p>
                </div>
              )}

              <button
                type="button"
                onClick={handleNewScan}
                className="inline-flex items-center justify-center gap-2 bg-background border border-foreground/15 text-foreground font-bold text-xs py-2 px-4 rounded-full hover:border-primary transition cursor-pointer shadow-sm"
              >
                <RotateCcw className="w-3.5 h-3.5 text-primary" />
                <span>Escanear Outro Ingresso</span>
              </button>
            </div>
          ) : (
            <div className="text-foreground-muted text-xs font-medium space-y-1">
              <p className="font-bold text-foreground">Aguardando leitura</p>
              <p className="text-[11px]">
                Escaneie com a câmera ou digite o hash para validar o ingresso.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}