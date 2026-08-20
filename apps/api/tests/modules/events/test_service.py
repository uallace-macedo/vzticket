from unittest.mock import AsyncMock

from vzticket.core.libs.tmdb.schemas import MovieSearchResponse, MovieSearchResult
from vzticket.modules.events.schemas import SearchTMDB
from vzticket.modules.events.service import EventService


async def test_event_service_search_tmdb_success(session, monkeypatch):
    mock_tmdb_response = MovieSearchResponse(
        page=1,
        total_pages=1,
        total_results=1,
        results=[
            MovieSearchResult(
                id=1,
                title='Matrix',
                original_title='The Matrix',
                overview='Sinopse do filme',
                vote_average=8.7,
                poster_path='/poster.jpg',
                media_type='movie',
                backdrop_path='/backdrop.jpg',
            )
        ],
    )

    mock_search = AsyncMock(return_value=mock_tmdb_response)
    monkeypatch.setattr(
        'vzticket.core.libs.tmdb.client.TMDBClient.search',
        mock_search,
    )

    event_service = EventService(session)
    search_dto = SearchTMDB(title='Matrix', page=1)

    response = await event_service.search_tmdb(search_dto)

    mock_search.assert_awaited_once_with('Matrix', 1)
    assert response == mock_tmdb_response
    assert response.results[0].title == 'Matrix'
