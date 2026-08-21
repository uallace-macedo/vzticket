from http import HTTPStatus

from fastapi import APIRouter, Depends

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.modules.auth.dependencies import CurrentUserDep, RoleChecker
from vzticket.modules.users.model import UserRole
from vzticket.modules.wallet_claim_tokens.dependencies import (
    WalletClaimTokenServiceDep,
)
from vzticket.modules.wallet_claim_tokens.exceptions import (
    TokenAlreadyClaimedError,
    TokenExpiredError,
    TokenNotFoundError,
)
from vzticket.modules.wallet_claim_tokens.schemas import (
    ClaimTokenClaim,
    ClaimTokenCreate,
    ClaimTokenResponse,
)

router = APIRouter(prefix='/wallet/claims', tags=['Wallet Claims'])
organizer_only = Depends(RoleChecker(allowed_routes=[UserRole.ORGANIZER]))


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=ClaimTokenResponse
)
async def create_claim_token(
    data: ClaimTokenCreate,
    service: WalletClaimTokenServiceDep,
    current_user: CurrentUserDep,
):
    """Gera um novo token/QR Code descartável"""
    return await service.create_claim_token(current_user.id, data)


@router.post(
    '/claim',
    status_code=HTTPStatus.OK,
    response_model=ClaimTokenResponse,
    responses={
        **create_error_response(
            TokenNotFoundError,
            'Token não encontrado.',
        ),
        **create_error_response(
            TokenAlreadyClaimedError,
            'Token já resgatado.',
        ),
        **create_error_response(
            TokenExpiredError,
            'Token expirado.',
        ),
    },
)
async def claim_token(
    data: ClaimTokenClaim,
    service: WalletClaimTokenServiceDep,
    current_user: CurrentUserDep,
):
    """Consome o token e adiciona o saldo na carteira do usuário logado"""
    return await service.claim_token(data, current_user)


@router.get(
    '/pending',
    status_code=HTTPStatus.OK,
    response_model=list[ClaimTokenResponse],
)
async def get_pending_claims(
    service: WalletClaimTokenServiceDep,
    current_user: CurrentUserDep,
):
    """Retorna os tokens pendentes atribuídos ao usuário logado"""
    return await service.get_pending_by_user(current_user.id)
