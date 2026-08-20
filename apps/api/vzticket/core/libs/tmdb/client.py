import httpx

from vzticket.core.libs.tmdb.exceptions import TMDBApiError, TMDBConnectionError
from vzticket.core.libs.tmdb.schemas import MovieSearchResponse
from vzticket.core.settings import settings


class TMDBClient:
    def __init__(self) -> None:
        self.base_url = settings.TMDB_BASE_URL
        self.api_key = settings.TMDB_API_KEY

    async def search(self, title: str, page: int = 1) -> MovieSearchResponse:
        """Search for movies, tv shows and people"""
        url = f'{self.base_url}/search/multi'
        params = {
            'query': title,
            'language': 'pt-BR',
            'page': page,
            'api_key': self.api_key
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()

                if 'results' in data:
                    data['results'] = [
                        item for item in data['results']
                        if item.get('media_type') != 'person'
                    ]

                return MovieSearchResponse(**data)
            except httpx.HTTPStatusError as exc:
                raise TMDBApiError(
                    status_code=exc.response.status_code
                )
            except httpx.RequestError:
                raise TMDBConnectionError()
