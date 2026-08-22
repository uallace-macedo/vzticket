from http import HTTPStatus

from fastapi import APIRouter

from vzticket.modules.auth.dependencies import CurrentUserDep
from vzticket.modules.wallet.dependencies import WalletSearchDep, WalletServiceDep
from vzticket.modules.wallet.schemas import WalletBalanceResponse

router = APIRouter(prefix='/wallet', tags=['Wallet'])


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=WalletBalanceResponse,
)
async def get_wallet(
    wallet_service: WalletServiceDep,
    params: WalletSearchDep,
    current_user: CurrentUserDep,
):
    """Busca o saldo atual e o extrato paginado de transações do usuário logado"""
    return await wallet_service.get_wallet(current_user, params)
