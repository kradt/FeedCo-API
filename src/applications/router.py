from typing import Annotated

from fastapi import APIRouter, Security, Depends, Query, Body

from src.applications import models
from src.users import models as user_models
from src.database.core import SessionLocal
from src.applications import service
from src.applications.dependencies import get_application_by_id, create_application, update_application
from src.auth.dependencies import get_current_user
from src.applications.schemas import ApplicationFull, ApplicationSearch, RatingFull, RatingCreate
from src.dependencies import get_db

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=list[ApplicationFull])
def get_applications(
        db: Annotated[SessionLocal, Depends(get_db)],
        search_pattern: Annotated[ApplicationSearch, Query()],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return service.get_all(db, search_pattern)


@router.get("/{application_id}", response_model=ApplicationFull)
def get_application(
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])],
        application: Annotated[models.Application, Depends(get_application_by_id)]):
    return application


@router.post("/", response_model=ApplicationFull)
def create_application(
        application: Annotated[models.Application, Depends(create_application)]):
    return application


@router.post("/{application_id}/rating", response_model=RatingFull)
def create_rating(
        db: Annotated[SessionLocal, Depends(get_db)],
        application: Annotated[models.Application, Depends(get_application_by_id)],
        rating_data: Annotated[RatingCreate, Body()],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return service.rate(db, rating_data, application.id)


@router.patch("/{application_id}", response_model=ApplicationFull)
def update_application(
        application: Annotated[models.Application, Depends(update_application)]):
    return application


@router.patch("/{application_id}", response_model=ApplicationFull)
def update_application(
        application: Annotated[models.Application, Depends(update_application)]):
    return application


@router.delete("/{application_id}", status_code=204)
def delete_application(
        application: Annotated[models.Application, Depends(get_application_by_id)]):
    service.delete(application.id)
