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
import re
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
        session_key: Optional[str] = None,
    ) -> List[dict]:
        """
        Retrieve top-k most similar memory entries for a query.

        Args:
            query: Query text to search for
            top_k: Number of results to return
            agent_slug: Optional - filter to specific agent's memories
            session_key: Optional - prioritize memories from same session

        Returns:
            List of relevant memory entries with similarity scores
        """
        semantic_results: List[dict] = []
        query_embedding = await self.embedding_service.generate_embedding(query)
        if query_embedding:
            semantic_results = await self._retrieve_semantic_results(
                query_embedding=query_embedding,
                top_k=top_k,
                agent_slug=agent_slug,
                session_key=session_key,
            )
        else:
            logger.warning(
                "Failed to generate embedding for query, falling back to lexical search: %s",
                query,
            )

        if len(semantic_results) >= top_k:
            return semantic_results[:top_k]

        lexical_results = await self._retrieve_lexical_results(
            query=query,
            top_k=top_k,
            agent_slug=agent_slug,
            session_key=session_key,
        )
        if not semantic_results:
            return lexical_results[:top_k]

        combined: List[dict] = []
        seen_ids: set[str] = set()
        for item in semantic_results + lexical_results:
            item_id = cast(str, item.get("id"))
            if item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            combined.append(item)

        combined.sort(
            key=lambda x: cast(float, x["similarity_score"]),
            reverse=True,
        )
        return combined[:top_k]

    async def retrieve_for_agent(
        self,
        agent_slug: str,
        query: str,
        top_k: int = 3,
        session_key: Optional[str] = None,
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
            session_key=session_key,
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
        session_key: Optional[str] = None,
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
            session_key=session_key,
        )

        # Extract tags from task for tag-based retrieval
        tags = self._extract_tags_from_task(task_description)
        tagged_results = await self.retrieve_by_tags(tags, top_k=3)

        return {
            "agent_slug": agent_slug,
            "query": task_description,
            "session_key": session_key,
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

    async def _retrieve_semantic_results(
        self,
        query_embedding: List[float],
        top_k: int,
        agent_slug: Optional[str],
        session_key: Optional[str],
    ) -> List[dict]:
        statement = self._base_memory_statement(require_embeddings=True)
        if agent_slug:
            statement = statement.where(
                (col(MemoryEntry.agent_slug) == agent_slug)
                | (col(MemoryEntry.agent_slug).is_(None))
            )

        memories = (await self.db_session.exec(statement)).all()
        if not memories:
            logger.info("No embeddings found for semantic similarity search")
            return []

        results: List[dict] = []
        for memory in memories:
            embedding = self._normalize_embedding(memory.embedding)
            if not embedding:
                continue

            similarity = self.embedding_service.cosine_similarity(
                query_embedding, embedding
            )
            if similarity < self.min_similarity_threshold:
                continue

            score = similarity
            score += self._session_boost(memory.tags, session_key)
            score += self._agent_boost(memory.agent_slug, agent_slug)

            results.append(
                self._serialize_result(
                    memory=memory,
                    score=score,
                    retrieval_mode="semantic",
                )
            )

        results.sort(
            key=lambda x: cast(float, x["similarity_score"]),
            reverse=True,
        )
        return results[:top_k]

    async def _retrieve_lexical_results(
        self,
        query: str,
        top_k: int,
        agent_slug: Optional[str],
        session_key: Optional[str],
    ) -> List[dict]:
        statement = self._base_memory_statement(require_embeddings=False)
        if agent_slug:
            statement = statement.where(
                (col(MemoryEntry.agent_slug) == agent_slug)
                | (col(MemoryEntry.agent_slug).is_(None))
            )

        memories = (await self.db_session.exec(statement)).all()
        if not memories:
            return []

        query_tokens = self._tokenize_query(query)
        query_lower = query.strip().lower()
        results: List[dict] = []

        for memory in memories:
            title_text = (memory.title or "").lower()
            body_text = (memory.body or "").lower()
            full_text = f"{title_text}\n{body_text}"

            lexical_hits = self._lexical_hits(query_tokens, title_text, body_text)
            if query_lower and query_lower in full_text:
                lexical_hits += 2

            if lexical_hits <= 0:
                continue

            score = 0.2 + min(lexical_hits * 0.03, 0.35)
            score += self._session_boost(memory.tags, session_key)
            score += self._agent_boost(memory.agent_slug, agent_slug)
            score = min(score, 0.95)

            results.append(
                self._serialize_result(
                    memory=memory,
                    score=score,
                    retrieval_mode="lexical",
                )
            )

        results.sort(
            key=lambda x: cast(float, x["similarity_score"]),
            reverse=True,
        )
        return results[:top_k]

    def _base_memory_statement(self, require_embeddings: bool):
        statement = select(MemoryEntry).where(
            col(MemoryEntry.entry_type).in_(["active", "global"])
        )
        if require_embeddings:
            statement = statement.where(col(MemoryEntry.embedding).is_not(None))
        return statement

    def _serialize_result(
        self,
        memory: MemoryEntry,
        score: float,
        retrieval_mode: str,
    ) -> dict:
        return {
            "id": str(memory.id),
            "title": memory.title,
            "body": memory.body[:500] if memory.body else None,
            "agent_slug": memory.agent_slug,
            "entry_type": memory.entry_type,
            "tags": memory.tags,
            "similarity_score": round(score, 3),
            "chunk_index": memory.chunk_index,
            "created_at": memory.created_at.isoformat(),
            "retrieval_mode": retrieval_mode,
        }

    def _session_boost(
        self,
        tags: Optional[List[str]],
        session_key: Optional[str],
    ) -> float:
        if not session_key or not tags:
            return 0.0
        target_tag = f"session:{session_key}"
        return 0.08 if target_tag in tags else 0.0

    def _agent_boost(
        self,
        memory_agent_slug: Optional[str],
        requested_agent_slug: Optional[str],
    ) -> float:
        if not requested_agent_slug or not memory_agent_slug:
            return 0.0
        return 0.04 if memory_agent_slug == requested_agent_slug else 0.0

    def _tokenize_query(self, query: str) -> List[str]:
        return [token for token in re.findall(r"\w+", query.lower()) if len(token) >= 3]

    def _lexical_hits(
        self,
        query_tokens: List[str],
        title_text: str,
        body_text: str,
    ) -> int:
        if not query_tokens:
            return 0
        score = 0
        for token in query_tokens:
            score += title_text.count(token) * 2
            score += body_text.count(token)
        return score

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
