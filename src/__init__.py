import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.settings import DevelopmentConfig, ProductionConfig, BaseConfig

load_dotenv()
config_mode = os.getenv("CONFIG_MODE", "PRODUCTION")

if config_mode == "PRODUCTION":
    config = ProductionConfig()
elif config_mode == "DEVELOPMENT":
    config = DevelopmentConfig()
else:
    config = BaseConfig()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

scopes = {
    "me": "Get info about current user",
    "users": "Get info about users",
    "manage-applications": "Create new Applications and manage them",
    "test-applications": "Get info about applications, write reviews and comments"
}
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scopes=scopes)
