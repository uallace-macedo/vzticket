from fastapi import FastAPI

from vzticket.core.config import settings
from vzticket.core.exceptions import register_exception_handlers

app = FastAPI(title=settings.app_name)

# Register global exception handlers
register_exception_handlers(app)


@app.get('/health')
async def health() -> dict[str, str]:
    return {'status': 'ok'}