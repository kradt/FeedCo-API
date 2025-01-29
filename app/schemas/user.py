from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    password: str
