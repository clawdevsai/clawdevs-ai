"""Anomaly detection in tool outputs."""
import json
import logging
from typing import Optional
from app.services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """Detect anomalies in tool outputs."""

    def __init__(self, ollama_client: Optional[OllamaClient] = None):
        self.ollama_client = ollama_client or OllamaClient()

    async def detect(
        self,
        output: str,
        tool_name: str = "",
        baseline_avg_size: int = 1000,
    ) -> dict:
        """Detect anomalies in tool output.

        Args:
            output: Tool output
            tool_name: Tool name
            baseline_avg_size: Expected output size

        Returns:
            Dict with anomaly_score, type, should_skip_compression
        """
        if not output:
            return {
                "anomaly_score": 0.0,
                "anomaly_type": None,
                "should_skip_compression": False,
            }

        # Statistical check
        size_ratio = len(output) / baseline_avg_size if baseline_avg_size > 0 else 1.0
        statistical_score = min(1.0, abs(size_ratio - 1.0) / 2.0)

        # Semantic check
        semantic_result = await self._semantic_anomaly_check(output[:2000], tool_name)

        # Combine
        combined = statistical_score * 0.4 + semantic_result.get("score", 0.5) * 0.6

        return {
            "anomaly_score": combined,
            "anomaly_type": semantic_result.get("type") if combined > 0.7 else None,
            "should_skip_compression": combined > 0.7,
        }

    async def _semantic_anomaly_check(self, output: str, tool_name: str) -> dict:
        """Use Ollama to detect semantic anomalies."""
        prompt = f"""Detect anomalies in this {tool_name} output.
Look for: unexpected errors, security warnings, resource exhaustion.

Output:
{output}

Response: {{"type": "string|null", "score": 0-1, "severity": "low|medium|high"}}
Only JSON."""

        response = await self.ollama_client.generate(
            prompt=prompt,
            temperature=0.2,
            timeout=2.0,
        )

        if not response:
            return {"type": None, "score": 0.3, "severity": "low"}

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"type": None, "score": 0.2, "severity": "low"}
