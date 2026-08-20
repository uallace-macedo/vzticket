from sqlalchemy.ext.asyncio import AsyncSession

from vzticket.core.libs.tmdb.client import TMDBClient
from vzticket.core.libs.tmdb.schemas import TMDBSearchResponse, TMDBSearchOptions


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self.tmdb_client = TMDBClient()
        self.session = session

    async def search_tmdb(self, options: TMDBSearchOptions) -> TMDBSearchResponse:
        """Uses TMDB Lib to search movies, tv shows and people"""
        return await self.tmdb_client.search(
            options.title,
            options.page
        )
