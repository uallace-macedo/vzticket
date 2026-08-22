import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'sonner';

import { getWalletBalance, createClaim } from '../services/wallet-service';
import {
  createClaimSchema,
  type CreateClaimProps,
  type TransactionType,
  type ClaimResponse,
} from '../types';
import type { ErrorResponse } from 'react-router-dom';
import type { ValidationErrorResponse } from '@/constants/types';

export function useWallet() {
  const queryClient = useQueryClient();
  const [page, setPage] = useState<number>(1);
  const [type, setType] = useState<TransactionType | undefined>(undefined);
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
    queryFn: () => getWalletBalance({ page, per_page: 10, type }),
  })

  const claimForm = useForm<CreateClaimProps>({
    resolver: zodResolver(createClaimSchema),
    defaultValues: {
      amount: 10,
      type: 'deposit',
    },
  })

  const claimMutation = useMutation({
    mutationFn: (data: CreateClaimProps) => createClaim(data),
    onSuccess: (claimData) => {
      setActiveClaim(claimData);
      toast.success('PIX gerado! Realize o pagamento para concluir.');
    },
    onError: (error: unknown) => {
      toast.error(getErrorMessage(error));
    },
  })

  const handleCloseModal = () => {
    setIsDepositModalOpen(false);
    setActiveClaim(null);
    claimForm.reset();
  }

  const handleRefreshWallet = () => {
    queryClient.invalidateQueries({ queryKey: ['wallet'] });
    handleCloseModal();
    toast.info('Dados da carteira atualizados.');
  }

  return {
    balance: Number(walletQuery.data?.balance ?? 0),
    transactions: walletQuery.data?.transactions,
    isLoading: walletQuery.isLoading,
    isRefetching: walletQuery.isRefetching,
    refetch: walletQuery.refetch,

    page,
    setPage,
    type,
    setType: (newType: TransactionType | undefined) => {
      setType(newType)
      setPage(1)
    },

    isDepositModalOpen,
    openDepositModal: () => setIsDepositModalOpen(true),
    closeDepositModal: handleCloseModal,
    activeClaim,
    refreshWallet: handleRefreshWallet,

    claimForm: {
      register: claimForm.register,
      handleSubmit: claimForm.handleSubmit((data: CreateClaimProps) =>
        claimMutation.mutate(data)
      ),
      errors: claimForm.formState.errors,
      isPending: claimMutation.isPending,
    },
  }
}
