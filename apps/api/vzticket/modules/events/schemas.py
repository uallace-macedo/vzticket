from typing import Optional

from pydantic import BaseModel


class SearchTMDB(BaseModel):
    title: str
    page: Optional[int] = None
