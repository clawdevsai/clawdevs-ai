from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)
    openclaw_session_id: str = Field(unique=True, index=True)
    channel: Optional[str] = None  # webchat|telegram|etc
    peer: Optional[str] = None
    message_count: int = Field(default=0)
    token_count: int = Field(default=0)
    status: str = Field(default="active")  # active|closed
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
