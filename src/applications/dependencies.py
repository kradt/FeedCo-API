from typing import Annotated

from fastapi import Depends, HTTPException, Security, Body, Path
from sqlalchemy.orm import Session

from src.applications.schemas import ApplicationBase, ApplicationUpdate
from src.applications import service
from src.dependencies import get_db
from src.users import models as user_models
from src.auth.dependencies import get_current_user


async def get_application_by_id(db: Annotated[Session, Depends(get_db)], application_id: Annotated[int, Path()]):
    application = service.get(db, application_id)
    if not application:
        raise HTTPException(404, detail=f"Application with id {application_id} is not exists")
    return application


async def create_application(db: Annotated[Session, Depends(get_db)],
                       application_data: Annotated[ApplicationBase, Body()],
                       current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    if service.exists(db, application_data.name, application_data.description):
        raise HTTPException(400, detail="Application with this name and description already exists")
    application = service.create(db, application_data, current_user.id)
    return application


async def update_application(
        db: Annotated[Session, Depends(get_db)],
        application_data: Annotated[ApplicationUpdate, Body()],
        application_id: Annotated[int, Path()],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    if service.exists(db, application_data.name, application_data.description):
        raise HTTPException(400, detail="Application with this name and description already exists")
    if not service.get(db, application_id):
        raise HTTPException(404, detail=f"Application with id {application_id} does not exist")
    application = service.update(db, application_data, application_id)
    return application
