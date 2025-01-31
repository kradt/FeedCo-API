from typing import Annotated



from fastapi import Depends, Query
from sqlalchemy.orm import Session

from src import models
from src.applications.schemas import ApplicationSearch
from src.dependencies import get_db


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