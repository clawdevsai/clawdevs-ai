OPENCLAW_STAMP="${OPENCLAW_STATE_DIR}/backlog/status/.openclaw-installed"
if command -v openclaw >/dev/null 2>&1; then
  echo "[bootstrap] openclaw ja instalado na imagem, pulando instalacao"
  touch "${OPENCLAW_STAMP}"
elif [ ! -f "${OPENCLAW_STAMP}" ] || ! command -v openclaw >/dev/null 2>&1; then
  OPENCLAW_VERSION="${OPENCLAW_VERSION:-}"
  if [ -n "${OPENCLAW_VERSION}" ]; then
    curl -fsSL "https://openclaw.ai/install.sh" | bash -s -- --no-onboard --no-prompt --version "${OPENCLAW_VERSION}"
  else
    curl -fsSL "https://openclaw.ai/install.sh" | bash -s -- --no-onboard --no-prompt
  fi
  touch "${OPENCLAW_STAMP}"
else
  echo "[bootstrap] openclaw ja instalado, pulando instalacao"
fi
if ! command -v openclaw >/dev/null 2>&1; then
  echo "OpenClaw nao foi instalado corretamente" >&2
  exit 1
fi
openclaw --version | head -n 1
