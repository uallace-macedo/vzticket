import math
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.wallet.schemas import WalletTransactionSearch
from vzticket.modules.wallet.model import WalletTransaction


class WalletRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, transaction: WalletTransaction) -> WalletTransaction:
        """Add a new transaction to db"""
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)

        return transaction

    async def get_by_user_id_paginated(
        self,
        user_id: UUID,
        params: WalletTransactionSearch,
    ) -> tuple[Sequence[WalletTransaction], int, int]:
        """Search transactions of a user with pagination and filters"""
        
        base_stmt = select(WalletTransaction).where(WalletTransaction.user_id == user_id)

        if params.type:
            base_stmt = base_stmt.where(WalletTransaction.type == params.type)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (params.page - 1) * params.per_page
        pages = math.ceil(total / params.per_page) if total > 0 else 1

        stmt = (
            base_stmt
            .order_by(WalletTransaction.created_at.desc())
            .offset(offset)
            .limit(params.per_page)
        )

        result = await self.session.execute(stmt)
        transactions = result.scalars().all()

        return transactions, total, pages
