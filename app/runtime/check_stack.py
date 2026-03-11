#!/usr/bin/env python3
"""Verificacao operacional da stack OpenClaw + Ollama."""
from __future__ import annotations

import json
import sys

from app.runtime import load_runtime_stack_config, validate_runtime_stack


def main() -> int:
    config = load_runtime_stack_config()
    errors = validate_runtime_stack(config)
    payload = {
        "stack": config.stack_label,
        "openclaw_required": config.openclaw_required,
        "model_provider": config.model_provider,
        "model_mode": config.model_mode,
        "ollama_base_url": config.ollama_base_url,
        "ollama_model": config.ollama_model,
        "ok": not errors,
        "errors": errors,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
