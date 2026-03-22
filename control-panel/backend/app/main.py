from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.core.auth import get_password_hash
from app.models import User
from app.api import auth as auth_api

settings = get_settings()


async def bootstrap_admin():
    """Create admin user on first startup if not exists."""
    async with AsyncSessionLocal() as session:
        result = await session.exec(
            select(User).where(User.username == settings.admin_username)
        )
        if result.first() is None:
            admin = User(
                username=settings.admin_username,
                password_hash=get_password_hash(settings.admin_password),
                role="admin",
            )
            session.add(admin)
            await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bootstrap_admin()
    yield


app = FastAPI(
    title="ClawDevs Panel API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://clawdevs-panel-frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)

# Routers
app.include_router(auth_api.router, prefix="/auth", tags=["auth"])


@app.get("/healthz", tags=["health"])
async def health():
    return {"status": "ok"}
