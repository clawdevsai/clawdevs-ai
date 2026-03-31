#!/usr/bin/env bash

set -euo pipefail

mkdir -p "${HOME}" /data/nemoclaw

# Check if NemoClaw runtime is available
nemoclaw_runtime_ok() {
  command -v nemoclaw >/dev/null 2>&1 || return 1
  nemoclaw --version >/dev/null 2>&1 || return 1
  return 0
}

install_nemoclaw() {
  curl -fsSL "https://raw.githubusercontent.com/NVIDIA/NemoClaw/main/install.sh" | bash -s -- --non-interactive
}

# Install OpenShell CLI (no gateway) if needed
install_openshell_cli() {
  curl -LsSf https://raw.githubusercontent.com/NVIDIA/OpenShell/main/install.sh | \
    OPENSHELL_VERSION="${OPENSHELL_VERSION:-v0.0.19}" OPENSHELL_INSTALL_DIR=/usr/local/bin sh
}

# Ensure NemoClaw is available
if ! nemoclaw_runtime_ok; then
  echo "[entrypoint] Installing NemoClaw..."
  install_nemoclaw
fi

# Try to install OpenShell if not already available
if ! command -v openshell >/dev/null 2>&1; then
  echo "[entrypoint] Installing OpenShell..."
  if install_openshell_cli; then
    echo "[entrypoint] OpenShell ready"
  else
    echo "[entrypoint] WARNING: OpenShell installation failed, continuing without it..."
  fi
else
  echo "[entrypoint] OpenShell already available"
fi

# Set up NemoClaw environment variables
export NEMOCLAW_SANDBOX_NAME="${NEMOCLAW_SANDBOX_NAME:-clawdevs-ai}"
export NEMOCLAW_PROVIDER="${NEMOCLAW_PROVIDER:-ollama}"
export NEMOCLAW_MODEL="${NEMOCLAW_MODEL:-mistral}"
export NEMOCLAW_POLICY_MODE="${NEMOCLAW_POLICY_MODE:-skip}"

export OPENSHELL_GATEWAY="${OPENSHELL_GATEWAY:-nemoclaw}"

echo "[entrypoint] Environment variables configured:"
echo "[entrypoint]   NEMOCLAW_SANDBOX_NAME=${NEMOCLAW_SANDBOX_NAME}"
echo "[entrypoint]   NEMOCLAW_PROVIDER=${NEMOCLAW_PROVIDER}"
echo "[entrypoint]   NEMOCLAW_MODEL=${NEMOCLAW_MODEL}"
echo "[entrypoint]   NEMOCLAW_POLICY_MODE=${NEMOCLAW_POLICY_MODE}"
echo "[entrypoint]   OPENSHELL_GATEWAY=${OPENSHELL_GATEWAY}"

# Run onboarding if needed
ONBOARD_DONE_FILE="/data/nemoclaw/.onboarding-done"
SANDBOX_LIST="$(nemoclaw list 2>/dev/null || true)"
if [ ! -f "${ONBOARD_DONE_FILE}" ] || [[ "${SANDBOX_LIST}" == *"No sandboxes registered"* ]]; then
  echo "[entrypoint] Running NemoClaw onboarding..."
  if [ -f "/data/nemoclaw/.nemoclaw/onboard.lock" ]; then
    rm -f "/data/nemoclaw/.nemoclaw/onboard.lock" >/dev/null 2>&1 || true
  fi
  if nemoclaw onboard 2>&1; then
    touch "${ONBOARD_DONE_FILE}"
    echo "[entrypoint] Onboarding completed successfully"
  else
    echo "[entrypoint] WARNING: Onboarding encountered issues, but continuing..."
  fi
else
  echo "[entrypoint] Onboarding already completed"
fi

# Ensure OpenShell gateway name is selected and running (best-effort)
if command -v openshell >/dev/null 2>&1; then
  mkdir -p /data/nemoclaw/.config/openshell >/dev/null 2>&1 || true
  if [ ! -f /data/nemoclaw/.config/openshell/active_gateway ]; then
    printf "%s" "${OPENSHELL_GATEWAY}" > /data/nemoclaw/.config/openshell/active_gateway 2>/dev/null || true
  fi
fi

# Start the NemoClaw bridge service
if [ -f "/opt/nemoclaw-bridge-venv/bin/uvicorn" ]; then
  echo "[entrypoint] Starting NemoClaw bridge service on port 18789..."
  exec /opt/nemoclaw-bridge-venv/bin/uvicorn bridge:app --host 0.0.0.0 --port 18789 --app-dir /opt/nemoclaw-bridge
else
  echo "[entrypoint] ERROR: NemoClaw bridge service not found at /opt/nemoclaw-bridge-venv/bin/uvicorn" >&2
  echo "[entrypoint] Make sure the bridge service is installed in the base Docker image" >&2
  exit 1
fi
