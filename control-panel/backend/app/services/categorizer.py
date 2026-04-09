"""Auto-categorization of memory chunks."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class MemoryCategorizer:
    """Categorize memory chunks automatically."""

    CATEGORIES = [
        "system",
        "code",
        "data",
        "integration",
        "security",
        "performance",
        "documentation",
    ]

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def categorize(self, content: str) -> dict:
        """Auto-categorize memory chunk.

        Args:
            content: Memory chunk content

        Returns:
            Dict with primary, secondary category, and confidence
        """
        if not content:
            return {
                "primary": "documentation",
                "secondary": "documentation",
                "confidence": 0.0,
            }

        prompt = f"""Categorize this memory chunk.
Categories: {', '.join(self.CATEGORIES)}

Content:
{content[:500]}

Output: {{"primary": "string", "secondary": "string", "confidence": 0-1}}
Only JSON."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.1,
            timeout=1.0,
        )

        if not response:
            return {
                "primary": "documentation",
                "secondary": "documentation",
                "confidence": 0.3,
            }

        try:
            result = json.loads(response)
            primary = result.get("primary", "documentation")
            secondary = result.get("secondary", "documentation")
            confidence = min(1.0, max(0.0, result.get("confidence", 0.5)))

            return {
                "primary": primary if primary in self.CATEGORIES else "documentation",
                "secondary": secondary if secondary in self.CATEGORIES else primary,
                "confidence": confidence,
            }
        except (json.JSONDecodeError, ValueError):
            return {
                "primary": "documentation",
                "secondary": "documentation",
                "confidence": 0.2,
            }
