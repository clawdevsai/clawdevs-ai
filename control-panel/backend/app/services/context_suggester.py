"""Context suggestion for agents."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class ContextSuggester:
    """Suggest relevant memories for agent actions."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def suggest_context(
        self,
        tool_name: str,
        args: str,
        candidate_memories: list[dict],
        top_k: int = 2,
    ) -> dict:
        """Suggest relevant memories for current action.

        Args:
            tool_name: Current tool being executed
            args: Tool arguments
            candidate_memories: List of candidate memory dicts
            top_k: Number of suggestions to return

        Returns:
            Dict with suggestions and confidence
        """
        if not candidate_memories:
            return {
                "suggestions": [],
                "reason": "no_candidates",
                "confidence": 0.0,
            }

        if len(candidate_memories) <= top_k:
            return {
                "suggestions": candidate_memories,
                "reason": "all_candidates",
                "confidence": 0.5,
            }

        ranked = await self._rank_by_relevance(tool_name, args, candidate_memories)

        return {
            "suggestions": ranked[:top_k],
            "reason": "semantic_ranking",
            "confidence": ranked[0].get("relevance_score", 0.5) if ranked else 0.0,
        }

    async def _rank_by_relevance(
        self,
        tool_name: str,
        args: str,
        memories: list[dict],
    ) -> list[dict]:
        """Rank memories by relevance."""
        action = f"{tool_name} {args}"
        memory_list = "\n".join(
            f"{i+1}. {m.get('title', 'Unknown')[:50]}" for i, m in enumerate(memories[:10])
        )

        prompt = f"""Agent running: {action}

Rank these memories by relevance (1-10):
{memory_list}

Output: {{"rankings": [1, 2, 3, ...]}}
Only JSON with numbers."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.2,
            timeout=3.0,
        )

        if not response:
            return memories[:5]

        try:
            data = json.loads(response)
            rankings = data.get("rankings", list(range(1, len(memories) + 1)))

            # Create list with scores
            scored = []
            for i, rank in enumerate(rankings):
                if i < len(memories):
                    memories[i]["relevance_score"] = (11 - rank) / 10.0
                    scored.append(memories[i])

            return sorted(scored, key=lambda x: x.get("relevance_score", 0.5), reverse=True)
        except (json.JSONDecodeError, ValueError):
            return memories[:5]
