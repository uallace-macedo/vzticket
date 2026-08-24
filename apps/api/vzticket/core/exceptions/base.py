from http import HTTPStatus


class AppError(Exception):
    """Application base exception"""
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    code: str = 'INTERNAL_SERVER_ERROR'

    def __init__(self, message: str = 'Ocorreu um erro interno no servidor.') -> None:
        self.message = message
        super().__init__(self.message)
