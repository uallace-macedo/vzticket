from http import HTTPStatus

from fastapi import FastAPI

from vzticket.core.exceptions import register_exception_handlers
from vzticket.core.exceptions.schemas import ValidationErrorResponse
from vzticket.router import api_router

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
