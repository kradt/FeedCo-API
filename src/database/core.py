from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
