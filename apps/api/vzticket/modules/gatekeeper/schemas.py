from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ValidateTicketRequest(BaseModel):
    qr_code_hash: str
    event_id: UUID


class ValidateTicketResponse(BaseModel):
    ticket_id: UUID
    event_id: UUID
    buyer_name: str
    buyer_email: str
    status: str
    validated_at: datetime
    message: str = 'Entrada liberada com sucesso!'

    model_config = ConfigDict(from_attributes=True)
