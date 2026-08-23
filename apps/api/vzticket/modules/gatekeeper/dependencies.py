from typing import Annotated

from fastapi import Depends

from vzticket.core.database import SessionDep
from vzticket.modules.gatekeeper.service import GatekeeperService


def get_gatekeeper_service(session: SessionDep) -> GatekeeperService:
    return GatekeeperService(session)


GatekeeperServiceDep = Annotated[
    GatekeeperService, Depends(get_gatekeeper_service)
]
