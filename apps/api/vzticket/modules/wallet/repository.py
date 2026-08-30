"""Data access layer for the wallet module."""

from vzticket.modules.wallet.models import WalletTransaction


import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.auth.models import User
from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    WalletClaimToken,
    WalletTransaction,
)


class WalletRepository:
    """Handles raw database operations for the wallet module."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        """Return the user with the given id, or ``None`` if not found."""
        return await self._session.get(User, user_id)

    async def get_user_by_id_for_update(self, user_id: uuid.UUID) -> User | None:
        """Return the user with row-locking, or ``None`` if not found."""
        result = await self._session.execute(
            select(User).where(User.id == user_id).with_for_update()
        )
        return result.scalar_one_or_none()

    async def get_claim_token_for_update(
        self, token: str
    ) -> WalletClaimToken | None:
        """Return the claim token with row-locking, or ``None`` if not found."""
        result = await self._session.execute(
            select(WalletClaimToken)
            .where(WalletClaimToken.token == token)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def create_claim_token(
        self, token: WalletClaimToken
    ) -> WalletClaimToken:
        """Persist a new claim token and return it."""
        self._session.add(token)
        await self._session.flush()
        return token

    async def create_transaction(
        self, transaction: WalletTransaction
    ) -> WalletTransaction:
        """Persist a new transaction and return it."""
        self._session.add(transaction)
        await self._session.flush()
        return transaction

    async def get_user_transactions(
        self, user_id: uuid.UUID
    ) -> list[WalletTransaction]:
        """Return all transactions for a user, newest first."""
        result = await self._session.execute(
            select(WalletTransaction)
            .where(WalletTransaction.user_id == user_id)
            .order_by(WalletTransaction.created_at.desc())
        )
        return list[WalletTransaction](result.scalars().all())

    async def get_pending_claim_token(
        self, user_id: uuid.UUID
    ) -> WalletClaimToken | None:
        """Return the pending claim token for a user, or ``None``."""
        result = await self._session.execute(
            select(WalletClaimToken).where(
                WalletClaimToken.user_id == user_id,
                WalletClaimToken.status == ClaimTokenStatus.PENDING,
            )
        )
        return result.scalar_one_or_none()

    async def commit(self) -> None:
        """Commit the current transaction."""
        await self._session.commit()