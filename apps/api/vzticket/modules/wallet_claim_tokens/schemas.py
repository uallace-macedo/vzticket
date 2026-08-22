from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vzticket.modules.wallet_claim_tokens.model import ClaimTokenStatus, ClaimType


class ClaimTokenCreate(BaseModel):
    amount: Decimal = Field(gt=Decimal('0.00'), decimal_places=2)
    type: ClaimType = Field(default=ClaimType.DEPOSIT)
    target_id: Optional[UUID] = Field(
        default=None,
        description='ID do objeto associado (ex: ticket_id, event_id)'
    )


class ClaimTokenClaim(BaseModel):
    token: str = Field(min_length=36, max_length=36)


class ClaimTokenResponse(BaseModel):
    id: UUID
    token: str
    amount: Decimal
    type: ClaimType
    status: ClaimTokenStatus
    expires_at: datetime
    created_at: datetime
    claimed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ClaimTokenSearch(BaseModel):
    type: Optional[ClaimType] = Field(default=None)
    status: Optional[ClaimTokenStatus] = Field(default=None)
    page: int = Field(ge=1, default=1, description='Número da página')
    per_page: int = Field(
        ge=1, le=100, default=10, description='Itens por página (máx. 100)'
    )


class PaginatedClaimTokensResponse(BaseModel):
    items: list[ClaimTokenResponse]
    total: int
    page: int
    per_page: int
    pages: int
