from typing import Type

from verzel.core.exceptions.base import AppError
from verzel.core.exceptions.schemas import ErrorResponse


def create_error_response(
    exception_cls: Type[AppError],
    description: str = 'Erro da aplicação',
) -> dict:
    """Generates swagger documentation structure using exception class"""
    instance = exception_cls()

    return {
        instance.status_code: {
            'model': ErrorResponse,
            'description': description,
            'content': {
                'application/json': {
                    'example': {
                        'code': instance.code,
                        'detail': instance.message,
                    }
                }
            },
        }
    }
