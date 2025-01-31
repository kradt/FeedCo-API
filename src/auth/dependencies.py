import datetime
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, Cookie, Query, Path
from fastapi.security import SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src import models, pwd_context, oauth_scheme, config
from src.applications.schemas import ApplicationSearch
from src.auth.schemas import TokenData
from src.dependencies import get_db
from src.users.schemas import UserCreate, UserSearch
from src.users.service import get_user_by_id


def get_applications(db: Annotated[Session, Depends(get_db)],
                     queryset: Annotated[ApplicationSearch, Query()]):
    query = db.query(models.Application).filter_by(deleted=False)
    if queryset.name:
        query = query.filter(models.Application.name.like(f"%{queryset.name}%"))
    if queryset.description:
        query = query.filter(models.Application.description.like(f"%{queryset.description}%"))
    if queryset.user_id:
        query = query.filter_by(user_id=queryset.user_id)
    return query.all()


def get_users(db: Annotated[Session, Depends(get_db)],
             queryset: Annotated[UserSearch, Query()]):
    query = db.query(models.User).filter_by(deleted=False)
    if queryset.username:
        query = query.filter(models.User.username.like(f"%{queryset.username}%"))
    if queryset.email:
        query = query.filter(models.User.email.like(f"%{queryset.email}%"))
    if queryset.account_type:
        query = query.filter(models.User.account_type == queryset.account_type)
    if queryset.description:
        query = query.filter(models.User.description.like(f"%{queryset.description}%"))
    return query.all()


def get_user(db: Annotated[Session, Depends(get_db)], user_id: Annotated[str, Path()]):
    return get_user_by_id(db, user_id)


def create_user(user: UserCreate,
                db: Annotated[Session, Depends(get_db)]):
    """
    Create user and save it to base
    :param db: session to interact with db
    :param user: scheme with user data like password and username
    :return: user from base
    """
    if db.query(models.User).filter(
            or_(models.User.username==user.username,
                models.User.email==user.email)).first():
       raise HTTPException(status_code=400, detail="User already exists")
    user_in_base = models.User(
        username=user.username,
        password=pwd_context.hash(user.password),
        email=user.email,
        account_type=user.account_type
    )
    db.add(user_in_base)
    db.commit()
    return user


def get_current_user(security_scopes: SecurityScopes,
                     token: Annotated[str, Depends(oauth_scheme)],
                     db: Annotated[Session, Depends(get_db)]):
    """
    Get current logged user using jwt token in headers
    :param security_scopes: scopes to manage what routes user can use
    :param db: session to interact with db
    :param token: jwt token from header 'Authorization'
    :return: user from database
    """
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    cred_exceptions = HTTPException(
        status_code=401,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": authenticate_value})
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.JWT_ALGORITHM)
        token_data = TokenData.model_validate(payload)
    except InvalidTokenError:
        raise cred_exceptions
    except ValidationError:
        raise cred_exceptions
    user = db.query(models.User).filter_by(id=token_data.user_id).first()
    if not user:
        raise cred_exceptions
    # If it is not access token, raise an exception
    if token_data.token_type != config.ACCESS_TOKEN_TYPE:
        raise cred_exceptions
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


def get_refresh_token(db: Annotated[Session, Depends(get_db)],
                      refresh_token: Annotated[str | None, Cookie()] = None) -> dict:
    """
    Get refresh token from cookies, decode it and validate
    :param db: session to interact with db
    :param refresh_token: cookie with refresh_token
    :return: decoded refresh_token
    """
    refresh_token_exception = HTTPException(status_code=401, detail="Invalid Refresh Token")
    if not refresh_token:
        raise refresh_token_exception
    try:
        decoded_refresh_token = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    except InvalidTokenError:
        raise refresh_token_exception
    if decoded_refresh_token.get("token_type") != config.REFRESH_TOKEN_TYPE:
        raise refresh_token_exception
    token_from_base = db.query(models.RefreshToken).filter_by(token=refresh_token).first()
    if not token_from_base:
        raise refresh_token_exception
    elif token_from_base.revoked:
        raise refresh_token_exception
    elif token_from_base.expires_at <= datetime.datetime.now(datetime.timezone.utc):
        raise refresh_token_exception
    return decoded_refresh_token
