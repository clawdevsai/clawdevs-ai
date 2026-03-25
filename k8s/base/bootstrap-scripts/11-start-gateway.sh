echo "[bootstrap] starting openclaw gateway"
echo "[bootstrap] running openclaw doctor --fix"
openclaw doctor --fix || echo "[bootstrap] warning: openclaw doctor --fix failed, proceeding with existing config"
set +e
openclaw gateway run --bind lan --port 18789
gateway_exit=$?
set -e
echo "[bootstrap] openclaw gateway exited with code ${gateway_exit}"
latest_gateway_log="$(ls -1t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -n 1 || true)"
if [ -n "${latest_gateway_log}" ] && [ -f "${latest_gateway_log}" ]; then
  cp "${latest_gateway_log}" "${BOOTSTRAP_LOG_DIR}/openclaw-gateway-last.log" || true
  cat "${latest_gateway_log}" || true
fi
exit "${gateway_exit}"
