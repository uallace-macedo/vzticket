from fastapi import FastAPI

app = FastAPI(
    title='EliteDEV Verzel - API',
    description='API da Plataforma de Eventos e Ingressos',
)


@app.get('/')
async def health():
    return {'status': 'ok'}
