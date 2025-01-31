import datetime
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, TypeDecorator, DateTime, String, Enum
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from src import pwd_context


class Base(DeclarativeBase):
    pass


class AccountType(PyEnum):
    startup = "startup"
    tester = "tester"


class RatingGrade(PyEnum):
    grade_1 = "1"
    grade_2 = "2"
    grade_3 = "3"
    grade_4 = "4"
    grade_5 = "5"


class User(Base):
    """
    User if person who use forum
    There are two types of account: for startup and for testers
    :param email: user email
    :param username: user username
    :param password: user password hash
    :param description: some words about user
    :param deleted: If True, user have deleted account
    :param account_type: can be startup or tester
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    account_type: Mapped[str] = mapped_column(Enum(AccountType), default=AccountType.tester)

    refresh_keys: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
    applications: Mapped[list["Application"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    reviews_votes: Mapped[list["ReviewVotes"]] = relationship(back_populates="user")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    comments_votes: Mapped[list["CommentVotes"]] = relationship(back_populates="user")
    ratings: Mapped[list["Rating"]] = relationship(back_populates="user")

    def check_password_hash(self, password: str):
        return pwd_context.verify(password, self.password)


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc)
        return value


class RefreshToken(Base):
    """
    RefreshTokens is used for refreshing access_token
    :param token: string variant of jwt token
    :param created_at: date when token was created
    :param expires_at: date when token will have expired
    :param revoked: if true token can't be used anymore
    """
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(TZDateTime())
    expires_at: Mapped[datetime.datetime] = mapped_column(TZDateTime())
    revoked: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="refresh_keys")


class Application(Base):
    """
    Application that need to be tested by users.
    Startups place their applications on the forum, and testers write reviews for that
    :param name: name of application
    :param description: In description startups should describe for what their project is used for
    :param date_created: date when application was placed on forum
    :param hide_reviews: if true, only startups will be able to read the reviews
    :param deleted: if true it mean that user deleted application
    """
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(1000))
    date_created: Mapped[datetime.datetime] = mapped_column()
    hide_reviews: Mapped[bool] = mapped_column()
    deleted: Mapped[bool] = mapped_column()
    # TODO: adding logo
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="applications")


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
    date_created: Mapped[datetime.datetime] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="reviews")

    rating: Mapped["Rating"] = relationship(back_populates="review")
    reviews_votes: Mapped["ReviewVotes"] = relationship(back_populates="review")
    comments: Mapped["Comment"] = relationship(back_populates="review")


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
    user: Mapped[User] = relationship(back_populates="reviews_votes")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    review: Mapped[Review] = relationship(back_populates="reviews_votes")


class Rating(Base):
    """
    Rating of Application
    Users is able to rate applications
    :param grade: grade from 1 to 5 that evaluate application
    """
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Enum(RatingGrade), default=RatingGrade.grade_5)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="ratings")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True)
    review: Mapped[Review] = relationship(back_populates="rating")


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
    user: Mapped[User] = relationship(back_populates="comments")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"))
    review: Mapped[Review] = relationship(back_populates="comments")

    votes: Mapped["CommentVotes"] = relationship(back_populates="comment")


class CommentVotes(Base):
    """
    Users can support comments or not
    :param vote_type: if true user support
    """
    __tablename__ = "comment_votes"
    id: Mapped[int] = mapped_column(primary_key=True)
    vote_type: Mapped[bool] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="comments_votes")

    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))
    comment: Mapped[Comment] = relationship(back_populates="votes")
