from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/users")


@router.get("/me/")
async def get_me(current_user: Annotated[models.User, Security(get_current_user, scopes=["me"])]):
    pass
