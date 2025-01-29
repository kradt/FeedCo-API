import datetime

from sqlalchemy import ForeignKey, TypeDecorator, DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from app import pwd_context


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    refresh_keys: Mapped[list["RefreshToken"]] = relationship(back_populates="user")

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
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(TZDateTime())
    expires_at: Mapped[datetime.datetime] = mapped_column(TZDateTime())
    revoked: Mapped[bool] = mapped_column(default=False)

    user: Mapped[User] = relationship(back_populates="refresh_keys")
