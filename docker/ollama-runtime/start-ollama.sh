#!/usr/bin/env bash
set -euo pipefail

ollama serve &

for i in $(seq 1 60); do
  if ollama list >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if [ "${OLLAMA_AUTO_PULL_MODELS:-false}" = "true" ]; then
  for model in ${OLLAMA_BOOT_MODELS:-}; do
    ollama pull "${model}" || echo "Aviso: pull do modelo ${model} falhou."
  done
else
  echo "OLLAMA_AUTO_PULL_MODELS=false: iniciando sem pulls automaticos."
fi

wait
