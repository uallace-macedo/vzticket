"""Business logic for the wallet module."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from vzticket.modules.wallet.exceptions import (
    ClaimTokenAlreadyUsedError,
    ExpiredClaimTokenError,
    InvalidClaimTokenError,
)
from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    ClaimTokenType,
    TransactionType,
    WalletClaimToken,
    WalletTransaction,
)
from vzticket.modules.wallet.repository import WalletRepository


class WalletService:
    """Encapsulates wallet business rules."""

    def __init__(self, repository: WalletRepository) -> None:
        self._repository = repository

    async def create_deposit_claim(
        self, user_id: uuid.UUID, amount: Decimal
    ) -> WalletClaimToken:
        """Create a PENDING deposit claim token expiring in 15 minutes."""
        token = WalletClaimToken(
            token=str(uuid.uuid4()),
            amount=amount,
            type=ClaimTokenType.DEPOSIT,
            user_id=user_id,
            status=ClaimTokenStatus.PENDING,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        )
        created = await self._repository.create_claim_token(token)
        await self._repository.commit()
        return created

    async def claim_token(
        self, token_str: str, current_user_id: uuid.UUID
    ) -> WalletTransaction:
        """Atomically claim a deposit token and credit the user's balance.

        Raises
        ------
        InvalidClaimTokenError
            If the token does not exist or does not belong to the user.
        ClaimTokenAlreadyUsedError
            If the token is not in a PENDING state.
        ExpiredClaimTokenError
            If the token has expired.
        """
        token = await self._repository.get_claim_token_for_update(token_str)
        if token is None or token.user_id != current_user_id:
            raise InvalidClaimTokenError
        if token.status != ClaimTokenStatus.PENDING:
            raise ClaimTokenAlreadyUsedError
        if token.expires_at <= datetime.now(timezone.utc):
            token.status = ClaimTokenStatus.EXPIRED
            await self._repository.commit()
            raise ExpiredClaimTokenError

        user = await self._repository.get_user_by_id_for_update(current_user_id)
        if user is None:
            raise InvalidClaimTokenError

        token.status = ClaimTokenStatus.CLAIMED
        token.claimed_at = datetime.now(timezone.utc)
        user.balance += token.amount

        transaction = WalletTransaction(
            user_id=current_user_id,
            amount=token.amount,
            type=TransactionType.DEPOSIT,
            description='Depósito via cobrança PIX',
        )
        created = await self._repository.create_transaction(transaction)
        await self._repository.commit()
        return created

    async def get_balance(self, user_id: uuid.UUID) -> dict:
        """Return the user's available and pending balances."""
        user = await self._repository.get_user_by_id(user_id)
        return {
            'balance': user.balance,
            'pending_balance': user.pending_balance,
        }

    async def get_history(
        self, user_id: uuid.UUID
    ) -> list[WalletTransaction]:
        """Return the user's transaction history."""
        return await self._repository.get_user_transactions(user_id)

    async def get_pending_deposit(
        self, user_id: uuid.UUID
    ) -> WalletClaimToken | None:
        """Return the user's pending deposit claim, or ``None``."""
        return await self._repository.get_pending_claim_token(user_id)
