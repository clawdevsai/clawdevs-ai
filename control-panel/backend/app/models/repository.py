from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class Repository(SQLModel, table=True):
    __tablename__ = "repositories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    full_name: str = Field(unique=True, index=True)  # org/repo
    description: Optional[str] = None
    default_branch: str = Field(default="main")
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
