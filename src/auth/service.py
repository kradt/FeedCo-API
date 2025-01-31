import datetime

import jwt
from sqlalchemy.orm import Session

from src import models, config
from src.auth.schemas import TokenSet


def authenticate_user(db: Session, username: str, password: str, ):
    """
    Check if user exists and password is correct
    :param db: session to interact with db
    :param username: User username
    :param password: User password
    :return: User from base or None
    """
    user = db.query(models.User).filter_by(username=username).first()
    if user and user.check_password_hash(password):
        return user


def create_jwt(data: dict, expires_at: datetime.timedelta):
    """
    Encode payload
    :param data: data to encode
    :param expires_at: timedelta declare when token will be expired
    :return: encoded jwt token
    """
    token_created_at = datetime.datetime.now(datetime.timezone.utc)
    jwt_token = jwt.encode(
        {
            **data,
            "exp": token_created_at + expires_at,
            "iat": token_created_at
        },
        config.SECRET_KEY,
        algorithm=config.JWT_ALGORITHM)
    return jwt_token


def create_access_token(data: dict, expires_at=datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)):
    return create_jwt(data, expires_at=expires_at)


def create_refresh_token(data: dict, expires_at=datetime.timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)):
    return create_jwt(data, expires_at=expires_at)


def get_refresh_token_by_token_string(db: Session, token):
    return db.query(models.RefreshToken).filter_by(token=token).first()


def save_refresh_token(
        db: Session,
        refresh_token: str,
        user: models.User,
        refresh_token_expires_days: datetime.timedelta):
    """
    Save refresh token in base
    :param db: session to interact with database
    :param refresh_token: refresh token that will be used to create access tokens
    :param user: User from base that wants to auth
    :param refresh_token_expires_days: time when refresh token will be expired
    :return: None
    """
    existed_refresh_token = db.query(models.RefreshToken).filter_by(user_id=user.id,
                                                                    revoked=False).first()
    if existed_refresh_token:
        existed_refresh_token.revoked = True
        db.add(existed_refresh_token)
    new_refresh_token = models.RefreshToken(
        token=refresh_token,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        expires_at=datetime.datetime.now(datetime.timezone.utc) + refresh_token_expires_days
    )
    new_refresh_token.user = user
    db.add(new_refresh_token)
    db.commit()


def create_token_set(db: Session, user: models.User, scopes: list[str]):
    """
    Create refresh and access token and return them as pydantic model
    :param scopes: permissions
    :param db: session to interact with database
    :param user: specific user object
    :return: TokenSet
    """
    access_token = create_access_token(
        dict(token_type=config.ACCESS_TOKEN_TYPE, user_id=user.id, scopes=scopes)
    )
    refresh_token = create_refresh_token(
        dict(token_type=config.REFRESH_TOKEN_TYPE, user_id=user.id, scopes=scopes)
    )
    save_refresh_token(db, refresh_token, user, datetime.timedelta(config.REFRESH_TOKEN_EXPIRE_DAYS))
    return TokenSet(access_token=access_token, refresh_token=refresh_token)
