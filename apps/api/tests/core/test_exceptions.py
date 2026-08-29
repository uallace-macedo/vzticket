import pytest
from httpx import AsyncClient

from vzticket.core.exceptions.base import AppError
from vzticket.main import app


@app.get('/_test/error')
async def dummy_error():
    raise AppError('Erro de teste')


@app.post('/_test/validate')
async def dummy_validate(name: str):
    return {'name': name}


@pytest.mark.asyncio
async def test_app_error_response(client: AsyncClient):
    response = await client.get('/_test/error')
    assert response.status_code == 500
    data = response.json()
    assert data['code'] == 'INTERNAL_SERVER_ERROR'
    assert data['detail'] == 'Erro de teste'


@pytest.mark.asyncio
async def test_validation_error_response(client: AsyncClient):
    response = await client.post('/_test/validate', json={})
    assert response.status_code == 422
    data = response.json()
    assert data['code'] == 'VALIDATION_ERROR'
    assert data['detail'] == 'Erro de validação.'
    assert isinstance(data['errors'], list)
    assert len(data['errors']) > 0

    error_item = data['errors'][0]
    assert 'field' in error_item
    assert 'message' in error_item
