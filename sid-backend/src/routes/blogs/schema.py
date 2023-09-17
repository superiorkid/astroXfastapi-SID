from datetime import datetime

from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    title: str = Field(min_length=5, max_length=25)
    content: str


class ArticleInput(ArticleBase):
    pass


class ArticleOutput(ArticleBase):
    slug: str
    publication_date: datetime
    last_modified: datetime
