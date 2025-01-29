from pydantic import BaseModel, constr, EmailStr

from app.models import AccountType


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    account_type: AccountType


class UserResponse(BaseUser):
    description: constr(max_length=200) | None = None


class UserCreate(BaseUser):
    password: str


class UserSearch(UserResponse):
    username: str | None = None
    email: str | None = None
    account_type: AccountType | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    description: constr(max_length=200) | None = None

