"""Exception handling utilities for the VZTicket API."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .base import AppError
from .schemas import ErrorResponse, ValidationErrorItem, ValidationErrorResponse

__all__ = ["AppError", "register_exception_handlers", "ErrorResponse", "ValidationErrorResponse"]


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the FastAPI app.

    Handles :class:`AppError` and :class:`RequestValidationError` and returns
    standardized JSON responses in Portuguese.
    """

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        payload: dict[str, Any] = {
            "code": exc.code,
            "detail": exc.message,
        }
        return JSONResponse(status_code=exc.status_code, content=payload)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            ValidationErrorItem(
                field=err.get("loc", ["unknown"])[-1], message=err.get("msg", "erro desconhecido")
            ).model_dump()
            for err in exc.errors()
        ]
        payload: dict[str, Any] = {
            "code": "VALIDATION_ERROR",
            "detail": "Erro de validação.",
            "errors": errors,
        }
        return JSONResponse(status_code=422, content=payload)
