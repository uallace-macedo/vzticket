from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vzticket.core.config import settings
from vzticket.core.exceptions import register_exception_handlers
from vzticket.core.routes import main_router

app = FastAPI(title=settings.app_name)

# Register global exception handlers
register_exception_handlers(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Register centralized route registry
app.include_router(main_router)


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}
