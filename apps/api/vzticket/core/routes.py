"""Centralized route registry for the VZTicket API.

All feature module routers must be included here instead of being registered
directly in ``vzticket.main``.
"""

from fastapi import APIRouter

main_router = APIRouter(prefix='/api/v1')

# Feature routers will be included here as they are implemented, e.g.:
# from vzticket.modules.auth.v1 import router as auth_router
# main_router.include_router(auth_router)