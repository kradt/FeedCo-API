import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.settings import DevelopmentConfig, ProductionConfig, BaseConfig

load_dotenv()
config_mode = os.getenv("CONFIG_MODE", "PRODUCTION")

if config_mode == "PRODUCTION":
    config = ProductionConfig()
elif config_mode == "DEVELOPMENT":
    config = DevelopmentConfig()
else:
    config = BaseConfig()


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

scopes = {
    "me": "Get info about current user",
    "users": "Get info about users"
}
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scopes=scopes)
