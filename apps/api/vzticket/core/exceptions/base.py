from http import HTTPStatus
from typing import Any


class AppError(Exception):
    """Base application error.

    All domain specific errors should inherit from this class.
    It provides a default HTTP status code, an error code and a default
    Portuguese message.
    """

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    code: str = "INTERNAL_SERVER_ERROR"
    message: str = "Ocorreu um erro interno no servidor."

    def __init__(self, message: str | None = None, *args: Any, **kwargs: Any) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message, *args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.message
