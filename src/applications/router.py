from typing import Annotated

from fastapi import APIRouter, Security, Depends, Query

from src.applications import models
from src.users import models as user_models
from src.database.core import SessionLocal
from src.applications import service
from src.applications.dependencies import get_application_by_id
from src.auth.dependencies import get_current_user
from src.applications.schemas import ApplicationFull, ApplicationSearch
from src.dependencies import get_db

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/", response_model=list[ApplicationFull])
def get_applications(db: Annotated[SessionLocal, Depends(get_db)],
                     search_pattern: Annotated[ApplicationSearch, Query()],
                     current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return service.get_all(db, search_pattern)


@router.get("/{application_id}", response_model=ApplicationFull)
def get_application(current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])],
                    application: Annotated[models.Application, Depends(get_application_by_id)]):
    return application