from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class MemoryEntry(SQLModel, table=True):
    __tablename__ = "memory_entries"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)  # null = global
    type: str = Field(index=True)  # user|feedback|project|reference
    content: str
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSONB))
    is_active: bool = Field(default=True, index=True)
    is_candidate: bool = Field(default=False, index=True)
    file_path: Optional[str] = None  # source file on PVC
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
