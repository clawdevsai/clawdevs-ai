# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta
from uuid import UUID

from app.core.database import get_session
from app.api.deps import CurrentUser
from app.models import Metric, Approval, Task, Agent, Session

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

    # Fallback for dashboard usage chart: derive sessions/day straight from sessions table.
    if metric_type == "sessions":
        day_start = since.replace(hour=0, minute=0, second=0, microsecond=0)
        day_bucket = func.date_trunc("day", Session.created_at)
        query = (
            select(day_bucket, func.count(Session.id))
            .where(Session.created_at >= day_start)
            .group_by(day_bucket)
            .order_by(day_bucket.asc())
        )
        rows = (await session.exec(query)).all()
        count_by_day: dict[datetime, float] = {}
        for bucket, count in rows:
            if bucket is None:
                continue
            count_by_day[bucket.replace(tzinfo=None)] = float(count)

        start_day = day_start
        today = datetime.now(timezone.utc).replace(tzinfo=None).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        items: list[MetricResponse] = []
        cursor = start_day
        while cursor <= today:
            items.append(
                MetricResponse(
                    metric_type="sessions",
                    value=count_by_day.get(cursor, 0.0),
                    period_start=cursor,
                    period_end=cursor + timedelta(days=1),
                    agent_id=None,
                )
            )
            cursor = cursor + timedelta(days=1)

        return MetricsListResponse(items=items, total=len(items))

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
