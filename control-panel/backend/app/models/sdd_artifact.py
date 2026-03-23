from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class SddArtifact(SQLModel, table=True):
    __tablename__ = "sdd_artifacts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    current_step: str = Field(default="brief")  # brief|clarify|spec|plan|task|validate
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id", index=True)
    brief: Optional[str] = None
    clarify: Optional[str] = None
    spec: Optional[str] = None
    plan: Optional[str] = None
    task_doc: Optional[str] = None
    validate_doc: Optional[str] = None
    github_issue_number: Optional[int] = None
    github_issue_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
