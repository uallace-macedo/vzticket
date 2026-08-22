from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.libs.tmdb.client import TMDBClient
from vzticket.core.libs.tmdb.schemas import TMDBSearchOptions, TMDBSearchResponse
from vzticket.core.settings import settings
from vzticket.modules.events.exceptions import (
    EventNotFoundError,
    InsufficientBalanceForFeeError,
)
from vzticket.modules.events.model import Event, EventStatus
from vzticket.modules.events.repository import EventRepository
from vzticket.modules.events.schemas import (
    EventCreate,
    EventCreatedResponse,
    EventResponse,
    EventsSearch,
    PaymentMethod,
)
from vzticket.modules.events.utils import slugify_city
from vzticket.modules.users.model import User
from vzticket.modules.wallet.model import TransactionType, WalletTransaction
from vzticket.modules.wallet_claim_tokens.model import ClaimType
from vzticket.modules.wallet_claim_tokens.schemas import ClaimTokenCreate
from vzticket.modules.wallet_claim_tokens.service import WalletClaimTokenService


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.tmdb_client = TMDBClient()
        self.event_repository = EventRepository(session)
        self.claim_token_service = WalletClaimTokenService(session)

    async def search_tmdb(self, options: TMDBSearchOptions) -> TMDBSearchResponse:
        return await self.tmdb_client.search(options.title, options.page)

    def _calculate_ticket_service_fee(self, ticket_price: Decimal) -> Decimal:
        fixed_fee = Decimal(str(settings.TICKET_FEE_FIXED))
        percentage = Decimal(str(settings.TICKET_FEE_PERCENTAGE))

        variable_fee = (ticket_price * percentage).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )
        return fixed_fee + variable_fee

    async def create(self, user: User, data: EventCreate) -> EventCreatedResponse:
        initial_status = (
            EventStatus.ACTIVE
            if data.payment_method == PaymentMethod.BALANCE
            else EventStatus.PENDING_FEE
        )

        event_dict = data.model_dump(
            mode='python', exclude_unset=True, exclude={'payment_method'}
        )

        calculated_service_fee = self._calculate_ticket_service_fee(data.ticket_price)

        event = Event(
            **event_dict,
            organizer_id=user.id,
            status=initial_status,
            city_slug=slugify_city(data.city),
            service_fee=calculated_service_fee,
        )

        event_creation_fee = (event.ticket_price * Decimal(
            str(settings.EVENT_CREATION_FEE_PERCENTAGE)
        )).quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        if data.payment_method == PaymentMethod.BALANCE:
            if user.balance < event_creation_fee:
                raise InsufficientBalanceForFeeError()

            user.balance -= event_creation_fee
            created_event = await self.event_repository.create(event)

            transaction = WalletTransaction(
                user_id=user.id,
                event_id=created_event.id,
                type=TransactionType.EVENT_CREATION_FEE,
                amount=event_creation_fee,
                description=f'Taxa de criação do evento: {created_event.title}',
            )
            self.session.add(transaction)
            await self.session.commit()

            return EventCreatedResponse(
                event=EventResponse.model_validate(created_event),
                payment_method=PaymentMethod.BALANCE,
            )

        created_event = await self.event_repository.create(event)

        claim_token = await self.claim_token_service.create_claim_token(
            user_id=user.id,
            data=ClaimTokenCreate(
                amount=event_creation_fee,
                type=ClaimType.EVENT_FEE,
                target_id=created_event.id,
            ),
        )

        return EventCreatedResponse(
            event=EventResponse.model_validate(created_event),
            payment_method=PaymentMethod.PIX,
            payment_token=claim_token.token
        )

    async def get_by_id(self, event_id: UUID) -> Event:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundError()

        return event

    async def search_events(self, options: EventsSearch) -> list[Event]:
        return await self.event_repository.search_events(options)
