from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.wallet_claim_tokens.model import (
    ClaimTokenStatus,
    WalletClaimToken,
)


class WalletClaimTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, claim_token: WalletClaimToken) -> WalletClaimToken:
        self.session.add(claim_token)
        await self.session.commit()
        await self.session.refresh(claim_token)
        return claim_token

    async def get_by_token(
        self,
        token: str
    ) -> WalletClaimToken | None:
        stmt = (
            select(WalletClaimToken)
            .where(WalletClaimToken.token == token)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_pending_by_user(
        self, user_id: UUID
    ) -> list[WalletClaimToken]:
        now = datetime.now(timezone.utc)
        stmt = select(WalletClaimToken).where(
            WalletClaimToken.user_id == user_id,
            WalletClaimToken.status == ClaimTokenStatus.PENDING,
            WalletClaimToken.expires_at > now,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def save(self, claim_token: WalletClaimToken) -> WalletClaimToken:
        await self.session.commit()
        await self.session.refresh(claim_token)
        return claim_token
