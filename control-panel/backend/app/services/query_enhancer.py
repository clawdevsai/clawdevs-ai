"""Query enhancement using Ollama for expanded semantic coverage."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class QueryEnhancer:
    """Expand agent queries with semantic variations."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        """Initialize query enhancer.

        Args:
            ollama_client: Ollama client instance (creates default if None)
        """
        self.ollama_client = ollama_client or OllamaClient()

    async def enhance_query(
        self,
        query: str,
        agent_context: str = "",
        max_expansions: int = 5,
    ) -> dict:
        """Expand query with related search terms.

        Args:
            query: Original search query
            agent_context: Agent description/context
            max_expansions: Max number of expansion terms

        Returns:
            Dict with original, expanded terms, and reasoning
        """
        if not query or len(query) < 2:
            return {
                "original": query,
                "expanded": [],
                "reasoning": "Query too short",
            }

        prompt = f"""Given an agent in context '{agent_context}', expand this search query with {max_expansions} related terms that capture synonyms, related concepts, and edge cases.

Query: "{query}"

Output JSON with:
- original: original query unchanged
- expanded: list of {max_expansions} expansion terms
- reasoning: brief explanation

Be concise. Output ONLY valid JSON."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.3,
            timeout=2.0,
        )

        if not response:
            return {
                "original": query,
                "expanded": [],
                "reasoning": "Ollama timeout/error",
            }

        try:
            result = json.loads(response)
            return {
                "original": result.get("original", query),
                "expanded": result.get("expanded", [])[:max_expansions],
                "reasoning": result.get("reasoning", ""),
            }
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse Ollama response: {response[:100]}")
            return {
                "original": query,
                "expanded": [],
                "reasoning": "Parse error",
            }

    async def health_check(self) -> bool:
        """Check if Ollama is available."""
        return await self.ollama_client.health_check()
