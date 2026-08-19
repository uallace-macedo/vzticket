from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from verzel.core.exceptions.base import AppError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppError)
    async def app_error_handler(req: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'code': exc.code,
                'detail': exc.message
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        req: Request,
        exc: RequestValidationError
    ) -> JSONResponse:
        errors = [
            {
                'field': ' -> '.join(str(loc) for loc in err['loc'][1:]),
                'message': err['msg']
            }
            for err in exc.errors()
        ]

        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content={
                'code': 'VALIDATION_ERROR',
                'detail': 'Dados de requisição inválidos',
                'errors': errors
            }
        )
