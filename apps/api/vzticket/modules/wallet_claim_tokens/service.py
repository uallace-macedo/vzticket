import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.settings import settings
from vzticket.modules.events.model import Event, EventStatus
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
    ClaimTokenResponse,
    ClaimTokenSearch,
    PaginatedClaimTokensResponse,
)


class WalletClaimTokenService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = WalletClaimTokenRepository(session)

    async def create_claim_token(
        self, user_id: uuid.UUID, data: ClaimTokenCreate
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
        self, token: str, user: Optional[User] = None
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
            await self.repository.create(claim_item)
            raise TokenExpiredError()

        claim_item.status = ClaimTokenStatus.CLAIMED
        claim_item.claimed_at = now

        if claim_item.type == ClaimType.DEPOSIT:
            target_user = user
            if not target_user and claim_item.user_id:
                stmt_user = select(User).where(User.id == claim_item.user_id)
                res_user = await self.session.execute(stmt_user)
                target_user = res_user.scalar_one_or_none()

            if target_user:
                target_user.balance += claim_item.amount
                transaction = WalletTransaction(
                    user_id=target_user.id,
                    type=TransactionType.DEPOSIT,
                    amount=claim_item.amount,
                    description='Depósito via PIX',
                )
                self.session.add(transaction)

        elif claim_item.type == ClaimType.TICKET_PURCHASE:
            from vzticket.modules.tickets.service import TicketService

            target_user_id = user.id if user else claim_item.user_id
            if claim_item.target_id and target_user_id:
                ticket_service = TicketService(self.session)
                await ticket_service.process_pix_ticket_purchase(
                    event_id=claim_item.target_id,
                    buyer_id=target_user_id,
                    total_amount=claim_item.amount,
                )

        elif claim_item.type == ClaimType.EVENT_FEE:
            if claim_item.target_id:
                stmt_event = select(Event).where(Event.id == claim_item.target_id)
                res_event = await self.session.execute(stmt_event)
                event = res_event.scalar_one_or_none()

                if event:
                    event.status = EventStatus.ACTIVE

                    target_user_id = user.id if user else claim_item.user_id
                    if target_user_id:
                        transaction = WalletTransaction(
                            user_id=target_user_id,
                            event_id=event.id,
                            type=TransactionType.EVENT_CREATION_FEE,
                            amount=claim_item.amount,
                            description=f'Taxa de criação do evento: {event.title}',
                        )
                        self.session.add(transaction)

        return await self.repository.create(claim_item)

    async def get_claims(
        self, user_id: uuid.UUID, params: ClaimTokenSearch
    ) -> PaginatedClaimTokensResponse:
        data, total, pages = await self.repository.get_claims(user_id, params)

        return PaginatedClaimTokensResponse(
            items=[ClaimTokenResponse.model_validate(t) for t in data],
            total=total,
            page=params.page,
            per_page=params.per_page,
            pages=pages,
        )
