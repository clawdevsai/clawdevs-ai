#!/usr/bin/env python3
"""
PO trigger: consome cmd:strategy (evento do CEO), envia contexto ao agente PO no OpenClaw.
O agente PO (no Gateway) usa ferramentas para ler Memoria, criar issues no GitHub,
gravar project:v1:issue:{id} e publicar em draft.2.issue. Sem LLM neste script.
"""
import os
import sys

from app.bootstrap import bootstrap_paths

bootstrap_paths()

from app.agents.po_agent import POAgent
from app.runtime import build_runtime_session_sender, build_runtime_tool_registry, run_stream_worker
from app.shared.redis_client import get_redis


def main() -> None:
    r = get_redis()
    registry = build_runtime_tool_registry()
    agent = POAgent()
    run_stream_worker(r, agent, build_runtime_session_sender(registry, role_name=agent.role_name, session_key=agent.session_key))


if __name__ == "__main__":
    main()
