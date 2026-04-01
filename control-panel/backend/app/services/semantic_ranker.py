"""Semantic reranking of search results using Ollama."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class SemanticRanker:
    """Rerank search results by semantic relevance."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def rerank(
        self,
        query: str,
        chunks: list[str],
        bm25_scores: list[float],
        top_k: int = 5,
    ) -> list[tuple[str, float]]:
        """Rerank chunks using semantic relevance scoring.

        Args:
            query: Search query
            chunks: Content chunks to rank
            bm25_scores: Original BM25 scores
            top_k: Return top K results

        Returns:
            List of (chunk, combined_score) tuples sorted by score descending
        """
        if not chunks or not query:
            return []

        semantic_scores = []

        # Batch process in groups of 4
        batch_size = 4
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            chunk_list = "\n".join(f"{j+1}. {c[:200]}" for j, c in enumerate(batch))
            prompt = f"""Query: "{query}"

Rate relevance of each chunk (1-10 scale):
{chunk_list}

Output JSON: {{"ratings": [1, 2, 3, ...]}}  Only numbers."""

            response = await self.ollama_client.generate(
                prompt=prompt,
                temperature=0.2,
                timeout=3.0,
            )

            if response:
                try:
                    data = json.loads(response)
                    ratings = data.get("ratings", [])
                    semantic_scores.extend([r / 10.0 for r in ratings[:len(batch)]])
                except (json.JSONDecodeError, ValueError):
                    semantic_scores.extend([0.5] * len(batch))
            else:
                semantic_scores.extend([0.5] * len(batch))

        # Combine scores: semantic 70%, BM25 30%
        combined = []
        for chunk, bm25, semantic in zip(chunks, bm25_scores, semantic_scores):
            score = semantic * 0.7 + (bm25 / 100.0) * 0.3
            combined.append((chunk, score))

        return sorted(combined, key=lambda x: x[1], reverse=True)[:top_k]
