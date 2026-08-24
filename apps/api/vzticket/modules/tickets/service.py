import hashlib
import uuid
from datetime import datetime, timezone, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.events.model import Event, EventStatus
from vzticket.modules.tickets.exceptions import (
    EventNotActiveError,
    EventSalesEndedError,
    EventSalesNotStartedError,
    InsufficientBalanceForTicketError,
    InsufficientTicketsError,
    TicketNotFoundError,
    TicketAlreadyCancelledError,
    TicketRefund7DaysExpiredError,
    TicketRefundWindowClosedError
)
from vzticket.modules.tickets.model import Ticket, TicketStatus
from vzticket.modules.tickets.repository import TicketRepository
from vzticket.modules.tickets.schemas import (
    TicketPaymentMethod,
    TicketPurchase,
    TicketSearch,
    TicketPurchaseResponse,
    TicketResponse,
    PaginatedTicketsResponse,

)
from vzticket.modules.users.model import User
from vzticket.modules.wallet.model import TransactionType, WalletTransaction
from vzticket.modules.wallet_claim_tokens.model import ClaimType
from vzticket.modules.wallet_claim_tokens.schemas import ClaimTokenCreate
from vzticket.modules.wallet_claim_tokens.service import WalletClaimTokenService


class TicketService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.ticket_repository = TicketRepository(session)
        self.claim_token_service = WalletClaimTokenService(session)

    def _generate_qr_code_hash(self, event_id: uuid.UUID, user_id: uuid.UUID) -> str:
        raw_data = f'{event_id}:{user_id}:{uuid.uuid4()}:{datetime.now(timezone.utc).timestamp()}'
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    async def purchase_tickets(
        self, event_id: uuid.UUID, buyer: User, data: TicketPurchase
    ) -> TicketPurchaseResponse:
        stmt_event = select(Event).where(Event.id == event_id).with_for_update()
        res_event = await self.session.execute(stmt_event)
        event = res_event.scalar_one_or_none()

        if not event:
            raise EventNotFoundError()

        if event.status != EventStatus.ACTIVE:
            raise EventNotActiveError()

        now = datetime.now(timezone.utc)
        if event.sales_start_at and event.sales_start_at > now:
            raise EventSalesNotStartedError()

        if event.sales_end_at and event.sales_end_at < now:
            raise EventSalesEndedError()

        if event.available_tickets < data.quantity:
            raise InsufficientTicketsError()

        sales_deadline = event.sales_end_at or (
            event.event_date + timedelta(minutes=30)
        )

        if now > sales_deadline:
            raise EventSalesEndedError()

        unit_total = event.ticket_price + event.service_fee
        total_amount = unit_total * Decimal(data.quantity)

        if data.payment_method == TicketPaymentMethod.BALANCE:
            if buyer.balance < total_amount:
                raise InsufficientBalanceForTicketError()

            buyer.balance -= total_amount

            stmt_organizer = select(User).where(User.id == event.organizer_id)
            res_organizer = await self.session.execute(stmt_organizer)
            organizer = res_organizer.scalar_one_or_none()

            if organizer:
                organizer.pending_balance += event.ticket_price * Decimal(data.quantity)

            event.available_tickets -= data.quantity

            wallet_transaction = WalletTransaction(
                user_id=buyer.id,
                event_id=event.id,
                type=TransactionType.TICKET_PURCHASE,
                amount=total_amount,
                description=f'Compra de {data.quantity} ingresso(s) para o evento: {event.title}',
            )
            self.session.add(wallet_transaction)

            tickets_to_create: list[Ticket] = []
            for _ in range(data.quantity):
                qr_hash = self._generate_qr_code_hash(event.id, buyer.id)
                ticket = Ticket(
                    event_id=event.id,
                    user_id=buyer.id,
                    qr_code_hash=qr_hash,
                    status=TicketStatus.VALID,
                )
                tickets_to_create.append(ticket)

            created_tickets = await self.ticket_repository.create_many(tickets_to_create)

            return TicketPurchaseResponse(
                tickets=[TicketResponse.model_validate(t) for t in created_tickets],
                payment_method=TicketPaymentMethod.BALANCE,
            )

        claim_token = await self.claim_token_service.create_claim_token(
            user_id=buyer.id,
            data=ClaimTokenCreate(
                amount=total_amount,
                type=ClaimType.TICKET_PURCHASE,
                target_id=event.id,
            ),
        )

        return TicketPurchaseResponse(
            tickets=[],
            payment_method=TicketPaymentMethod.PIX,
            payment_token=claim_token.token,
        )

    async def process_pix_ticket_purchase(
        self, event_id: uuid.UUID, buyer_id: uuid.UUID, total_amount: Decimal
    ) -> list[Ticket]:
        stmt_event = select(Event).where(Event.id == event_id).with_for_update()
        res_event = await self.session.execute(stmt_event)
        event = res_event.scalar_one_or_none()

        if not event:
            raise EventNotFoundError()

        if event.status != EventStatus.ACTIVE:
            raise EventNotActiveError()

        now = datetime.now(timezone.utc)
        if event.sales_start_at and event.sales_start_at > now:
            raise EventSalesNotStartedError()

        if event.sales_end_at and event.sales_end_at < now:
            raise EventSalesEndedError()

        unit_total = event.ticket_price + event.service_fee
        quantity = int(total_amount // unit_total) if unit_total > 0 else 1
        if quantity < 1:
            quantity = 1

        if event.available_tickets < quantity:
            raise InsufficientTicketsError()

        stmt_organizer = select(User).where(User.id == event.organizer_id)
        res_organizer = await self.session.execute(stmt_organizer)
        organizer = res_organizer.scalar_one_or_none()

        if organizer:
            organizer.pending_balance += event.ticket_price * Decimal(quantity)

        event.available_tickets -= quantity

        wallet_transaction = WalletTransaction(
            user_id=buyer_id,
            event_id=event.id,
            type=TransactionType.TICKET_PURCHASE,
            amount=total_amount,
            description=f'Compra de {quantity} ingresso(s) via PIX para o evento: {event.title}',
        )
        self.session.add(wallet_transaction)

        tickets_to_create: list[Ticket] = []
        for _ in range(quantity):
            qr_hash = self._generate_qr_code_hash(event.id, buyer_id)
            ticket = Ticket(
                event_id=event.id,
                user_id=buyer_id,
                qr_code_hash=qr_hash,
                status=TicketStatus.VALID,
            )
            tickets_to_create.append(ticket)

        return await self.ticket_repository.create_many(tickets_to_create)

    async def get_user_tickets(
        self, user_id: uuid.UUID, params: TicketSearch
    ) -> PaginatedTicketsResponse:
        data, total, pages = await self.ticket_repository.get_by_user_id(user_id, params)

        return PaginatedTicketsResponse(
            items=[TicketResponse.model_validate(t) for t in data],
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=pages,
        )
    
    async def get_ticket_by_id(self, ticket_id: uuid.UUID) -> Ticket:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if not ticket:
            raise TicketNotFoundError()
        return ticket

    async def cancel_ticket(
        self,
        user_id: uuid.UUID,
        ticket_id: uuid.UUID
    ) -> Ticket:
        ticket = await self.ticket_repository.get_by_id_and_user_for_update(
            ticket_id, user_id
        )
        
        if not ticket:
            raise TicketNotFoundError()

        if ticket.status != TicketStatus.VALID:
            raise TicketAlreadyCancelledError()

        event = ticket.event
        buyer = ticket.user
        organizer = event.organizer

        now = datetime.now(timezone.utc)
        purchased_at = ticket.purchased_at.replace(tzinfo=timezone.utc) if ticket.purchased_at.tzinfo is None else ticket.purchased_at
        event_date = event.event_date.replace(tzinfo=timezone.utc) if event.event_date.tzinfo is None else event.event_date

        if (now - purchased_at).days >= 7:
            raise TicketRefund7DaysExpiredError()

        hours_until_event = (event_date - now).total_seconds() / 3600
        if hours_until_event < 24:
            raise TicketRefundWindowClosedError()

        base_refund = event.ticket_price + event.service_fee
        rate = Decimal('0.80') if hours_until_event < 48 else Decimal('1.00')

        refund_amount = base_refund * rate
        organizer_deduction = event.ticket_price * rate

        ticket.status = TicketStatus.CANCELLED
        event.available_tickets += 1

        buyer.balance += refund_amount

        if organizer:
            organizer.pending_balance = max(Decimal('0.00'), organizer.pending_balance - organizer_deduction)

        self.session.add(
            WalletTransaction(
                user_id=user_id,
                event_id=event.id,
                ticket_id=ticket.id,
                type=TransactionType.TICKET_REFUND,
                amount=refund_amount,
                description=f'Reembolso do ingresso para o evento: {event.title}',
            )
        )

        await self.session.commit()
        return ticket
