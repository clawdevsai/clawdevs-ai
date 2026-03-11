#!/usr/bin/env python3
"""
Developer trigger: consome task:backlog, envia tarefa ao agente Developer no OpenClaw.
Adquire lock por story, seta estado InProgress; o Developer (no Gateway) implementa e,
ao concluir, usa ferramenta/adapter para publicar code:ready e liberar o lock. Sem LLM neste script.
"""
import os
import sys

from app.bootstrap import bootstrap_paths

bootstrap_paths()

from app.agents.developer_agent import DeveloperAgent
from app.runtime import build_runtime_session_sender, build_runtime_tool_registry, run_stream_worker
from app.shared.redis_client import get_redis


def main() -> None:
    r = get_redis()
    registry = build_runtime_tool_registry()
    agent = DeveloperAgent()
    run_stream_worker(r, agent, build_runtime_session_sender(registry, role_name=agent.role_name, session_key=agent.session_key))


if __name__ == "__main__":
    main()
    sys.exit(0)
