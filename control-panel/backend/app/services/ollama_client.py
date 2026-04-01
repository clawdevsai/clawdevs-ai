"""Ollama client for Phase 6 semantic optimization."""
import asyncio
import aiohttp
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class OllamaClient:
    """Async HTTP client for Ollama API."""

    def __init__(self, base_url: str = "http://ollama:11434", model: str = "phi4-mini-reasoning:latest"):
        """Initialize Ollama client.

        Args:
            base_url: Ollama server URL (default: Docker internal network)
            model: Model name (default: phi4-mini-reasoning:latest)
        """
        self.base_url = base_url
        self.model = model
        self.timeout = aiohttp.ClientTimeout(total=5.0)

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
        top_p: float = 0.9,
        timeout: float = 3.0,
    ) -> Optional[str]:
        """Call Ollama generate endpoint.

        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1)
            top_p: Top-p sampling
            timeout: Request timeout in seconds

        Returns:
            Generated text or None if error/timeout
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature,
                        "top_p": top_p,
                    },
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "")
                    else:
                        logger.error(f"Ollama error: HTTP {resp.status}")
                        return None
        except asyncio.TimeoutError:
            logger.warning(f"Ollama timeout (>{timeout}s)")
            return None
        except Exception as e:
            logger.error(f"Ollama call failed: {e}")
            return None

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        timeout: float = 3.0,
    ) -> Optional[str]:
        """Call Ollama chat endpoint.

        Args:
            messages: Chat messages in format [{"role": "user", "content": "..."}]
            temperature: Sampling temperature
            timeout: Request timeout

        Returns:
            Response text or None
        """
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.post(
                    f"{self.base_url}/api/chat",
                    json={
                        "model": self.model,
                        "messages": messages,
                        "stream": False,
                        "temperature": temperature,
                    },
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("message", {}).get("content", "")
                    else:
                        logger.error(f"Ollama chat error: HTTP {resp.status}")
                        return None
        except asyncio.TimeoutError:
            logger.warning(f"Ollama chat timeout (>{timeout}s)")
            return None
        except Exception as e:
            logger.error(f"Ollama chat failed: {e}")
            return None

    async def health_check(self) -> bool:
        """Check if Ollama is accessible."""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2.0)) as session:
                async with session.get(f"{self.base_url}/api/tags") as resp:
                    return resp.status == 200
        except Exception:
            return False
