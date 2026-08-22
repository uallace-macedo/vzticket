from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from vzticket.modules.auth.dependencies import (
    CurrentUserDep,
    OptionalCurrentUserDep,
    RoleChecker,
)
from vzticket.modules.users.model import UserRole
from vzticket.modules.wallet_claim_tokens.dependencies import (
    ClaimTokenQuery,
    ClaimTokenSearchDep,
    WalletClaimTokenServiceDep,
)
from vzticket.modules.wallet_claim_tokens.schemas import (
    ClaimTokenCreate,
    ClaimTokenResponse,
    PaginatedClaimTokensResponse,
)
from vzticket.modules.wallet_claim_tokens.utils import render_deposit_success_html

router = APIRouter(prefix='/wallet/claims', tags=['Wallet Claims'])
organizer_only = Depends(RoleChecker(allowed_routes=[UserRole.ORGANIZER]))


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=PaginatedClaimTokensResponse,
)
async def get_claims(
    service: WalletClaimTokenServiceDep,
    params: ClaimTokenSearchDep,
    current_user: CurrentUserDep,
):
    """Retorna os tokens atribuídos ao usuário logado"""
    return await service.get_claims(current_user.id, params)


@router.get(
    '/pay',
    status_code=HTTPStatus.OK,
    response_class=HTMLResponse,
)
async def process_payment_via_qr(
    service: WalletClaimTokenServiceDep,
    data: ClaimTokenQuery,
    current_user: OptionalCurrentUserDep = None,
):
    """
    Endpoint público acionado pelo QR Code / Link de Pagamento.
    Processa depósitos, compras de ingressos ou taxas de eventos.
    """
    claim_data = await service.execute_claim(
        token=data.token, user=current_user
    )

    return render_deposit_success_html(claim_data)


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=ClaimTokenResponse,
)
async def create_claim_token(
    data: ClaimTokenCreate,
    service: WalletClaimTokenServiceDep,
    current_user: CurrentUserDep,
):
    """Gera um novo token/QR Code descartável"""
    return await service.create_claim_token(current_user.id, data)
