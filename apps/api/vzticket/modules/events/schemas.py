from typing import Optional

from pydantic import BaseModel, Field


class SearchTMDB(BaseModel):
    title: str
    page: Optional[int] = None


class SearchEvents(BaseModel):
    title: Optional[str] = Field(default=None)
    limit: Optional[int] = Field(ge=1, default=10)
    offset: Optional[int] = Field(ge=0, default=0)
