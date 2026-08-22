from http import HTTPStatus

from fastapi import APIRouter, Depends

from vzticket.modules.auth.dependencies import (
    CurrentUserDep,
    OptionalCurrentUserDep,
    RoleChecker,
)
from vzticket.modules.users.model import UserRole
from vzticket.modules.wallet_claim_tokens.dependencies import (
    ClaimTokenQuery,
    WalletClaimTokenServiceDep,
)
from vzticket.modules.wallet_claim_tokens.schemas import (
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


@router.get(
    '/pay',
    status_code=HTTPStatus.OK,
    response_model=ClaimTokenResponse,
)
async def process_payment_via_qr(
    service: WalletClaimTokenServiceDep,
    data: ClaimTokenQuery,
    current_user: OptionalCurrentUserDep = None
):
    """
    Endpoint público acionado pelo QR Code / Link de Pagamento.
    Processa depósitos, compras de ingressos ou taxas de eventos.
    """
    return await service.execute_claim(token=data.token, user=current_user)


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
