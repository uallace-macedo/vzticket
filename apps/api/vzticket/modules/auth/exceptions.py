"""Domain-specific exceptions for the auth module."""

from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class EmailAlreadyRegisteredError(AppError):
    """Raised when attempting to register an email that already exists."""

    status_code: int = HTTPStatus.CONFLICT.value
    code: str = 'EMAIL_ALREADY_REGISTERED'
    message: str = 'Este e-mail já está cadastrado.'


class InvalidCredentialsError(AppError):
    """Raised when the provided credentials do not match a valid user."""

    status_code: int = HTTPStatus.UNAUTHORIZED.value
    code: str = 'INVALID_CREDENTIALS'
    message: str = 'E-mail ou senha inválidos.'


class UnauthorizedError(AppError):
    """Raised when the request is not authenticated."""

    status_code: int = HTTPStatus.UNAUTHORIZED.value
    code: str = 'UNAUTHORIZED'
    message: str = 'Autenticação necessária para acessar este recurso.'


class InvalidTokenError(AppError):
    """Raised when a provided token is invalid, expired or malformed."""

    status_code: int = HTTPStatus.UNAUTHORIZED.value
    code: str = 'INVALID_TOKEN'
    message: str = 'Token inválido ou expirado.'
