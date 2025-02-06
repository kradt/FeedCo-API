import datetime

from pydantic import BaseModel

from src.comments.schemas import CommentFull


class ReviewBase(BaseModel):
    title: str
    body: str


class Review(ReviewBase):
    date_created: datetime.datetime


class ReviewFull(Review):
    id: int
    comments: list[CommentFull] | None = None
    votes_positive: int
    votes_negative: int


class ReviewUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
