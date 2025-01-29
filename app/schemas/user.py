from dataclasses import Field

from pydantic import BaseModel, constr

from app.models import AccountType


class BaseUser(BaseModel):
    username: str
    email: str
    account_type: AccountType


class UserResponse(BaseUser):
    description: constr(max_length=200)


class UserCreate(BaseUser):
    password: str
