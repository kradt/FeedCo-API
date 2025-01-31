from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.users.schemas import UserSearch, UserCreate
from src.users import service


async def get_user_by_id(db: Annotated[Session, Depends(get_db)], user_id: Annotated[str, Path()]):
    user = service.get(db, user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {user_id} is not found")
    return user


async def create_user(user: UserCreate,
                db: Annotated[Session, Depends(get_db)]):
    """
    Create user and save it to base
    :param db: session to interact with db
    :param user: scheme with user data like password and username
    :return: user from base
    """
    if service.get_all(db, UserSearch(email=user.email, username=user.username)):
       raise HTTPException(status_code=400, detail="User already exists")
    service.create(db, user)
    return user
