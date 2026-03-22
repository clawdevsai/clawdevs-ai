OPENCLAW_VERSION="${OPENCLAW_VERSION:-}"
if [ -n "${OPENCLAW_VERSION}" ]; then
  curl -fsSL "https://openclaw.ai/install.sh" | bash -s -- --no-onboard --no-prompt --version "${OPENCLAW_VERSION}"
else
  curl -fsSL "https://openclaw.ai/install.sh" | bash -s -- --no-onboard --no-prompt
fi
