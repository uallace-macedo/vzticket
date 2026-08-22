import math
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.wallet_claim_tokens.model import (
    ClaimTokenStatus,
    WalletClaimToken,
)
from vzticket.modules.wallet_claim_tokens.schemas import ClaimTokenSearch


class WalletClaimTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, claim_token: WalletClaimToken) -> WalletClaimToken:
        self.session.add(claim_token)
        await self.session.commit()
        await self.session.refresh(claim_token)
        return claim_token

    async def get_by_token(self, token: str) -> WalletClaimToken | None:
        stmt = (
            select(WalletClaimToken)
            .where(WalletClaimToken.token == token)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_claims(
        self,
        user_id: UUID,
        params: ClaimTokenSearch,
    ) -> tuple[list[WalletClaimToken], int, int]:
        """Search claim tokens of a user with pagination and filters"""
        now = datetime.now(timezone.utc)

        update_stmt = (
            update(WalletClaimToken)
            .where(
                WalletClaimToken.user_id == user_id,
                WalletClaimToken.status == ClaimTokenStatus.PENDING,
                WalletClaimToken.expires_at <= now
            )
            .values(status=ClaimTokenStatus.EXPIRED)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

        base_stmt = select(WalletClaimToken).where(
            WalletClaimToken.user_id == user_id
        )

        if params.type:
            base_stmt = base_stmt.where(WalletClaimToken.type == params.type)

        if params.status:
            base_stmt = base_stmt.where(WalletClaimToken.status == params.status)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (params.page - 1) * params.per_page
        pages = math.ceil(total / params.per_page) if total > 0 else 1

        stmt = (
            base_stmt
            .order_by(WalletClaimToken.created_at.desc())
            .offset(offset)
            .limit(params.per_page)
        )

        result = await self.session.execute(stmt)
        tokens = result.scalars().all()

        return list(tokens), total, pages
