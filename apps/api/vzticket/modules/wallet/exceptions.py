"""Domain-specific exceptions for the wallet module."""

from http import HTTPStatus

from vzticket.core.exceptions.base import AppError


class InsufficientBalanceError(AppError):
    """Raised when a transaction exceeds the available balance."""

    status_code: int = HTTPStatus.BAD_REQUEST.value
    code: str = 'INSUFFICIENT_BALANCE'
    message: str = 'Saldo insuficiente para realizar a transação.'


class InvalidClaimTokenError(AppError):
    """Raised when a claim token is not found or is invalid."""

    status_code: int = HTTPStatus.BAD_REQUEST.value
    code: str = 'INVALID_CLAIM_TOKEN'
    message: str = 'Cobrança não encontrada ou inválida.'


class ExpiredClaimTokenError(AppError):
    """Raised when a claim token has already expired."""

    status_code: int = HTTPStatus.BAD_REQUEST.value
    code: str = 'EXPIRED_CLAIM_TOKEN'
    message: str = 'Cobrança PIX expirada.'


class ClaimTokenAlreadyUsedError(AppError):
    """Raised when a claim token has already been processed."""

    status_code: int = HTTPStatus.BAD_REQUEST.value
    code: str = 'CLAIM_TOKEN_ALREADY_USED'
    message: str = 'Cobrança já processada.'
