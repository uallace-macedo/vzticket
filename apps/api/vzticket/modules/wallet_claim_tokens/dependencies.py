from typing import Annotated

from fastapi import Depends, Query

from vzticket.core.database import SessionDep
from vzticket.modules.wallet_claim_tokens.schemas import (
    ClaimTokenClaim,
    ClaimTokenSearch,
)
from vzticket.modules.wallet_claim_tokens.service import WalletClaimTokenService


def get_wallet_claim_token_service(
    session: SessionDep,
) -> WalletClaimTokenService:
    return WalletClaimTokenService(session)


WalletClaimTokenServiceDep = Annotated[
    WalletClaimTokenService, Depends(get_wallet_claim_token_service)
]

ClaimTokenQuery = Annotated[ClaimTokenClaim, Query()]
ClaimTokenSearchDep = Annotated[ClaimTokenSearch, Query()]
