from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from vzticket.modules.wallet.model import TransactionType


class WalletTransactionResponse(BaseModel):
    id: UUID
    type: TransactionType
    amount: Decimal
    description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WalletTransactionSearch(BaseModel):
    type: Optional[TransactionType] = Field(
        default=None,
        description="Filtrar por tipo de transação"
    )
    page: int = Field(ge=1, default=1, description="Número da página")
    per_page: int = Field(
        ge=1,
        le=100,
        default=10,
        description="Itens por página (máx. 100)"
    )


class PaginatedTransactionsResponse(BaseModel):
    items: list[WalletTransactionResponse]
    total: int
    page: int
    per_page: int
    pages: int


class WalletBalanceResponse(BaseModel):
    balance: Decimal
    transactions: PaginatedTransactionsResponse
