import datetime

from sqlalchemy import ForeignKey, TypeDecorator, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.core import Base


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
    user: Mapped["User"] = relationship(back_populates="refresh_keys")
