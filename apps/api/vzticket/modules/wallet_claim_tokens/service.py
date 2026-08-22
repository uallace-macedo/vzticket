import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.settings import settings
from vzticket.modules.users.model import User
from vzticket.modules.wallet.model import TransactionType, WalletTransaction
from vzticket.modules.wallet_claim_tokens.exceptions import (
    TokenAlreadyClaimedError,
    TokenExpiredError,
    TokenNotFoundError,
)
from vzticket.modules.wallet_claim_tokens.model import (
    ClaimTokenStatus,
    ClaimType,
    WalletClaimToken,
)
from vzticket.modules.wallet_claim_tokens.repository import (
    WalletClaimTokenRepository,
)
from vzticket.modules.wallet_claim_tokens.schemas import (
    ClaimTokenCreate,
)


class WalletClaimTokenService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = WalletClaimTokenRepository(session)

    async def create_claim_token(
        self,
        user_id: uuid.UUID,
        data: ClaimTokenCreate
    ) -> WalletClaimToken:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=settings.WALLET_CLAIM_EXP_MINUTES)

        claim_token = WalletClaimToken(
            token=str(uuid.uuid4()),
            amount=data.amount,
            type=data.type,
            created_at=now,
            expires_at=expires_at,
            user_id=user_id,
            target_id=data.target_id,
        )

        return await self.repository.create(claim_token)

    async def execute_claim(
        self,
        token: str,
        user: Optional[User] = None
    ) -> WalletClaimToken:
        now = datetime.now(timezone.utc)
        claim_item = await self.repository.get_by_token(token)

        if not claim_item:
            raise TokenNotFoundError()

        if claim_item.status == ClaimTokenStatus.CLAIMED:
            raise TokenAlreadyClaimedError()

        expires_at = claim_item.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if claim_item.status == ClaimTokenStatus.EXPIRED or expires_at < now:
            claim_item.status = ClaimTokenStatus.EXPIRED
            await self.repository.save(claim_item)
            raise TokenExpiredError()

        claim_item.status = ClaimTokenStatus.CLAIMED
        claim_item.claimed_at = now

        if claim_item.type == ClaimType.DEPOSIT:
            if user:
                user.balance += claim_item.amount
                transaction = WalletTransaction(
                    user_id=user.id,
                    type=TransactionType.DEPOSIT,
                    amount=claim_item.amount,
                    description='Depósito via QR Code/PIX',
                )
                self.session.add(transaction)

        elif claim_item.type == ClaimType.TICKET_PURCHASE:
            pass

        elif claim_item.type == ClaimType.EVENT_FEE:
            pass

        return await self.repository.save(claim_item)

    async def get_pending_by_user(self, user_id: uuid.UUID) -> list[WalletClaimToken]:
        return await self.repository.get_pending_by_user(user_id)
