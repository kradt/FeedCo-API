from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.applications import service
from src.dependencies import get_db


def get_application_by_id(db: Annotated[Session, Depends(get_db)], application_id: int):
    application = service.get(db, application_id)
    if not application:
        raise HTTPException(404, detail=f"Application with id {application_id} is not exists")
    return application