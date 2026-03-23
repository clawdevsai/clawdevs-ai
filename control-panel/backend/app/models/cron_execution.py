from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class CronExecution(SQLModel, table=True):
    __tablename__ = "cron_executions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)
    cron_name: str = Field(index=True)
    status: str  # success|error|running
    started_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    log_output: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
