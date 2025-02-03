from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.core import Base


class Comment(Base):
    """
    Comments are used for discussing review
    Users can write comments under review
    :param text: text of comment
    """
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    review: Mapped["Review"] = relationship(back_populates="comments")

    votes: Mapped[list["CommentVotes"]] = relationship(back_populates="comment")

    @property
    def votes_positive(self):
        return len([vote for vote in self.votes if vote.vote_type is True])

    @property
    def votes_negative(self):
        return len([vote for vote in self.votes if vote.vote_type is False])


class CommentVotes(Base):
    """
    Users can support comments or not
    :param vote_type: if true user support
    """
    __tablename__ = "comment_votes"
    id: Mapped[int] = mapped_column(primary_key=True)
    vote_type: Mapped[bool] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments_votes")

    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    comment: Mapped[Comment] = relationship(back_populates="votes")
