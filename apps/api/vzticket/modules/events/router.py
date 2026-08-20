from http import HTTPStatus

from fastapi import APIRouter

from vzticket.core.exceptions.swagger import create_error_response
from vzticket.core.libs.tmdb.exceptions import TMDBApiError, TMDBConnectionError
from vzticket.core.libs.tmdb.schemas import TMDBSearchResponse
from vzticket.modules.auth.dependencies import CurrentUserDep
from vzticket.modules.events.dependencies import EventServiceDep
from vzticket.modules.events.dependencies import SearchTMDBOptions

router = APIRouter(prefix='/events', tags=['Events'])


@router.get(
    '',
    status_code=HTTPStatus.OK,
    response_model=TMDBSearchResponse,
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
    """Utiliza a lib configurada do TMDB para fazer a busca com base nas options"""
    return await event_service.search_tmdb(options)
