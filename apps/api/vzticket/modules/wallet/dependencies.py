"""Dependencies for the wallet module."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.database import get_db
from vzticket.modules.wallet.repository import WalletRepository
from vzticket.modules.wallet.service import WalletService


async def get_wallet_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> WalletService:
    """Provide a WalletService instance with injected WalletRepository."""
    return WalletService(repository=WalletRepository(db))


WalletServiceDep = Annotated[WalletService, Depends(get_wallet_service)]
