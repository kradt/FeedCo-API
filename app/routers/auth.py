from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import create_user, get_refresh_token, get_db
from app.schemas.token import TokenSet
from app.schemas.user import BaseUser
from app import models
from app.services.auth import authenticate_user, create_token_set
from app.services.user import get_user_by_id

router = APIRouter(prefix="/auth")


@router.post("/login/", response_model=TokenSet)
async def get_auth_tokens(response: Response,
                    db: Annotated[Session, Depends(get_db)],
                    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Get access and refresh tokens to use routes that requires auth
    :param db: get and close db after work
    :param form_data: username and password
    :param response: object for define response
    :return: access token and refresh token
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username of password")
    token_set = create_token_set(db, user)
    response.set_cookie(
        key="refresh_token",
        value=token_set.refresh_token,
        httponly=True)
    return token_set


@router.post("/refresh/", response_model=TokenSet)
async def refresh_tokens(response: Response,
                   db: Annotated[Session, Depends(get_db)],
                   decoded_refresh_token: Annotated[dict, Depends(get_refresh_token)]):
    """
    According to specification we should recreate access and refresh tokens both during refreshing
    :return: TokenSet
    """
    user = get_user_by_id(db, decoded_refresh_token.get("user_id"))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials. User does not exist")
    token_set = create_token_set(db, user)
    response.set_cookie(
        key="refresh_token",
        value=token_set.refresh_token,
        httponly=True)
    return token_set


@router.post("/create-user/", response_model=BaseUser)
async def create_user(user: Annotated[models.User, Depends(create_user)]):
    """
    Registrate user or raise and error if user already exists
    :param user: created user from base
    :return: json with user data
    """
    return user
