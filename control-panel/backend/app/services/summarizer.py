"""Intelligent summarization of memory chunks."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class IntelligentSummarizer:
    """Summarize content while preserving critical information."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def summarize(
        self,
        content: str,
        intent: Optional[str] = None,
        max_words: int = 100,
    ) -> dict:
        """Summarize content intelligently.

        Args:
            content: Content to summarize
            intent: Agent intent/context
            max_words: Maximum summary length

        Returns:
            Dict with summary and key_points
        """
        if not content or len(content) < 50:
            return {
                "summary": content,
                "key_points": [],
                "compression_ratio": 1.0,
            }

        prompt = f"""Summarize in {max_words} words. Keep: numbers, errors, solutions, warnings.
Remove: verbose explanations, examples.
{f'Context: {intent}' if intent else ''}

Content:
{content}

Output: {{"summary": "...", "key_points": [...]}}
Only JSON."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.3,
            timeout=2.5,
        )

        if not response:
            return {
                "summary": content[:200],
                "key_points": [],
                "compression_ratio": 0.2,
            }

        try:
            result = json.loads(response)
            summary = result.get("summary", content[:200])
            return {
                "summary": summary,
                "key_points": result.get("key_points", []),
                "compression_ratio": len(summary) / len(content) if content else 1.0,
            }
        except json.JSONDecodeError:
            return {
                "summary": content[:200],
                "key_points": [],
                "compression_ratio": 0.2,
            }
