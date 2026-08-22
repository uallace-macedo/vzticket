from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vzticket.modules.tickets.model import TicketStatus


class TicketPaymentMethod(str, Enum):
    BALANCE = 'balance'
    PIX = 'pix'


class TicketPurchase(BaseModel):
    quantity: int = Field(default=1, ge=1, le=10, description='Quantidade de ingressos (máximo 10 por compra)')
    payment_method: TicketPaymentMethod = Field(default=TicketPaymentMethod.BALANCE)


class TicketResponse(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    qr_code_hash: str
    share_token: UUID
    status: TicketStatus
    purchased_at: datetime
    validated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TicketPurchaseResponse(BaseModel):
    tickets: list[TicketResponse] = Field(default_factory=list)
    payment_method: TicketPaymentMethod
    payment_token: Optional[str] = Field(
        default=None,
        description='UUID do WalletClaimToken gerado caso o pagamento seja PIX',
    )
