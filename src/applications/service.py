from sqlalchemy.orm import Session

from src.applications import models
from src.applications.schemas import ApplicationSearch


def get_all(db: Session,
            queryset: ApplicationSearch):
    query = db.query(models.Application).filter_by(deleted=False)
    if queryset.name:
        query = query.filter(models.Application.name.like(f"%{queryset.name}%"))
    if queryset.description:
        query = query.filter(models.Application.description.like(f"%{queryset.description}%"))
    if queryset.user_id:
        query = query.filter_by(user_id=queryset.user_id)
    return query.all()


def get(db: Session, application_id: int):
    return db.query(models.Application).filter_by(id=application_id).first()
