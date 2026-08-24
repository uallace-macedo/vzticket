from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from vzticket.core.libs.tmdb.client import TMDBClient
from vzticket.core.libs.tmdb.exceptions import TMDBApiError, TMDBConnectionError
from vzticket.core.libs.tmdb.schemas import TMDBSearchResponse


async def test_tmdb_client_search_success(monkeypatch):
    mock_json = {
        'page': 1,
        'total_pages': 1,
        'total_results': 1,
        'results': [
            {
                'id': 100,
                'title': 'Matrix',
                'original_title': 'The Matrix',
                'overview': 'Um hacker descobre a verdade...',
                'vote_average': 8.7,
                'poster_path': '/poster.jpg',
                'media_type': 'movie',
                'backdrop_path': '/backdrop.jpg',
            }
        ],
    }

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.json.return_value = mock_json
    mock_response.raise_for_status.return_value = None

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    monkeypatch.setattr('httpx.AsyncClient.get', mock_client.get)

    client = TMDBClient()
    response = await client.search('Matrix')

    assert isinstance(response, TMDBSearchResponse)
    assert response.page == 1
    assert response.results[0].title == 'Matrix'


async def test_tmdb_client_search_http_status_error_raises_tmdb_api_error(
    monkeypatch,
):
    mock_request = httpx.Request('GET', 'https://api.themoviedb.org/3/search/multi')
    mock_response = httpx.Response(401, request=mock_request)

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    monkeypatch.setattr('httpx.AsyncClient.get', mock_client.get)

    client = TMDBClient()

    with pytest.raises(TMDBApiError) as exc_info:
        await client.search('Matrix')

    assert exc_info.value.status_code == HTTPStatus.UNAUTHORIZED


async def test_tmdb_client_search_request_error_raises_tmdb_connection_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.RequestError('Erro de conexão')

    monkeypatch.setattr('httpx.AsyncClient.get', mock_client.get)

    client = TMDBClient()

    with pytest.raises(TMDBConnectionError):
        await client.search('Matrix')
