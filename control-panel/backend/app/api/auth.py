from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.auth import verify_password, create_access_token, get_password_hash
from app.core.database import get_session
from app.models import User
from app.api.deps import CurrentUser

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    username: str
    role: str


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    result = await session.exec(select(User).where(User.username == body.username))
    user = result.first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account disabled",
        )
    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser):
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        role=current_user.role,
    )


@router.post("/agent-token", response_model=TokenResponse)
async def create_agent_token(
    current_user: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Gera JWT de 30 dias para uso dos agentes OpenClaw via curl."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    token = create_access_token(
        data={"sub": current_user.username, "type": "agent"},
        expires_delta=timedelta(days=30),
    )
    return TokenResponse(access_token=token)
