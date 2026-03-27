from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import UUID

from app.core.database import get_session
from app.api.deps import CurrentUser
from app.models import MemoryEntry, Agent
from app.services.memory_sync import sync_memory_entries

router = APIRouter()


class MemoryEntryResponse(BaseModel):
    id: str
    agent_id: str | None
    agent_slug: str | None
    entry_type: str
    content: str
    title: str
    body: str
    tags: list[str] | None
    source_agents: list[str] | None
    promoted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class MemoryListResponse(BaseModel):
    items: list[MemoryEntryResponse]
    total: int


@router.get("", response_model=MemoryListResponse)
async def list_memory(
    _: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
    agent_id: Optional[str] = Query(None),
    agent_slug: Optional[str] = Query(None),
    entry_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(30, ge=1, le=100),
):
    # Best-effort sync from OpenClaw files before serving memory.
    await sync_memory_entries(session)

    slug_to_id: dict[str, UUID] = {}
    id_to_slug: dict[UUID, str] = {}
    agents_result = await session.exec(select(Agent))
    for agent in agents_result.all():
        slug_to_id[agent.slug] = agent.id
        id_to_slug[agent.id] = agent.slug

    query = select(MemoryEntry).order_by(MemoryEntry.created_at.desc())
    count_query = select(func.count(MemoryEntry.id))

    if agent_id:
        agent_uuid = UUID(agent_id)
        query = query.where(MemoryEntry.agent_id == agent_uuid)
        count_query = count_query.where(MemoryEntry.agent_id == agent_uuid)
    if agent_slug:
        slug_id = slug_to_id.get(agent_slug)
        if slug_id is None:
            return MemoryListResponse(items=[], total=0)
        query = query.where(MemoryEntry.agent_id == slug_id)
        count_query = count_query.where(MemoryEntry.agent_id == slug_id)
    if entry_type:
        query = query.where(MemoryEntry.entry_type == entry_type)
        count_query = count_query.where(MemoryEntry.entry_type == entry_type)
    if search:
        pattern = f"%{search}%"
        query = query.where(MemoryEntry.content.ilike(pattern))
        count_query = count_query.where(MemoryEntry.content.ilike(pattern))

    total = (await session.exec(count_query)).one() or 0
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await session.exec(query)
    entries = result.all()
    items = [
        MemoryEntryResponse(
            id=str(e.id),
            agent_id=str(e.agent_id) if e.agent_id else None,
            agent_slug=id_to_slug.get(e.agent_id) if e.agent_id else "shared",
            entry_type=e.entry_type,
            content=e.content,
            title=e.tags[0] if e.tags and len(e.tags) > 0 else "Memory entry",
            body=e.content,
            tags=e.tags, source_agents=e.source_agents,
            promoted_at=e.promoted_at, created_at=e.created_at, updated_at=e.updated_at,
        )
        for e in entries
    ]
    return MemoryListResponse(items=items, total=total)


@router.post("/{entry_id}/promote")
async def promote_entry(
    entry_id: str,
    _: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    result = await session.exec(select(MemoryEntry).where(MemoryEntry.id == UUID(entry_id)))
    entry = result.first()
    if entry is None:
        raise HTTPException(status_code=404, detail="Memory entry not found")
    if entry.entry_type != "candidate":
        raise HTTPException(status_code=400, detail="Only candidate entries can be promoted")
    entry.entry_type = "global"
    entry.promoted_at = datetime.now(timezone.utc)
    entry.updated_at = datetime.now(timezone.utc)
    await session.commit()
    return {"status": "promoted", "id": entry_id}
