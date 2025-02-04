import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.comments.models import Comment
from src.database.core import Base


class Review(Base):
    """
    Review from user that tested application
    After tests users can write review where describe what did satisfy them and what not
    :param title: Summarized info about review
    :param body: main content of review
    :param date_created: date when review was created
    """
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column(String(1000))
    date_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    deleted: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="reviews")

    rating: Mapped["Rating"] = relationship(back_populates="review")
    reviews_votes: Mapped[list["ReviewVotes"]] = relationship(back_populates="review")
    comments: Mapped[list["Comment"]] = relationship(back_populates="review")

    @property
    def votes_positive(self):
        return len([vote for vote in self.reviews_votes if vote.vote_type is True])

    @property
    def votes_negative(self):
        return len([vote for vote in self.reviews_votes if vote.vote_type is False])


class ReviewVotes(Base):
    """
    Votes from users about reviews
    User can support review or not
    :param vote_type: if true user supports review
    """
    __tablename__ = "review_votes"
    id: Mapped[int] = mapped_column(primary_key=True)
    vote_type: Mapped[bool] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="reviews_votes")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    review: Mapped[Review] = relationship(back_populates="reviews_votes")
