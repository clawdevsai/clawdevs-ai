#!/bin/sh
# Copyright (c) 2026 Diego Silva Morais <lukewaresoftwarehouse@gmail.com>
#
# Substitui o K8s Job 'generate-agent-token-job'.
# Roda no container 'token-init' (imagem curlimages/curl).
# Aguarda o panel-backend, faz login, gera token de agente e salva em volume compartilhado.

set -e

BACKEND="http://panel-backend:8000/api"
MAX_RETRIES=30
RETRY_DELAY=2

echo "[token-init] Aguardando panel-backend em $BACKEND..."
i=0
until curl -sf "$BACKEND/auth/login" > /dev/null 2>&1; do
  i=$((i + 1))
  if [ "$i" -ge "$MAX_RETRIES" ]; then
    echo "[token-init] ERRO: backend nao respondeu apos $MAX_RETRIES tentativas."
    exit 1
  fi
  echo "[token-init] Tentativa $i/$MAX_RETRIES..."
  sleep "$RETRY_DELAY"
done

echo "[token-init] Backend pronto. Fazendo login..."
LOGIN_RESP=$(curl -sf -X POST "$BACKEND/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${PANEL_ADMIN_USERNAME}\",\"password\":\"${PANEL_ADMIN_PASSWORD}\"}")

ADMIN_TOKEN=$(echo "$LOGIN_RESP" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "[token-init] ERRO: falha ao obter token admin. Resposta: $LOGIN_RESP"
  exit 1
fi

echo "[token-init] Login OK. Gerando token de agente..."
AGENT_RESP=$(curl -sf -X POST "$BACKEND/auth/agent-token" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

AGENT_TOKEN=$(echo "$AGENT_RESP" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$AGENT_TOKEN" ]; then
  echo "[token-init] ERRO: falha ao gerar token de agente. Resposta: $AGENT_RESP"
  exit 1
fi

echo "$AGENT_TOKEN" > /panel-token/PANEL_TOKEN
echo "[token-init] Token salvo em /panel-token/PANEL_TOKEN"
