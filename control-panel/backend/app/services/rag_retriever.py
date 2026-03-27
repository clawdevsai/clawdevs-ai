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

"""
RAG (Retrieval-Augmented Generation) Service

Retrieves relevant memories based on semantic similarity and
provides context for agent decision-making.
"""

import logging
import json
from typing import Any, List, Optional, cast

from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.memory_entry import MemoryEntry
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Retrieve relevant memories using semantic search."""

    def __init__(
        self,
        db_session: AsyncSession,
        embedding_service: Optional[EmbeddingService] = None,
    ):
        self.db_session = db_session
        self.embedding_service = embedding_service or EmbeddingService()
        self.min_similarity_threshold = 0.5  # Only return results above this threshold

    async def retrieve_similar_solutions(
        self,
        query: str,
        top_k: int = 5,
        agent_slug: Optional[str] = None,
    ) -> List[dict]:
        """
        Retrieve top-k most similar memory entries for a query.

        Args:
            query: Query text to search for
            top_k: Number of results to return
            agent_slug: Optional - filter to specific agent's memories

        Returns:
            List of relevant memory entries with similarity scores
        """
        # Generate query embedding
        query_embedding = await self.embedding_service.generate_embedding(query)
        if not query_embedding:
            logger.warning(f"Failed to generate embedding for query: {query}")
            return []

        # Fetch all memories with valid embeddings
        statement = select(MemoryEntry).where(
            col(MemoryEntry.embedding).is_not(None),  # Only memories with embeddings
            col(MemoryEntry.entry_type).in_(
                ["active", "global"]
            ),  # Skip archived/candidates
        )

        if agent_slug:
            statement = statement.where(
                (col(MemoryEntry.agent_slug) == agent_slug)
                | (col(MemoryEntry.agent_slug).is_(None))  # Include shared memories
            )

        memories = (await self.db_session.exec(statement)).all()

        if not memories:
            logger.info("No embeddings found for similarity search")
            return []

        # Calculate similarities
        results = []
        for memory in memories:
            # memory.embedding is already a list[float] from pgvector
            embedding = self._normalize_embedding(memory.embedding)
            if not embedding:
                continue

            similarity = self.embedding_service.cosine_similarity(
                query_embedding, embedding
            )

            if similarity >= self.min_similarity_threshold:
                results.append(
                    {
                        "id": str(memory.id),
                        "title": memory.title,
                        "body": memory.body[:500] if memory.body else None,  # Summary
                        "agent_slug": memory.agent_slug,
                        "entry_type": memory.entry_type,
                        "tags": memory.tags,
                        "similarity_score": round(similarity, 3),
                        "chunk_index": memory.chunk_index,
                        "created_at": memory.created_at.isoformat(),
                    }
                )

        # Sort by similarity (highest first) and return top-k
        results.sort(
            key=lambda x: cast(float, x["similarity_score"]),
            reverse=True,
        )
        return results[:top_k]

    async def retrieve_for_agent(
        self,
        agent_slug: str,
        query: str,
        top_k: int = 3,
    ) -> List[str]:
        """
        Retrieve relevant context for an agent to use in decision-making.

        Args:
            agent_slug: Agent requesting the memory
            query: Query/context for retrieval
            top_k: Number of results to return

        Returns:
            List of relevant memory bodies formatted for agent context
        """
        results = await self.retrieve_similar_solutions(
            query,
            top_k=top_k,
            agent_slug=agent_slug,
        )

        context_items = []
        for result in results:
            if result["body"]:
                context_items.append(
                    f"[{result['title']} (similarity: {result['similarity_score']})] "
                    f"{result['body']}"
                )

        return context_items

    async def retrieve_by_tags(
        self,
        tags: List[str],
        top_k: int = 5,
    ) -> List[dict]:
        """
        Retrieve memories by tags.

        Args:
            tags: List of tags to search for
            top_k: Number of results to return

        Returns:
            List of memory entries with matching tags
        """
        # This requires PostgreSQL ARRAY operations
        # Using basic filtering for now
        statement = select(MemoryEntry).where(
            col(MemoryEntry.embedding).is_not(None),
            col(MemoryEntry.entry_type).in_(["active", "global"]),
        )

        memories = (await self.db_session.exec(statement)).all()

        results = []
        for memory in memories:
            if memory.tags and any(tag in memory.tags for tag in tags):
                results.append(
                    {
                        "id": str(memory.id),
                        "title": memory.title,
                        "body": memory.body[:500] if memory.body else None,
                        "agent_slug": memory.agent_slug,
                        "tags": memory.tags,
                        "created_at": memory.created_at.isoformat(),
                    }
                )

        return results[:top_k]

    async def get_rag_context(
        self,
        agent_slug: str,
        task_description: str,
        max_context_items: int = 5,
    ) -> dict:
        """
        Get comprehensive RAG context for task execution.

        Combines:
        - Most similar solutions (semantic search)
        - Relevant patterns (tag-based)
        - Agent-specific memories

        Args:
            agent_slug: Agent requesting context
            task_description: Task to get context for
            max_context_items: Max items to return

        Returns:
            Comprehensive context dict for agent use
        """
        # Semantic search
        similar = await self.retrieve_for_agent(
            agent_slug,
            task_description,
            top_k=max_context_items,
        )

        # Extract tags from task for tag-based retrieval
        tags = self._extract_tags_from_task(task_description)
        tagged_results = await self.retrieve_by_tags(tags, top_k=3)

        return {
            "agent_slug": agent_slug,
            "query": task_description,
            "similar_solutions": similar,
            "tagged_patterns": [r["title"] for r in tagged_results],
            "total_context_items": len(similar) + len(tagged_results),
            "recommendation": (
                "Use retrieved context as reference. "
                "Similar solutions may guide implementation approach."
                if similar
                else "No relevant memories found. Proceed with fresh approach."
            ),
        }

    def _extract_tags_from_task(self, task_description: str) -> List[str]:
        """
        Extract potential tags from task description.

        Simple keyword-based extraction.
        """
        keywords = [
            "authentication",
            "database",
            "api",
            "frontend",
            "backend",
            "testing",
            "deployment",
            "security",
            "performance",
            "bugfix",
            "feature",
        ]

        task_lower = task_description.lower()
        found_tags = [kw for kw in keywords if kw in task_lower]

        return found_tags

    def chunk_text(
        self, text: str, chunk_size: int = 512, overlap: int = 64
    ) -> List[str]:
        """Compatibility wrapper around embedding chunking."""
        return self.embedding_service.chunk_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

    def _normalize_embedding(self, value: Any) -> Optional[List[float]]:
        """Accept list embeddings and tolerate JSON-string legacy test fixtures."""
        if value is None:
            return None
        if isinstance(value, list):
            return [float(v) for v in value]
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return [float(v) for v in parsed]
            except (TypeError, ValueError, json.JSONDecodeError):
                return None
        return None

    async def rerank_results(
        self,
        results: List[dict],
        agent_context: Optional[str] = None,
    ) -> List[dict]:
        """
        Re-rank results based on additional context.

        Args:
            results: Initial retrieval results
            agent_context: Additional agent context for reranking

        Returns:
            Re-ranked results
        """
        # Basic reranking: boost exact title matches
        if agent_context:
            for result in results:
                if agent_context.lower() in result.get("title", "").lower():
                    result["similarity_score"] += 0.2  # Boost score

        # Re-sort
        results.sort(
            key=lambda x: cast(float, x["similarity_score"]),
            reverse=True,
        )
        return results
