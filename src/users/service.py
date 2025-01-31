from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src import models, pwd_context
from src.users.schemas import UserUpdate, UserSearch, UserCreate


def create_user(db: Session, user: UserCreate):
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


def get_users(db: Session, queryset: UserSearch):
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


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter_by(id=user_id).first()


def delete_user_by_id(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    user.deleted = True
    db.add(user)
    db.commit()


def update_user_by_id(db: Session, user_id: int, update_scheme: UserUpdate) -> models.User:
    user = get_user_by_id(db, user_id)
    if update_scheme.username:
        user.username = update_scheme.username
    if update_scheme.email:
        user.email = update_scheme.email
    if update_scheme.description:
        user.description = update_scheme.description
    db.add(user)
    db.commit()
    return user
