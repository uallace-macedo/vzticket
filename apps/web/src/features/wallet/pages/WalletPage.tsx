import {
  Wallet,
  Plus,
  Loader2,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
  ArrowLeft,
  AlertCircle,
  CheckCircle2,
  Clock,
} from 'lucide-react';
import { useWallet } from '../hooks/use-wallet';
import { TransactionItem } from '../components/TransactionItem';
import { ClaimItem } from '../components/ClaimItem';
import { DepositModal } from '../components/DepositModal';
import type { TransactionType, ClaimStatus } from '../types';
import { Link } from 'react-router-dom';
import { PAGES } from '@/constants/pages';

export function WalletPage() {
  const {
    balance,
    transactions,
    claimsData,
    claims,
    isLoadingClaims,
    claimsPage,
    setClaimsPage,
    claimsStatus,
    setClaimsStatus,
    isLoading,
    isRefetching,
    refetch,
    page,
    setPage,
    type,
    setType,
    isDepositModalOpen,
    openDepositModal,
    closeDepositModal,
    claimForm,
    activeClaim,
    handleSelectPendingClaim,
    refreshWallet,
  } = useWallet();

  const formattedBalance = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(balance);

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 sm:py-8 space-y-6">
      <Link
        to={PAGES.PUBLIC.EVENTS}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar</span>
      </Link>

      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl sm:text-3xl font-black text-foreground tracking-tight uppercase">
            Carteira
          </h1>
          <Wallet className="w-6 h-6 text-primary" />
        </div>

        <button
          onClick={openDepositModal}
          className="flex items-center gap-1.5 bg-primary text-primary-foreground font-bold text-xs px-3.5 py-2 rounded-full hover:bg-primary/90 transition cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Depositar</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 space-y-1">
          <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider">
            Saldo em Conta
          </span>
          <p className="text-2xl sm:text-3xl font-black text-foreground">
            {isLoading ? 'R$ ---' : formattedBalance}
          </p>
        </div>

        <div className="bg-background-muted border border-foreground/10 rounded-2xl p-4 sm:p-5 flex items-center justify-between">
          <div className="space-y-1">
            <span className="text-[11px] font-bold uppercase text-foreground-muted tracking-wider">
              Total de Transações
            </span>
            <p className="text-2xl sm:text-3xl font-black text-foreground">
              {transactions?.total ?? 0}
            </p>
          </div>

          <button
            onClick={() => refetch()}
            title="Atualizar dados"
            className="p-2 rounded-xl hover:bg-foreground/5 text-foreground-muted hover:text-foreground transition cursor-pointer"
          >
            <RefreshCw
              className={`w-4 h-4 ${isRefetching ? 'animate-spin text-primary' : ''}`}
            />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">        
        <div className="flex flex-col h-full space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-foreground/10 min-h-[38px]">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-500" />
              <h2 className="text-base font-bold text-foreground">
                Cobranças
              </h2>
            </div>

            <div className="relative shrink-0">
              <select
                value={claimsStatus}
                onChange={(e) => setClaimsStatus(e.target.value as ClaimStatus)}
                className="bg-background-muted border border-foreground/10 px-3 py-1 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition cursor-pointer appearance-none pr-7 w-full sm:w-auto"
              >
                <option value="pending">Pendentes</option>
                <option value="expired">Expiradas</option>
              </select>
              <div className="absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-[10px] text-foreground-muted">
                ▼
              </div>
            </div>
          </div>

          {isLoadingClaims ? (
            <div className="flex-1 flex justify-center items-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-primary" />
            </div>
          ) : claims.length === 0 ? (
            <div className="flex-1 min-h-[220px] flex flex-col items-center justify-center p-6 border border-dashed border-foreground/10 rounded-2xl bg-background-muted/30 text-center">
              {claimsStatus === 'pending' ? (
                <>
                  <CheckCircle2 className="w-8 h-8 text-emerald-500 mb-2" />
                  <p className="text-xs font-bold text-foreground">Nenhuma pendência por aqui!</p>
                  <p className="text-[11px] text-foreground-muted mt-1">
                    Todas as suas cobranças e depósitos estão em dia.
                  </p>
                </>
              ) : (
                <>
                  <Clock className="w-8 h-8 text-foreground-muted mb-2" />
                  <p className="text-xs font-bold text-foreground">Nenhuma cobrança expirada.</p>
                  <p className="text-[11px] text-foreground-muted mt-1">
                    Seus PIX vencidos aparecerão nesta lista.
                  </p>
                </>
              )}
            </div>
          ) : (
            <div className="space-y-2">
              {claims.map((claim) => (
                <ClaimItem
                  key={claim.id}
                  claim={claim}
                  onClick={handleSelectPendingClaim}
                />
              ))}
            </div>
          )}

          {claimsData && claimsData.pages > 1 && (
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-foreground-muted font-medium">
                Página {claimsData.page} de {claimsData.pages}
              </span>

              <div className="flex items-center gap-1">
                <button
                  disabled={claimsPage <= 1}
                  onClick={() => setClaimsPage(claimsPage - 1)}
                  className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  disabled={claimsPage >= claimsData.pages}
                  onClick={() => setClaimsPage(claimsPage + 1)}
                  className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="flex flex-col h-full space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-foreground/10 min-h-[38px]">
            <h2 className="text-base font-bold text-foreground">Extrato</h2>

            <div className="relative shrink-0">
              <select
                value={type || ''}
                onChange={(e) =>
                  setType(
                    e.target.value ? (e.target.value as TransactionType) : undefined
                  )
                }
                className="bg-background-muted border border-foreground/10 px-3 py-1 rounded-full text-xs font-bold text-foreground outline-none focus:border-primary transition cursor-pointer appearance-none pr-7 w-full sm:w-auto"
              >
                <option value="">Todas as movimentações</option>
                <option value="deposit">Depósitos</option>
                <option value="ticket_purchase">Compras</option>
                <option value="ticket_refund">Reembolsos</option>
                <option value="event_creation_fee">Taxas</option>
                <option value="event_payout">Recebimentos</option>
              </select>
              <div className="absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none text-[10px] text-foreground-muted">
                ▼
              </div>
            </div>
          </div>

          {isLoading ? (
            <div className="flex-1 flex justify-center items-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-primary" />
            </div>
          ) : !transactions || transactions.items.length === 0 ? (
            <div className="flex-1 min-h-[220px] flex items-center justify-center text-center py-12 text-foreground-muted text-sm font-medium border border-dashed border-foreground/10 rounded-2xl bg-background-muted/30">
              Nenhuma transação encontrada.
            </div>
          ) : (
            <div className="space-y-2">
              {transactions.items.map((tx) => (
                <TransactionItem key={tx.id} transaction={tx} />
              ))}
            </div>
          )}

          {transactions && transactions.pages > 1 && (
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-foreground-muted font-medium">
                Página {transactions.page} de {transactions.pages}
              </span>

              <div className="flex items-center gap-1">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage(page - 1)}
                  className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <button
                  disabled={page >= transactions.pages}
                  onClick={() => setPage(page + 1)}
                  className="p-1.5 rounded-lg border border-foreground/10 text-foreground disabled:opacity-30 disabled:cursor-not-allowed hover:bg-foreground/5 transition cursor-pointer"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <DepositModal
        isOpen={isDepositModalOpen}
        onClose={closeDepositModal}
        claimForm={claimForm}
        claimData={activeClaim}
        onPaidClick={refreshWallet}
      />
    </div>
  );
}
