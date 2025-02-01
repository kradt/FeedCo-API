from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src import pwd_context, Base
from src.enums import AccountType


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