from typing import Type

from fastapi import FastAPI
from pydantic import BaseModel

from .base import AppError
from .schemas import ErrorResponse


def create_error_response(exception_cls: Type[AppError], description: str) -> dict:
    """Return an OpenAPI response definition for a given AppError.

    Parameters
    ----------
    exception_cls:
        The exception class that will be used for the response.
    description:
        Human‑readable description for the OpenAPI schema.

    Returns
    -------
    dict
        A dictionary suitable for FastAPI ``responses`` mapping.
    """
    return {
        "model": ErrorResponse,
        "description": description,
        "content": {
            "application/json": {
                "example": {
                    "code": exception_cls.code,
                    "detail": exception_cls.message,
                }
            }
        },
    }
