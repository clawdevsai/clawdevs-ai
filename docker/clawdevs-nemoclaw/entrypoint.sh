#!/usr/bin/env bash

set -euo pipefail

mkdir -p "${HOME}" /data/nemoclaw

if ! command -v nemoclaw >/dev/null 2>&1 || ! command -v openshell >/dev/null 2>&1; then
  curl -fsSL "https://www.nvidia.com/nemoclaw.sh" | bash -s -- --non-interactive
fi

if ! command -v nemoclaw >/dev/null 2>&1 || ! command -v openshell >/dev/null 2>&1; then
  echo "[nemoclaw][error] failed to install nemoclaw/openshell" >&2
  exit 1
fi

export NEMOCLAW_SANDBOX_NAME="${NEMOCLAW_SANDBOX_NAME:-clawdevs-ai}"
export NEMOCLAW_PROVIDER="${NEMOCLAW_PROVIDER:-ollama}"
export NEMOCLAW_MODEL="${NEMOCLAW_MODEL:-mistral}"
export NEMOCLAW_POLICY_MODE="${NEMOCLAW_POLICY_MODE:-skip}"

if ! nemoclaw "${NEMOCLAW_SANDBOX_NAME}" status --json >/dev/null 2>&1; then
  nemoclaw onboard >/dev/null
fi

exec /opt/nemoclaw-bridge-venv/bin/uvicorn bridge:app --host 0.0.0.0 --port 18789 --app-dir /opt/nemoclaw-bridge
