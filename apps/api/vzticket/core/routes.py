"""Centralized route registry for the VZTicket API.

All feature module routers must be included here instead of being registered
directly in ``vzticket.main``.
"""

from fastapi import APIRouter

from vzticket.modules.auth.routers.v1 import router as auth_router
from vzticket.modules.wallet.routers.v1 import router as wallet_router

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(auth_router)
main_router.include_router(wallet_router)
