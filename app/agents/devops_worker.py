#!/usr/bin/env python3
"""
DevOps trigger: consome event:devops (após merge), envia ao agente DevOps no OpenClaw.
O agente DevOps (no Gateway) atualiza estado Deployed, dispara pipeline se necessário
e emite feature_complete em orchestrator:events via ferramentas. Sem LLM neste script.
"""
import os
import sys

from app.bootstrap import bootstrap_paths

bootstrap_paths()

from app.agents.devops_agent import DevOpsAgent
from app.runtime import build_runtime_tool_registry, build_session_sender, run_stream_worker
from app.shared.redis_client import get_redis


def main() -> None:
    r = get_redis()
    registry = build_runtime_tool_registry()
    agent = DevOpsAgent()
    run_stream_worker(r, agent, build_session_sender(registry, role_name=agent.role_name))


if __name__ == "__main__":
    main()
