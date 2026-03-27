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

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_session
from app.api.deps import CurrentUser
from app.models import Agent, CronExecution

router = APIRouter()


class CronStatusResponse(BaseModel):
    agent_id: str
    agent_slug: str
    display_name: str
    cron_expression: str | None
    cron_status: str
    cron_last_run_at: datetime | None
    cron_next_run_at: datetime | None
    last_exit_code: int | None
    recent_executions: list[dict]


@router.get("", response_model=list[CronStatusResponse])
async def list_cron_statuses(
    _: CurrentUser,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    result = await session.exec(
        select(Agent).where(Agent.cron_expression != None).order_by(Agent.slug)
    )
    agents = result.all()

    statuses = []
    for agent in agents:
        exec_result = await session.exec(
            select(CronExecution)
            .where(CronExecution.agent_id == agent.id)
            .order_by(CronExecution.started_at.desc())
            .limit(10)
        )
        executions = exec_result.all()
        last_exit = executions[0].exit_code if executions else None

        statuses.append(CronStatusResponse(
            agent_id=str(agent.id),
            agent_slug=agent.slug,
            display_name=agent.display_name,
            cron_expression=agent.cron_expression,
            cron_status=agent.cron_status,
            cron_last_run_at=agent.cron_last_run_at,
            cron_next_run_at=agent.cron_next_run_at,
            last_exit_code=last_exit,
            recent_executions=[
                {
                    "id": str(e.id),
                    "started_at": e.started_at.isoformat(),
                    "finished_at": e.finished_at.isoformat() if e.finished_at else None,
                    "exit_code": e.exit_code,
                    "trigger_type": e.trigger_type,
                }
                for e in executions
            ],
        ))
    return statuses
