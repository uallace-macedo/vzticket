"""HTTP routes for the wallet module."""

from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends

from vzticket.core.exceptions.swagger import ErrorResponse, create_error_response
from vzticket.modules.auth.deps import get_current_user
from vzticket.modules.auth.exceptions import InvalidTokenError, UnauthorizedError
from vzticket.modules.auth.models import User
from vzticket.modules.wallet.dependencies import WalletServiceDep
from vzticket.modules.wallet.exceptions import (
    ClaimTokenAlreadyUsedError,
    ExpiredClaimTokenError,
    InvalidClaimTokenError,
)
from vzticket.modules.wallet.schemas import (
    ClaimTokenResponse,
    DepositRequest,
    TransactionResponse,
    WalletBalanceResponse,
)

router = APIRouter(prefix='/wallet', tags=['Wallet'])


@router.get(
    '/me/balance',
    responses={
        **create_error_response(
            UnauthorizedError, 'Autenticação necessária' 
        ),
    }
)
async def get_balance(
    current_user: Annotated[User, Depends(get_current_user)],
    service: WalletServiceDep,
) -> WalletBalanceResponse:
    """Return the current user's wallet balance."""
    balance = await service.get_balance(current_user.id)
    return WalletBalanceResponse(**balance)


@router.post(
    '/deposit',
    status_code=HTTPStatus.CREATED,
    responses={
        **create_error_response(
            UnauthorizedError, 'Autenticação necessária' 
        ),
    },
)
async def create_deposit(
    data: DepositRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    service: WalletServiceDep,
) -> ClaimTokenResponse:
    """Create a PENDING deposit claim token."""
    token = await service.create_deposit_claim(current_user.id, data.amount)
    return ClaimTokenResponse.model_validate(token)


@router.get(
    '/pending',
    responses={
        **create_error_response(
            UnauthorizedError, 'Autenticação necessária' 
        ),
    }
)
async def get_pending_deposit(
    current_user: Annotated[User, Depends(get_current_user)],
    service: WalletServiceDep,
) -> ClaimTokenResponse | None:
    """Return the current user's pending deposit claim, if any."""
    token = await service.get_pending_deposit(current_user.id)
    if token is None:
        return None
    return ClaimTokenResponse.model_validate(token)


@router.post(
    '/claim/{token}',
    responses={
        **create_error_response(
            InvalidClaimTokenError, 'Cobrança inválida'
        ),
        **create_error_response(
            ExpiredClaimTokenError, 'Cobrança PIX expirada'
        ),
        **create_error_response(
            ClaimTokenAlreadyUsedError, 'Cobrança já processada'
        ),
        **create_error_response(
            UnauthorizedError, 'Autenticação necessária' 
        ),
    },
)
async def claim_token(
    token: str,
    current_user: Annotated[User, Depends(get_current_user)],
    service: WalletServiceDep,
) -> TransactionResponse:
    """Atomically claim a deposit token and credit the user's balance."""
    transaction = await service.claim_token(token, current_user.id)
    return TransactionResponse.model_validate(transaction)


@router.get(
    '/transactions',
    responses={
        **create_error_response(
            UnauthorizedError, 'Autenticação necessária' 
        ),
    }
)
async def get_transactions(
    current_user: Annotated[User, Depends(get_current_user)],
    service: WalletServiceDep,
) -> list[TransactionResponse]:
    """Return the current user's transaction history."""
    transactions = await service.get_history(current_user.id)
    return [TransactionResponse.model_validate(t) for t in transactions]
