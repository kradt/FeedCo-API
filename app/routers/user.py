from typing import Annotated

from fastapi import APIRouter, Depends, Security, Body
from sqlalchemy.orm import Session

from app import models
from app.dependencies import get_current_user, get_users, get_user, get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import delete_user_by_id, update_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
async def get_all_users(current_user: Annotated[models.User, Security(get_current_user, scopes=["users"])],
                        users: Annotated[models.User, Depends(get_users)]):
    return users


@router.get("/{user_id}", response_model=UserResponse | None)
async def get_user_by_id_in_base(current_user: Annotated[models.User, Security(get_current_user, scopes=["users"])],
                           requested_user: Annotated[models.User, Depends(get_user)]):
    return requested_user


@router.get("/me/", response_model=UserResponse)
async def get_me(current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    return current_user


@router.delete("/me/", status_code=204)
async def delete_account(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    delete_user_by_id(db, current_user.id)


@router.patch("/me/", response_model=UserResponse)
async def update_account(db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])],
                         updated_user: UserUpdate):
    user = update_user_by_id(db, user_id=current_user.id, update_scheme=updated_user)
    print(user)
    return user

