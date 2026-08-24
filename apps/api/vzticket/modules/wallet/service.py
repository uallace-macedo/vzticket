from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.users.model import User
from vzticket.modules.wallet.repository import WalletRepository
from vzticket.modules.wallet.schemas import (
    PaginatedTransactionsResponse,
    WalletBalanceResponse,
    WalletTransactionResponse,
    WalletTransactionSearch,
)


class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.wallet_repository = WalletRepository(session)

    async def get_wallet(
        self,
        user: User,
        params: WalletTransactionSearch,
    ) -> WalletBalanceResponse:
        """Get current balance and paginated transactions of a user"""
        data, total, pages = await self.wallet_repository.get_by_user_id_paginated(
            user.id,
            params,
        )

        return WalletBalanceResponse(
            balance=user.balance,
            transactions=PaginatedTransactionsResponse(
                items=[WalletTransactionResponse.model_validate(t) for t in data],
                total=total,
                page=params.page,
                per_page=params.per_page,
                pages=pages,
            ),
        )
