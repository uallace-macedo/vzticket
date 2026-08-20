from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class InvalidTokenError(AppError):
    """Token invalid signature"""
    status_code = HTTPStatus.UNAUTHORIZED
    code = 'INVALID_TOKEN'


class ExpiredTokenError(AppError):
    """Expired token"""
    status_code = HTTPStatus.UNAUTHORIZED
    code = 'EXPIRED_TOKEN'
