from sqlalchemy.orm import Session

from app import models
from app.schemas.user import UserUpdate


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
