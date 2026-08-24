from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.events_payout.model import EventPayout, PayoutStatus
from vzticket.modules.events.model import Event, EventStatus
from vzticket.modules.wallet.model import TransactionType, WalletTransaction


class EventPayoutRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, payout: EventPayout) -> EventPayout:
        self.session.add(payout)
        await self.session.commit()
        await self.session.refresh(payout)
        return payout

    async def get_by_event_id(self, event_id: UUID) -> Optional[EventPayout]:
        stmt = select(EventPayout).where(EventPayout.event_id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_events_starting_at(self, date_start: datetime, date_end: datetime) -> list[Event]:
        stmt = select(Event).where(
            Event.status == EventStatus.ACTIVE,
            Event.event_date >= date_start,
            Event.event_date <= date_end
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_pending_payouts_due(self, limit_date: datetime) -> list[EventPayout]:
        stmt = select(EventPayout).where(
            EventPayout.status == PayoutStatus.PENDING,
            EventPayout.scheduled_for <= limit_date
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def calculate_event_sales_balance(self, event_id: UUID) -> tuple[Decimal, int]:
        purchases_stmt = select(
            func.coalesce(func.sum(WalletTransaction.amount), Decimal('0.00')),
            func.count(WalletTransaction.id)
        ).where(
            WalletTransaction.event_id == event_id,
            WalletTransaction.type == TransactionType.TICKET_PURCHASE
        )
        purchases_res = await self.session.execute(purchases_stmt)
        total_purchases, total_tickets = purchases_res.one()

        refunds_stmt = select(
            func.coalesce(func.sum(WalletTransaction.amount), Decimal('0.00')),
            func.count(WalletTransaction.id)
        ).where(
            WalletTransaction.event_id == event_id,
            WalletTransaction.type == TransactionType.TICKET_REFUND
        )
        refunds_res = await self.session.execute(refunds_stmt)
        total_refunds, refunded_tickets = refunds_res.one()

        net_sales = Decimal(str(total_purchases)) - Decimal(str(total_refunds))
        net_tickets = total_tickets - refunded_tickets

        return net_sales, max(net_tickets, 0)
