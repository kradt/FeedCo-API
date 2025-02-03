import datetime

from pydantic import BaseModel, constr

from src.enums import RatingGrade
from src.reviews.schemas import ReviewFull, ReviewBase
from src.users.schemas import UserFull


class RatingBase(BaseModel):
    grade: RatingGrade


class RatingCreate(RatingBase):
    user_id: int
    review: ReviewBase | None = None


class RatingFull(RatingBase):
    id: int
    review: ReviewFull | None = None


class ApplicationBase(BaseModel):
    name: constr(max_length=100)
    description: constr(min_length=200, max_length=1000)
    date_created: datetime.datetime = datetime.datetime.now()
    hide_reviews: bool = False


class ApplicationFull(ApplicationBase):
    id: int
    user: UserFull
    ratings: list[RatingFull]


class ApplicationUpdateBase(BaseModel):
    name: constr(max_length=100) | None = None
    description: constr(min_length=200, max_length=1000) | None = None


class ApplicationUpdate(ApplicationUpdateBase):
    hide_reviews: bool | None = None


class ApplicationSearch(ApplicationUpdateBase):
    user_id: int | None = None
