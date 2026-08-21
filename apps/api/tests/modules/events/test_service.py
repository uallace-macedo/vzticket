from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from vzticket.core.libs.tmdb.schemas import (
    TMDBSearchOptions,
    TMDBSearchResponse,
    TMDBSearchResult,
)
from vzticket.modules.events.exceptions import EventNotFoundError
from vzticket.modules.events.schemas import EventsSearch
from vzticket.modules.events.service import EventService


async def test_event_service_search_tmdb_success(session, monkeypatch):
    mock_tmdb_response = TMDBSearchResponse(
        page=1,
        total_pages=1,
        total_results=1,
        results=[
            TMDBSearchResult(
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
    search_dto = TMDBSearchOptions(title='Matrix', page=1)

    response = await event_service.search_tmdb(search_dto)

    mock_search.assert_awaited_once_with('Matrix', 1)
    assert response == mock_tmdb_response
    assert response.results[0].title == 'Matrix'


async def test_event_service_create_success(session, event_data):
    service = EventService(session)

    event = await service.create(event_data)

    assert event.id is not None
    assert event.title == "Show de Rock"
    assert event.available_tickets == event_data.available_tickets


async def test_event_service_get_by_id_success(session, event_data):
    service = EventService(session)
    created_event = await service.create(event_data)

    found_event = await service.get_by_id(created_event.id)

    assert found_event.id == created_event.id
    assert found_event.title == created_event.title


async def test_event_service_get_by_id_not_found_raises_error(session):
    service = EventService(session)

    with pytest.raises(EventNotFoundError):
        await service.get_by_id(uuid4())


async def test_event_service_search_events_success(session, event_data):
    service = EventService(session)
    await service.create(event_data)

    options = EventsSearch(title="Rock", limit=10, offset=0)
    results = await service.search_events(options)

    assert len(results) >= 1
    assert results[0].title == "Show de Rock"
