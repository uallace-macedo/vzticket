from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class TMDBConnectionError(AppError):
    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    code: str = 'TMDB_CONNECTION_ERROR'

    def __init__(self, message: str = 'Ocorreu um erro de conexão com o TMDb.') -> None:
        super().__init__(message)


class TMDBApiError(AppError):
    status_code: int
    code: str = 'TMDB_API_ERROR'

    def __init__(
        self,
        status_code: int = HTTPStatus.UNAUTHORIZED,
        message: str = 'Ocorreu um erro ao fazer a busca.'
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
