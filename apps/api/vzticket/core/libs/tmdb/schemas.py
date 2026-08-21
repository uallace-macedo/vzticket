from typing import Optional

from pydantic import AliasChoices, BaseModel, Field, computed_field

from vzticket.core.settings import settings


class TMDBSearchResult(BaseModel):
    id: int

    title: str = Field(
        validation_alias=AliasChoices(
            'title',
            'name'
        )
    )

    original_title: str = Field(
        validation_alias=AliasChoices('original_title', 'original_name')
    )

    overview: str = ''
    vote_average: float = 0
    poster_path: Optional[str] = None
    media_type: Optional[str] = None
    backdrop_path: Optional[str] = None

    @computed_field
    def poster_url(self) -> str | None:
        """Generates complete poster url"""
        url = f'{settings.TMDB_IMAGE_BASE_URL}{self.poster_path}'
        return url if self.poster_path else None

    @computed_field
    def backdrop_url(self) -> str | None:
        """Generates complete banner url"""
        url = f'{settings.TMDB_IMAGE_BASE_URL}{self.backdrop_path}'
        return url if self.backdrop_path else None


class TMDBSearchResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results: list[TMDBSearchResult]


class TMDBSearchOptions(BaseModel):
    title: str
    page: Optional[int] = None
