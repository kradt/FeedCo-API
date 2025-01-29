from typing import Annotated

from fastapi import APIRouter, Depends

from app import models
from app.dependencies import get_current_user

router = APIRouter(prefix="/users")


@router.get("/me/")
async def get_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    pass