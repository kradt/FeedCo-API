from sqlalchemy.orm import Session

from app import models


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter_by(id=user_id).first()