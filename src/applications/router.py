from typing import Annotated

from fastapi import APIRouter, Security, Depends

from src import models
from src.auth.dependencies import get_current_user, get_applications
from src.applications.schemas import ApplicationFull

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=list[ApplicationFull])
def get_applications(application: Annotated[list[models.User], Depends(get_applications)],
                     current_user: Annotated[models.User, Security(get_current_user, scopes=["application"])]):
    return application


@router.get("/{application_id}", response_model=ApplicationFull)
def get_application(current_user: Annotated[models.User, Security(get_current_user, scopes=["application"])]):
    pass