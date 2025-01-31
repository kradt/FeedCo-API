from typing import Annotated

from fastapi import APIRouter, Depends, Security, Query, Path
from sqlalchemy.orm import Session

from src import models, SessionLocal
from src.applications.schemas import ApplicationFull
from src.users.dependencies import get_user_by_id, get_db, create_user
from src.auth.dependencies import get_current_user
from src.users.schemas import UserFull, UserUpdate, BaseUser, UserSearch
from src.users import service
from src.applications import service as application_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create-user/", response_model=BaseUser)
async def create_user(user: Annotated[models.User, Depends(create_user)]):
    """
    Registrate user or raise and error if user already exists
    :param user: created user from base
    :return: json with user data
    """
    return user


@router.get("/", response_model=list[UserFull])
async def get_all_users(current_user: Annotated[models.User, Security(get_current_user, scopes=["users"])],
                        db: Annotated[SessionLocal, Depends(get_db)],
                        search_pattern: Annotated[Query, UserSearch]):
    return service.get_all(db, search_pattern)


@router.get("/{user_id}", response_model=UserFull | None)
async def get_user(current_user: Annotated[models.User, Security(get_current_user, scopes=["users"])],
                   requested_user: Annotated[models.User, Depends(get_user_by_id)]):
    return requested_user


@router.get("/{user_id}/applications/")
async def get_applications_of_specific_user(db: Annotated[SessionLocal, Depends(get_db)],
                                      current_user: Annotated[models.User, Security(get_current_user, scopes=["users", "applications"])],
                                      user_id: Annotated[int, Path()]):
    return application_service.get_all_by_user(db, user_id)


@router.get("/me/applications/", response_model=list[ApplicationFull])
async def get_applications_of_current_user(db: Annotated[SessionLocal, Depends(get_db)],
                                     current_user: Annotated[models.User, Security(get_current_user, scopes=["users", "applications"])]):
    return application_service.get_all_by_user(db, current_user.id)


@router.get("/me/", response_model=UserFull)
async def get_me(current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    return current_user


@router.delete("/me/", status_code=204)
async def delete_user(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    service.delete(db, current_user.id)


@router.patch("/me/", response_model=UserFull)
async def update_user(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])],
                         updated_user: UserUpdate):
    return service.update(db, user_id=current_user.id, update_scheme=updated_user)
