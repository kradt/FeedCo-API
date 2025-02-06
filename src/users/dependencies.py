from typing import Annotated

from fastapi import Depends, HTTPException, Path, Security
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.dependencies import get_db
from src.users.schemas import UserCreate, UserUpdate
from src.users import service, models


async def get_user_by_id(db: Annotated[Session, Depends(get_db)], user_id: Annotated[str, Path()]):
    user = service.get(db, user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {user_id} is not found")
    return user


async def create_user(
        user: UserCreate,
        db: Annotated[Session, Depends(get_db)]):
    """
    Create user and save it to base
    :param db: session to interact with db
    :param user: scheme with user data like password and username
    :return: user from base
    """
    if service.exists(db, user.email, user.username):
       raise HTTPException(status_code=400, detail="User already exists")
    service.create(db, user)
    return user


async def update_user(
        user: UserUpdate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    if service.exists(db, user.email, user.username):
        raise HTTPException(status_code=400, detail="User already exists")
    user = service.update(db, current_user.id, user)
    return user



