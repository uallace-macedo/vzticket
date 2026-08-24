from fastapi import APIRouter

from vzticket.modules.auth.router import router as auth_router
from vzticket.modules.events.router import router as events_router
from vzticket.modules.wallet.router import router as wallet_router
from vzticket.modules.wallet_claim_tokens.router import router as wallet_claim_tokens_router
from vzticket.modules.tickets.router import router as tickets_router
from vzticket.modules.gatekeeper.router import router as gatekeeper_router

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(auth_router)
api_router.include_router(events_router)
api_router.include_router(wallet_router)
api_router.include_router(wallet_claim_tokens_router)
api_router.include_router(tickets_router)
api_router.include_router(gatekeeper_router)
