from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from uuid import UUID

from app.core.database import get_session
from app.api.deps import CurrentUser
from app.models import Metric, Approval, Task, Agent

router = APIRouter()


class OverviewMetrics(BaseModel):
    active_agents: int
    pending_approvals: int
    open_tasks: int
    tokens_24h: float


class MetricResponse(BaseModel):
    metric_type: str
    value: float
    period_start: datetime
    period_end: datetime | None
    agent_id: str | None


class MetricsListResponse(BaseModel):
    items: list[MetricResponse]
    total: int


@router.get("", response_model=MetricsListResponse)
async def list_metrics(
    _: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
    metric_type: Optional[str] = Query(None),
    days: int = Query(7, ge=1, le=90),
    agent_id: Optional[str] = Query(None),
):
    since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)

    query = select(Metric).where(Metric.period_start >= since).order_by(Metric.period_start.asc())
    if metric_type:
        query = query.where(Metric.metric_type == metric_type)
    if agent_id:
        query = query.where(Metric.agent_id == UUID(agent_id))

    result = await session.exec(query)
    metrics = result.all()
    items = [
        MetricResponse(
            metric_type=m.metric_type,
            value=m.value,
            period_start=m.period_start,
            period_end=m.period_end,
            agent_id=str(m.agent_id) if m.agent_id else None,
        )
        for m in metrics
    ]
    return MetricsListResponse(items=items, total=len(items))


@router.get("/overview", response_model=OverviewMetrics)
async def overview_metrics(
    _: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    since = datetime.now(timezone.utc) - timedelta(hours=24)

    agents_result = await session.exec(
        select(Agent).where(Agent.status.in_(["online", "working"]))
    )
    active_agents = len(agents_result.all())

    approvals_result = await session.exec(
        select(Approval).where(Approval.status == "pending")
    )
    pending_approvals = len(approvals_result.all())

    tasks_result = await session.exec(
        select(Task).where(Task.status.in_(["inbox", "in_progress", "review"]))
    )
    open_tasks = len(tasks_result.all())

    metrics_result = await session.exec(
        select(Metric).where(
            Metric.metric_type == "tokens_used",
            Metric.period_start >= since,
        )
    )
    tokens_24h = sum(m.value for m in metrics_result.all())

    return OverviewMetrics(
        active_agents=active_agents,
        pending_approvals=pending_approvals,
        open_tasks=open_tasks,
        tokens_24h=tokens_24h,
    )
