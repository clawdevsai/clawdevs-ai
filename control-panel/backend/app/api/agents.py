from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
import httpx

from app.core.database import get_session
from app.core.config import get_settings
from app.models import Agent
from app.api.deps import get_current_user

router = APIRouter()
settings = get_settings()


class AgentResponse(BaseModel):
    id: str
    slug: str
    display_name: str
    role: str
    avatar_url: Optional[str]
    status: str
    current_model: Optional[str]
    last_heartbeat_at: Optional[datetime]
    cron_expression: Optional[str]
    cron_last_run_at: Optional[datetime]
    cron_next_run_at: Optional[datetime]
    cron_status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_agent(cls, agent: Agent) -> "AgentResponse":
        return cls(
            id=str(agent.id),
            slug=agent.slug,
            display_name=agent.display_name,
            role=agent.role,
            avatar_url=agent.avatar_url,
            status=agent.status,
            current_model=agent.current_model,
            last_heartbeat_at=agent.last_heartbeat_at,
            cron_expression=agent.cron_expression,
            cron_last_run_at=agent.cron_last_run_at,
            cron_next_run_at=agent.cron_next_run_at,
            cron_status=agent.cron_status,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )


@router.get("", response_model=Page[AgentResponse])
async def list_agents(
    session: AsyncSession = Depends(get_session),
    _=Depends(get_current_user),
):
    query = select(Agent).order_by(Agent.slug)
    result = await paginate(session, query)
    # Convert Agent objects to AgentResponse
    result.items = [AgentResponse.from_agent(a) for a in result.items]
    return result


@router.get("/{slug}", response_model=AgentResponse)
async def get_agent(
    slug: str,
    session: AsyncSession = Depends(get_session),
    _=Depends(get_current_user),
):
    result = await session.exec(select(Agent).where(Agent.slug == slug))
    agent = result.first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{slug}' não encontrado")
    return AgentResponse.from_agent(agent)


@router.post("/{slug}/restart", status_code=status.HTTP_204_NO_CONTENT)
async def restart_agent(
    slug: str,
    session: AsyncSession = Depends(get_session),
    _=Depends(get_current_user),
):
    result = await session.exec(select(Agent).where(Agent.slug == slug))
    agent = result.first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{slug}' não encontrado")

    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{settings.openclaw_gateway_url}/v1/agents/{slug}/restart",
                headers={"Authorization": f"Bearer {settings.openclaw_gateway_token}"},
                timeout=10.0,
            )
            r.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Erro ao reiniciar agente: {e}")


@router.post("/{slug}/cron/trigger", status_code=status.HTTP_204_NO_CONTENT)
async def trigger_cron(
    slug: str,
    session: AsyncSession = Depends(get_session),
    _=Depends(get_current_user),
):
    result = await session.exec(select(Agent).where(Agent.slug == slug))
    agent = result.first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{slug}' não encontrado")

    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{settings.openclaw_gateway_url}/v1/agents/{slug}/cron/trigger",
                headers={"Authorization": f"Bearer {settings.openclaw_gateway_token}"},
                timeout=10.0,
            )
            r.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Erro ao disparar cron: {e}")
