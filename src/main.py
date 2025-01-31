from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import config, engine, models
from src.applications import router as applications
from src.users import router as users
from src.auth import router as auth


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
    root_path="/api/v1",
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
app.include_router(users.router)
app.include_router(applications.router)
