"""Pydantic schemas for the wallet module."""

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from vzticket.modules.wallet.models import (
    ClaimTokenStatus,
    ClaimTokenType,
    TransactionType,
)


class DepositRequest(BaseModel):
    """Payload for depositing funds into a wallet."""

    amount: Decimal = Field(gt=0, decimal_places=2)


class WalletBalanceResponse(BaseModel):
    """Public representation of a wallet balance."""

    balance: Decimal
    pending_balance: Decimal


class TransactionResponse(BaseModel):
    """Public representation of a wallet transaction."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    amount: Decimal
    type: TransactionType
    description: str
    created_at: datetime
    event_id: uuid.UUID | None
    ticket_id: uuid.UUID | None


class ClaimTokenResponse(BaseModel):
    """Public representation of a wallet claim token."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    token: str
    amount: Decimal
    type: ClaimTokenType
    status: ClaimTokenStatus
    expires_at: datetime
    created_at: datetime
