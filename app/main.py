from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, user, application
from app import config, engine, models

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


tags_metadata = [
    {
        "name": "Auth",
        "description": "Routes for managing user authentication and authorization"
    },
    {
        "name": "Users",
        "description": "Routes for operations with users"
    },
    {
        "name": "Applications",
        "description": "Routes for operations with applications"
    }
]
app = FastAPI(
    lifespan=lifespan,
    title=config.API_NAME,
    contact={
        "name": "Robert Pustota",
        "url": "https://t.me/robertpustota",
        "email": "kradworkmail@gmail.com"
    },
    openapi_tags=tags_metadata,
    openapi_url="/docs/" if config.SHOW_DOCUMENTATION else None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(application.router)
