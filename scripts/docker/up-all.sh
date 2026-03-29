#!/usr/bin/env bash

set -euo pipefail

ENV_FILE="${1:-.env}"
STACK_NETWORK="${2:-clawdevs}"
POSTGRES_IMAGE="${3:-clawdevsai/postgres-runtime:local}"
REDIS_IMAGE="${4:-clawdevsai/redis-runtime:local}"
OLLAMA_IMAGE="${5:-clawdevsai/ollama-runtime:local}"
SEARXNG_IMAGE="${6:-clawdevsai/searxng-runtime:local}"
SEARXNG_PROXY_IMAGE="${7:-clawdevsai/searxng-proxy:local}"
PANEL_BACKEND_IMAGE="${8:-clawdevsai/clawdevs-panel-backend:local}"
PANEL_WORKER_IMAGE="${9:-clawdevsai/clawdevs-panel-worker:local}"
PANEL_FRONTEND_IMAGE="${10:-clawdevsai/clawdevs-panel-frontend:local}"
TOKEN_INIT_IMAGE="${11:-clawdevsai/token-init-runtime:local}"
SEARXNG_PROXY_CONF="${12:-docker/clawdevs-searxng-proxy/default.conf}"

load_env_file() {
  local env_file="$1"
  while IFS= read -r raw_line || [ -n "$raw_line" ]; do
    line="${raw_line%$'\r'}"
    case "$line" in
      ''|\#*) continue ;;
    esac
    key="${line%%=*}"
    value="${line#*=}"
    key="$(printf '%s' "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    key="${key#export }"
    if ! printf '%s' "$key" | grep -Eq '^[A-Za-z_][A-Za-z0-9_]*$'; then
      echo "[up] ERRO: chave invalida no .env: $key"
      return 1
    fi
    export "$key=$value"
  done < "$env_file"
}

wait_for_health() {
  local name="${1:-}"
  local timeout="${2:-120}"
  local elapsed=0
  local status=""
  while true; do
    status="$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$name" 2>/dev/null || true)"
    if [ "$status" = "healthy" ] || [ "$status" = "running" ]; then
      echo "[up] $name pronto ($status)"
      return 0
    fi
    if [ "$status" = "exited" ] || [ "$status" = "dead" ] || [ "$status" = "unhealthy" ]; then
      echo "[up] ERRO: $name em estado $status"
      docker logs "$name" || true
      return 1
    fi
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "[up] ERRO: timeout aguardando $name"
      docker logs "$name" || true
      return 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done
}

wait_for_running() {
  local name="${1:-}"
  local timeout="${2:-120}"
  local elapsed=0
  local status=""
  while true; do
    status="$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || true)"
    if [ "$status" = "running" ]; then
      echo "[up] $name pronto ($status)"
      return 0
    fi
    if [ "$status" = "exited" ] || [ "$status" = "dead" ]; then
      echo "[up] ERRO: $name em estado $status"
      docker logs "$name" || true
      return 1
    fi
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "[up] ERRO: timeout aguardando $name"
      docker logs "$name" || true
      return 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done
}

wait_for_exit_success() {
  local name="${1:-}"
  local timeout="${2:-180}"
  local elapsed=0
  local status=""
  local code=""
  while true; do
    status="$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || true)"
    if [ "$status" = "exited" ]; then
      code="$(docker inspect -f '{{.State.ExitCode}}' "$name")"
      if [ "$code" = "0" ]; then
        echo "[up] $name concluido com sucesso"
        return 0
      fi
      echo "[up] ERRO: $name finalizou com exit code $code"
      docker logs "$name" || true
      return 1
    fi
    if [ "$status" = "dead" ] || [ -z "$status" ]; then
      echo "[up] ERRO: $name em estado $status"
      docker logs "$name" || true
      return 1
    fi
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "[up] ERRO: timeout aguardando $name"
      docker logs "$name" || true
      return 1
    fi
    sleep 2
    elapsed=$((elapsed + 2))
  done
}

load_env_file "$ENV_FILE"

# Start postgres
echo "[up] iniciando clawdevs-postgres"
docker run -d --name clawdevs-postgres --network "$STACK_NETWORK" --network-alias postgres \
  -e POSTGRES_DB=clawdevs_panel \
  -e POSTGRES_USER=panel \
  -e POSTGRES_PASSWORD="$PANEL_DB_PASSWORD" \
  -v postgres-data:/var/lib/postgresql/data \
  --health-cmd="pg_isready -U panel -d clawdevs_panel" \
  --health-interval=5s --health-timeout=3s --health-retries=10 --health-start-period=10s \
  --restart unless-stopped \
  "$POSTGRES_IMAGE" >/dev/null
wait_for_health clawdevs-postgres 180

# Start redis
echo "[up] iniciando clawdevs-redis"
docker run -d --name clawdevs-redis --network "$STACK_NETWORK" --network-alias redis \
  -e PANEL_REDIS_PASSWORD="$PANEL_REDIS_PASSWORD" \
  --health-cmd="sh -c 'redis-cli -a $PANEL_REDIS_PASSWORD ping | grep PONG'" \
  --health-interval=5s --health-timeout=3s --health-retries=10 --health-start-period=5s \
  --restart unless-stopped \
  "$REDIS_IMAGE" \
  redis-server --requirepass "$PANEL_REDIS_PASSWORD" >/dev/null
wait_for_health clawdevs-redis 120

echo "[up] Stack iniciada com sucesso!"
echo "  http://localhost:3000        Painel de Controle"
echo "  http://localhost:8000/docs   API Docs"
echo "  http://localhost:18789       OpenClaw Gateway"
echo "  http://localhost:11434       Ollama API"
