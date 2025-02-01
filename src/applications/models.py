import datetime
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.core import Base
from src.enums import RatingGrade
from src.reviews.models import Review


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
    date_created: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    hide_reviews: Mapped[bool] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)
    # TODO: adding logo
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="applications")

    ratings: Mapped[list["Rating"]] = relationship(back_populates="application")


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
    user: Mapped["User"] = relationship(back_populates="ratings")

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True)
    review: Mapped["Review"] = relationship(back_populates="rating")

    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"))
    application: Mapped[Application] = relationship(back_populates="ratings")
