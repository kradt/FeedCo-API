import datetime
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends, Cookie
from fastapi.security import SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session

from src import oauth_scheme, config
from src.auth.schemas import TokenData
from src.dependencies import get_db
from src.users import service as user_service
from src.auth import service


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
    user = user_service.get(db, token_data.user_id)
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
    token_from_base = service.get_refresh_token_by_token_string(db, refresh_token)
    if not token_from_base:
        raise refresh_token_exception
    elif token_from_base.revoked:
        raise refresh_token_exception
    elif token_from_base.expires_at <= datetime.datetime.now(datetime.timezone.utc):
        raise refresh_token_exception
    return decoded_refresh_token
