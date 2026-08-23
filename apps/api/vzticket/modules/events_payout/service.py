from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.events_payout.model import EventPayout, PayoutStatus
from vzticket.modules.events_payout.repository import EventPayoutRepository
from vzticket.modules.events.model import EventStatus
from vzticket.modules.events.repository import EventRepository
from vzticket.modules.users.repository import UserRepository
from vzticket.modules.wallet.model import TransactionType, WalletTransaction


class EventPayoutService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.payout_repository = EventPayoutRepository(session)
        self.event_repository = EventRepository(session)
        self.user_repository = UserRepository(session)

    async def schedule_payouts_for_today_events(self) -> int:
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        events_today = await self.payout_repository.get_events_starting_at(start_of_day, end_of_day)
        scheduled_count = 0

        for event in events_today:
            existing_payout = await self.payout_repository.get_by_event_id(event.id)
            if not existing_payout:
                payout = EventPayout(
                    event_id=event.id,
                    gross_amount=Decimal('0.00'),
                    platform_fee_amount=Decimal('0.00'),
                    net_amount=Decimal('0.00'),
                    organizer_id=event.organizer_id,
                    scheduled_for=start_of_day + timedelta(days=1)
                )
                await self.payout_repository.create(payout)
                scheduled_count += 1

        return scheduled_count

    async def process_due_payouts(self) -> int:
        now = datetime.now(timezone.utc)
        pending_payouts = await self.payout_repository.get_pending_payouts_due(now)
        processed_count = 0

        for payout in pending_payouts:
            async with self.session.begin_nested():
                event = await self.event_repository.get_by_id_for_update(payout.event_id)
                organizer = await self.user_repository.get_by_id_for_update(payout.organizer_id)

                if not event or not organizer:
                    continue

                net_ticket_sales, ticket_count = await self.payout_repository.calculate_event_sales_balance(event.id)

                unit_fee = event.service_fee
                total_platform_fee = unit_fee * Decimal(ticket_count)

                gross_amount = net_ticket_sales + total_platform_fee
                net_amount = net_ticket_sales

                organizer.balance += organizer.pending_balance
                organizer.pending_balance = Decimal('0.00')

                payout.gross_amount = gross_amount
                payout.platform_fee_amount = total_platform_fee
                payout.net_amount = net_amount
                payout.status = PayoutStatus.PAID
                payout.paid_at = now

                event.status = EventStatus.FINISHED

                payout_transaction = WalletTransaction(
                    user_id=organizer.id,
                    event_id=event.id,
                    ticket_id=None,
                    type=TransactionType.EVENT_PAYOUT,
                    amount=net_amount,
                    description=f'Repasse financeiro do evento: {event.title}',
                )
                self.session.add(payout_transaction)

                processed_count += 1

        await self.session.commit()
        return processed_count
