from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    API_NAME: str = "FeedCo API"
    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SQLALCHEMY_DATABASE_URI: str
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    SHOW_DOCUMENTATION: bool = False
    model_config = SettingsConfigDict(env_file="../.env", extra="allow")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class ProductionConfig(BaseConfig):
    pass
