# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

"""Unit tests for Failure Detection Service."""

from datetime import timedelta
from typing import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models.agent import Agent
from app.models.task import Task
from app.services.failure_detector import FailureDetector


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    SessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with SessionLocal() as session:
        yield session


@pytest.fixture
async def sample_agents(session: AsyncSession) -> dict[str, Agent]:
    arquiteto = Agent(
        slug="arquiteto",
        display_name="Arquiteto",
        role="Senior Architect",
        can_escalate=True,
        max_escalations=10,
    )
    dev_backend = Agent(
        slug="dev_backend",
        display_name="Dev Backend",
        role="Backend Developer",
        can_escalate=False,
    )
    session.add(arquiteto)
    session.add(dev_backend)
    await session.commit()
    return {"arquiteto": arquiteto, "dev_backend": dev_backend}


@pytest.fixture
async def sample_task(session: AsyncSession) -> Task:
    task = Task(
        title="Test Task",
        description="A task for testing",
        status="in_progress",
        label="back_end",
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


class TestFailureDetector:
    @pytest.mark.asyncio
    async def test_record_single_failure(
        self, session: AsyncSession, sample_task: Task
    ) -> None:
        detector = FailureDetector(session)
        await detector.record_failure(
            sample_task.id, "Connection timeout", "network_error"
        )
        await session.refresh(sample_task)
        assert sample_task.failure_count == 1
        assert sample_task.consecutive_failures == 1
        assert sample_task.last_error == "Connection timeout"
        assert sample_task.error_reason == "network_error"

    @pytest.mark.asyncio
    async def test_escalation_on_threshold(
        self,
        session: AsyncSession,
        sample_task: Task,
        sample_agents: dict[str, Agent],
    ) -> None:
        detector = FailureDetector(session)
        for i in range(3):
            await detector.record_failure(
                sample_task.id, f"Error {i+1}", "execution_error"
            )
        await session.refresh(sample_task)
        assert sample_task.consecutive_failures == 3
        assert sample_task.escalated_to_agent_id == sample_agents["arquiteto"].id

    @pytest.mark.asyncio
    async def test_reset_consecutive_failures(
        self, session: AsyncSession, sample_task: Task
    ) -> None:
        detector = FailureDetector(session)
        await detector.record_failure(sample_task.id, "Error", "execution_error")
        await detector.record_failure(sample_task.id, "Error", "execution_error")
        await session.refresh(sample_task)
        assert sample_task.consecutive_failures == 2
        await detector.reset_consecutive_failures(sample_task.id)
        await session.refresh(sample_task)
        assert sample_task.consecutive_failures == 0

    @pytest.mark.asyncio
    async def test_exponential_backoff(self, session: AsyncSession) -> None:
        detector = FailureDetector(session)
        delay1 = await detector.apply_exponential_backoff(uuid4(), 1)
        delay2 = await detector.apply_exponential_backoff(uuid4(), 2)
        delay3 = await detector.apply_exponential_backoff(uuid4(), 3)
        assert delay1 == timedelta(seconds=1)
        assert delay2 == timedelta(seconds=1)
        assert delay3.total_seconds() > delay2.total_seconds()

    @pytest.mark.asyncio
    async def test_get_task_health(
        self, session: AsyncSession, sample_task: Task
    ) -> None:
        detector = FailureDetector(session)
        healthy = await detector.get_task_health(sample_task.id)
        assert healthy["status"] == "healthy"
        await detector.record_failure(sample_task.id, "Error", "execution_error")
        unhealthy = await detector.get_task_health(sample_task.id)
        assert unhealthy["status"] == "unhealthy"

    @pytest.mark.asyncio
    async def test_non_existent_task(self, session: AsyncSession) -> None:
        detector = FailureDetector(session)
        non_existent_id = uuid4()
        await detector.record_failure(non_existent_id, "Error", "execution_error")
        health = await detector.get_task_health(non_existent_id)
        assert health["status"] == "unknown"
