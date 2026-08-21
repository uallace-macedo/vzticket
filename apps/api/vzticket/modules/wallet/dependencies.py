from typing import Annotated

from fastapi import Depends, Query

from vzticket.core.database import SessionDep
from vzticket.modules.wallet.schemas import WalletTransactionSearch
from vzticket.modules.wallet.service import WalletService


def get_wallet_service(session: SessionDep) -> WalletService:
    return WalletService(session)


WalletServiceDep = Annotated[WalletService, Depends(get_wallet_service)]
WalletSearchDep = Annotated[WalletTransactionSearch, Query()]
