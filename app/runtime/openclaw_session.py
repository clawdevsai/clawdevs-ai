#!/usr/bin/env python3
"""Resolucao explicita de sessao OpenClaw para a stack Ollama."""
from __future__ import annotations

from dataclasses import dataclass

from .model_provider import RuntimeStackConfig


@dataclass(frozen=True, slots=True)
class OpenClawSessionConfig:
    session_key: str
    provider: str
    mode: str
    model: str
    base_url: str

    def to_payload(self) -> dict[str, str]:
        return {
            "provider": self.provider,
            "mode": self.mode,
            "model": self.model,
            "baseUrl": self.base_url,
        }


def resolve_openclaw_session_config(session_key: str, stack: RuntimeStackConfig) -> OpenClawSessionConfig:
    return OpenClawSessionConfig(
        session_key=session_key,
        provider=stack.model_provider,
        mode=stack.model_mode,
        model=stack.ollama_model,
        base_url=stack.ollama_base_url,
    )
