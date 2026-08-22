import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'sonner';

import { getWalletBalance, createClaim, getClaims } from '../services/wallet-service';
import {
  createClaimSchema,
  type CreateClaimProps,
  type TransactionType,
  type ClaimResponse,
  type ClaimStatus,
} from '../types';
import type { ErrorResponse } from 'react-router-dom';
import type { ValidationErrorResponse } from '@/constants/types';

export function useWallet() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState<number>(1);
  const [type, setType] = useState<TransactionType | undefined>(undefined);

  const [claimsPage, setClaimsPage] = useState<number>(1);
  const [claimsStatus, setClaimsStatus] = useState<ClaimStatus>('pending');

  const [isDepositModalOpen, setIsDepositModalOpen] = useState<boolean>(false);
  const [activeClaim, setActiveClaim] = useState<ClaimResponse | null>(null);

  function getErrorMessage(error: unknown): string {
    const err = error as { response?: { data?: ErrorResponse | ValidationErrorResponse } };
    const responseData = err.response?.data;

    if (responseData) {
      if ('errors' in responseData && Array.isArray(responseData.errors) && responseData.errors.length > 0) {
        return responseData.errors[0].message;
      }
      if ('detail' in responseData && typeof responseData.detail === 'string') {
        return responseData.detail;
      }
    }
    return 'Ocorreu um erro na solicitação. Tente novamente.';
  }

  const walletQuery = useQuery({
    queryKey: ['wallet', { page, type }],
    queryFn: () => getWalletBalance({ page, per_page: 5, type }),
  });

  const claimsQuery = useQuery({
    queryKey: ['wallet-claims', { page: claimsPage, status: claimsStatus }],
    queryFn: () => getClaims({ page: claimsPage, status: claimsStatus, per_page: 5 }),
  });

  const claimForm = useForm<CreateClaimProps>({
    resolver: zodResolver(createClaimSchema),
    defaultValues: {
      amount: 10,
      type: 'deposit',
    },
  });

  const claimMutation = useMutation({
    mutationFn: (data: CreateClaimProps) => createClaim(data),
    onSuccess: (claimData) => {
      setActiveClaim(claimData);
      queryClient.invalidateQueries({ queryKey: ['wallet-claims'] });
      toast.success('PIX gerado! Realize o pagamento para concluir.');
    },
    onError: (error: unknown) => {
      toast.error(getErrorMessage(error));
    },
  });

  const handleCloseModal = () => {
    setIsDepositModalOpen(false);
    setActiveClaim(null);
    claimForm.reset();
  };

  const handleRefreshWallet = () => {
    queryClient.invalidateQueries({ queryKey: ['wallet'] });
    queryClient.invalidateQueries({ queryKey: ['wallet-claims'] });
    handleCloseModal();
    toast.info('Dados da carteira atualizados.');
  };

  const handleSelectPendingClaim = (claim: ClaimResponse) => {
    if (claim.status === 'pending') {
      setActiveClaim(claim);
      setIsDepositModalOpen(true);
    }
  };

  return {
    balance: Number(walletQuery.data?.balance ?? 0),
    transactions: walletQuery.data?.transactions,
    
    claimsData: claimsQuery.data,
    claims: claimsQuery.data?.items ?? [],
    isLoadingClaims: claimsQuery.isLoading,
    claimsPage,
    setClaimsPage,
    claimsStatus,
    setClaimsStatus: (newStatus: ClaimStatus) => {
      setClaimsStatus(newStatus);
      setClaimsPage(1);
    },

    isLoading: walletQuery.isLoading,
    isRefetching: walletQuery.isRefetching,
    refetch: () => {
      walletQuery.refetch();
      claimsQuery.refetch();
    },

    page,
    setPage,
    type,
    setType: (newType: TransactionType | undefined) => {
      setType(newType);
      setPage(1);
    },

    isDepositModalOpen,
    openDepositModal: () => {
      setActiveClaim(null);
      setIsDepositModalOpen(true);
    },
    closeDepositModal: handleCloseModal,
    activeClaim,
    handleSelectPendingClaim,
    refreshWallet: handleRefreshWallet,

    claimForm: {
      register: claimForm.register,
      handleSubmit: claimForm.handleSubmit((data: CreateClaimProps) =>
        claimMutation.mutate(data)
      ),
      errors: claimForm.formState.errors,
      isPending: claimMutation.isPending,
    },
  };
}
