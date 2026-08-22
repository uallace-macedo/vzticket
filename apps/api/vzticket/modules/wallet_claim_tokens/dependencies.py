from typing import Annotated

from fastapi import Depends

from vzticket.core.database import SessionDep
from vzticket.modules.wallet_claim_tokens.service import WalletClaimTokenService


def get_wallet_claim_token_service(
    session: SessionDep,
) -> WalletClaimTokenService:
    return WalletClaimTokenService(session)


WalletClaimTokenServiceDep = Annotated[
    WalletClaimTokenService, Depends(get_wallet_claim_token_service)
]
