import { api } from '@/lib/axios';
import { ROUTES } from '@/constants/routes';
import type {
  WalletBalanceResponse,
  WalletTransactionSearchParams,
  CreateClaimProps,
  ClaimResponse,
} from '../types';

export async function getWalletBalance(
  params?: WalletTransactionSearchParams
): Promise<WalletBalanceResponse> {
  const response = await api.get<WalletBalanceResponse>(ROUTES.WALLET.GET_BALANCE, {
    params,
  })
  return response.data;
}

export async function createClaim(data: CreateClaimProps): Promise<ClaimResponse> {
  const response = await api.post<ClaimResponse>(ROUTES.WALLET.CREATE_CLAIM, data);
  return response.data;
}
