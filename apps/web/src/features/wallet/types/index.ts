import { z } from 'zod';

export const transactionTypeSchema = z.enum([
  'deposit',
  'ticket_purchase',
  'ticket_refund',
  'event_creation_fee',
  'event_payout',
]);
export type TransactionType = z.infer<typeof transactionTypeSchema>;

export const claimStatusSchema = z.enum(['pending', 'claimed', 'expired']);
export type ClaimStatus = z.infer<typeof claimStatusSchema>;

export const claimTypeSchema = z.enum([
  'deposit',
  'ticket_purchase',
  'event_fee',
]);
export type ClaimType = z.infer<typeof claimTypeSchema>;

export interface WalletTransactionResponse {
  id: string;
  type: TransactionType;
  amount: number | string;
  description: string;
  created_at: string;
}

export interface PaginatedTransactionsResponse {
  items: WalletTransactionResponse[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface WalletBalanceResponse {
  balance: number | string;
  transactions: PaginatedTransactionsResponse;
}

export interface WalletTransactionSearchParams {
  type?: TransactionType;
  page?: number;
  per_page?: number;
}

export interface ClaimTokenSearchParams {
  type?: ClaimType;
  status?: ClaimStatus;
  page?: number;
  per_page?: number;
}

export const createClaimSchema = z.object({
  amount: z
    .number('Informe um valor válido.')
    .min(5, 'O valor mínimo para depósito é R$ 5,00.'),
  type: claimTypeSchema,
});
export type CreateClaimProps = z.infer<typeof createClaimSchema>;

export interface ClaimResponse {
  id: string;
  token: string;
  amount: string;
  status: ClaimStatus;
  expires_at: string;
  created_at: string;
  claimed_at: string | null;
}

export interface PaginatedClaimsResponse {
  items: ClaimResponse[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}
