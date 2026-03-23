from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class Metric(SQLModel, table=True):
    __tablename__ = "metrics"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)
    period: str = Field(index=True)  # 1h|24h|7d
    token_count: int = Field(default=0)
    task_count: int = Field(default=0)
    approval_count: int = Field(default=0)
    error_count: int = Field(default=0)
    recorded_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
