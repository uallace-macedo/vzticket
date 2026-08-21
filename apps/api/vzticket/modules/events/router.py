from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.core.libs.tmdb.exceptions import TMDBApiError, TMDBConnectionError
from vzticket.core.libs.tmdb.schemas import TMDBSearchResponse
from vzticket.modules.auth.dependencies import CurrentUserDep, RoleChecker
from vzticket.modules.events.dependencies import (
    EventSearchDep,
    EventServiceDep,
    SearchTMDBOptions,
)
from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.events.schemas import EventCreate, EventResponse
from vzticket.modules.users.model import UserRole

router = APIRouter(prefix='/events', tags=['Events'])
organizer_only = Depends(RoleChecker(allowed_routes=[UserRole.ORGANIZER]))


@router.get(
    '/tmdb',
    status_code=HTTPStatus.OK,
    response_model=TMDBSearchResponse,
    dependencies=[organizer_only],
    responses={
        **create_error_response(
            TMDBApiError,
            'Erro ao buscar na API do TMDB.'
        ),
        **create_error_response(
            TMDBConnectionError,
            'Erro de conexão com o TMDb.'
        ),
    }
)
async def search_tmdb(
    event_service: EventServiceDep,
    options: SearchTMDBOptions,
    _: CurrentUserDep
):
    """
    Utiliza a lib configurada do TMDB para fazer a busca com base
    nas options (apenas organizadores)
    """
    return await event_service.search_tmdb(options)


@router.post(
    '',
    status_code=HTTPStatus.CREATED,
    response_model=EventResponse,
    dependencies=[organizer_only],
)
async def create_event(
    event_service: EventServiceDep,
    data: EventCreate,
    _: CurrentUserDep,
):
    """Cria um novo evento (apenas organizadores)"""
    return await event_service.create(data)


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=list[EventResponse],
)
async def search_events(
    event_service: EventServiceDep,
    options: EventSearchDep
):
    """Busca eventos com base nos filtros informados"""
    return await event_service.search_events(options)


@router.get(
    '/{event_id}',
    status_code=HTTPStatus.OK,
    response_model=EventResponse,
    responses={
        **create_error_response(
            EventNotFoundError,
            'Evento não encontrado.'
        ),
    }
)
async def get_event_by_id(
    event_id: UUID,
    event_service: EventServiceDep,
):
    """Busca os detalhes de um evento pelo id"""
    return await event_service.get_by_id(event_id)
