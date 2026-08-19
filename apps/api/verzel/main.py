from http import HTTPStatus

from fastapi import FastAPI

from verzel.core.exceptions import register_exception_handlers
from verzel.core.exceptions.schemas import ValidationErrorResponse
from verzel.router import api_router

app = FastAPI(
    title='EliteDEV Verzel - API',
    description='API da Plataforma de Eventos e Ingressos',
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'model': ValidationErrorResponse,
            'description': 'Erro de validação nos campos informados.',
        }
    },
)


app.include_router(api_router)
register_exception_handlers(app)
