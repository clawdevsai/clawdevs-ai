# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>

"""Integration tests for RAG Retriever Service."""

from __future__ import annotations

from typing import AsyncGenerator, Optional

import pytest
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.memory_entry import MemoryEntry
from app.services.embedding_service import EmbeddingService
from app.services.rag_retriever import RAGRetriever


class FakeEmbeddingService(EmbeddingService):
    async def generate_embedding(self, text: str) -> Optional[list[float]]:
        if not text:
            return None
        return [0.1, 0.2, 0.3]

    def cosine_similarity(
        self, embedding1: list[float], embedding2: list[float]
    ) -> float:
        if not embedding1 or not embedding2:
            return 0.0
        return 0.9 if embedding2[0] <= 0.15 else 0.6

    def chunk_text(
        self, text: str, chunk_size: int = 512, overlap: int = 64
    ) -> list[str]:
        return [
            text[i : i + chunk_size]
            for i in range(0, len(text), max(chunk_size - overlap, 1))
        ]


class NoEmbeddingService(FakeEmbeddingService):
    async def generate_embedding(self, text: str) -> Optional[list[float]]:
        return None


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
async def sample_memories(session: AsyncSession) -> None:
    memories = [
        MemoryEntry(
            title="Authentication Best Practices",
            body="Use JWT tokens with secure expiry.",
            agent_slug="dev_backend",
            entry_type="global",
            tags=["authentication", "security"],
            embedding=[0.1, 0.2, 0.3],
        ),
        MemoryEntry(
            title="Database Migration Pattern",
            body="Use Alembic for migrations.",
            agent_slug="dba_data_engineer",
            entry_type="global",
            tags=["database", "migrations"],
            embedding=[0.2, 0.2, 0.3],
        ),
        MemoryEntry(
            title="API Rate Limiting",
            body="Implement rate limiting.",
            agent_slug="dev_backend",
            entry_type="active",
            tags=["api", "security"],
            embedding=[0.12, 0.2, 0.3],
        ),
    ]

    for memory in memories:
        session.add(memory)
    await session.commit()


class TestRAGRetriever:
    @pytest.mark.asyncio
    async def test_retrieve_similar_solutions(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        results = await retriever.retrieve_similar_solutions(
            query="secure user authentication", top_k=5
        )
        assert len(results) > 0
        assert len(results) <= 5
        assert "similarity_score" in results[0]

    @pytest.mark.asyncio
    async def test_retrieve_for_agent(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        context = await retriever.retrieve_for_agent(
            "dev_backend", "how to authenticate users", top_k=3
        )
        assert isinstance(context, list)
        assert all(isinstance(item, str) for item in context)

    @pytest.mark.asyncio
    async def test_retrieve_by_tags(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        results = await retriever.retrieve_by_tags(tags=["security"], top_k=5)
        assert len(results) > 0

    @pytest.mark.asyncio
    async def test_get_rag_context(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        context = await retriever.get_rag_context(
            agent_slug="dev_backend",
            task_description="implement secure authentication system",
            max_context_items=5,
        )
        assert context["agent_slug"] == "dev_backend"
        assert "similar_solutions" in context

    @pytest.mark.asyncio
    async def test_chunk_text(self, session: AsyncSession) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        chunks = retriever.chunk_text(
            "This is a sentence. " * 100, chunk_size=100, overlap=10
        )
        assert len(chunks) > 1

    @pytest.mark.asyncio
    async def test_invalid_embedding_json(self, session: AsyncSession) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        session.add(
            MemoryEntry(
                title="Corrupted", body="x", embedding_model="mistral", embedding=None
            )
        )
        await session.commit()
        results = await retriever.retrieve_similar_solutions("test", top_k=5)
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_rerank_results(self, session: AsyncSession) -> None:
        retriever = RAGRetriever(session, FakeEmbeddingService())
        initial = [
            {"title": "Authentication", "similarity_score": 0.8},
            {"title": "User Auth System", "similarity_score": 0.75},
        ]
        reranked = await retriever.rerank_results(initial, agent_context="User Auth")
        assert len(reranked) == len(initial)

    @pytest.mark.asyncio
    async def test_fallback_to_lexical_when_embedding_unavailable(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        retriever = RAGRetriever(session, NoEmbeddingService())
        results = await retriever.retrieve_similar_solutions(
            query="database migrations with alembic",
            top_k=5,
            agent_slug="dba_data_engineer",
        )

        assert len(results) > 0
        assert results[0]["retrieval_mode"] == "lexical"
        assert "Database Migration Pattern" in [r["title"] for r in results]

    @pytest.mark.asyncio
    async def test_prioritize_same_session_memories(
        self, session: AsyncSession, sample_memories: None
    ) -> None:
        session.add(
            MemoryEntry(
                title="Session-specific Cache Strategy",
                body="Use Redis write-through cache with session constraints.",
                agent_slug="dev_backend",
                entry_type="active",
                tags=["session:agent:dev_backend:main", "cache"],
                embedding=[0.1, 0.2, 0.3],
            )
        )
        session.add(
            MemoryEntry(
                title="Generic Cache Strategy",
                body="Use Redis write-through cache.",
                agent_slug="dev_backend",
                entry_type="active",
                tags=["cache"],
                embedding=[0.1, 0.2, 0.3],
            )
        )
        await session.commit()

        retriever = RAGRetriever(session, FakeEmbeddingService())
        results = await retriever.retrieve_similar_solutions(
            query="cache strategy",
            top_k=5,
            agent_slug="dev_backend",
            session_key="agent:dev_backend:main",
        )

        assert len(results) > 0
        assert results[0]["title"] == "Session-specific Cache Strategy"
        assert results[0]["retrieval_mode"] == "semantic"
