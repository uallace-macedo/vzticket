from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vzticket.core.exceptions import register_exception_handlers
from vzticket.core.exceptions.schemas import ValidationErrorResponse
from vzticket.core.settings import settings
from vzticket.router import api_router
from vzticket.lifespan import lifespan

origins = [settings.WEB_URL]
app = FastAPI(
    title='EliteDEV Verzel - API',
    description='API da Plataforma de Eventos e Ingressos',
    responses={
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'model': ValidationErrorResponse,
            'description': 'Erro de validação nos campos informados.',
        }
    },
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
register_exception_handlers(app)
