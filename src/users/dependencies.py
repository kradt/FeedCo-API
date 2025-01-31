from typing import Annotated

from fastapi import Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_

from src import models, pwd_context
from src.dependencies import get_db
from src.users.schemas import UserSearch, UserCreate
from src.users.service import get_user_by_id


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
