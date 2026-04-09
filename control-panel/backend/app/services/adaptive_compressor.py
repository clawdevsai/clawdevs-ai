"""Adaptive compression strategy based on content type."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class AdaptiveCompressor:
    """Select compression strategy based on content classification."""

    STRATEGIES = {
        "code": 0.85,
        "logs": 0.70,
        "docs": 0.60,
        "metrics": 0.80,
        "errors": 1.0,  # No compression
    }

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def compress_adaptive(self, output: str, tool_name: str = "") -> dict:
        """Classify content and apply appropriate compression.

        Args:
            output: Tool output to compress
            tool_name: Name of tool that generated output

        Returns:
            Dict with compressed output, metrics, and strategy
        """
        if not output:
            return {
                "compressed": "",
                "original_size": 0,
                "compressed_size": 0,
                "ratio": 1.0,
                "strategy": "empty",
            }

        classification = await self._classify_output(output[:1000], tool_name)
        strategy = classification.get("type", "code")
        confidence = classification.get("confidence", 0.5)

        # Apply strategy-based compression (placeholder)
        compression_ratio = self.STRATEGIES.get(strategy, 0.85)
        compressed = output[: int(len(output) * compression_ratio)]

        return {
            "compressed": compressed,
            "original_size": len(output),
            "compressed_size": len(compressed),
            "ratio": len(compressed) / len(output) if output else 1.0,
            "strategy": strategy,
            "confidence": confidence,
        }

    async def _classify_output(self, sample: str, tool_name: str) -> dict:
        """Classify output type using Ollama."""
        prompt = f"""Classify this {tool_name} output as one of: code, logs, docs, metrics, errors

Sample:
{sample}

Output: {{"type": "string", "confidence": 0-1}}
Only JSON, no other text."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.1,
            timeout=1.0,
        )

        if not response:
            return {"type": "code", "confidence": 0.5}

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"type": "code", "confidence": 0.3}
