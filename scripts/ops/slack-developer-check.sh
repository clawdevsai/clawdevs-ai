#!/usr/bin/env bash
# Verifica se o agente Developer está configurado para responder no Slack (conta developer no gateway).
# Uso: ./scripts/ops/slack-developer-check.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SECRET_SCRIPT="$REPO_ROOT/scripts/openclaw/k8s-openclaw-secret-from-env.sh"
cd "$REPO_ROOT"

echo "==> Checklist: Developer não responde no Slack"
echo ""

echo "1. Secret tem tokens do Developer (DEVELOPER_SLACK_APP_TOKEN e DEVELOPER_SLACK_BOT_TOKEN)?"
if ! kubectl get secret openclaw-telegram -n ai-agents &>/dev/null; then
  echo "   ERRO: Secret openclaw-telegram não existe. Rode: $SECRET_SCRIPT"
  exit 1
fi
HAS_DEV_APP=$(kubectl get secret openclaw-telegram -n ai-agents -o jsonpath='{.data.DEVELOPER_SLACK_APP_TOKEN}' 2>/dev/null | wc -c)
HAS_DEV_BOT=$(kubectl get secret openclaw-telegram -n ai-agents -o jsonpath='{.data.DEVELOPER_SLACK_BOT_TOKEN}' 2>/dev/null | wc -c)
if [[ "${HAS_DEV_APP:-0}" -lt 10 || "${HAS_DEV_BOT:-0}" -lt 10 ]]; then
  echo "   ERRO: Secret não tem DEVELOPER_SLACK_APP_TOKEN e/ou DEVELOPER_SLACK_BOT_TOKEN."
  echo "   No .env defina DEVELOPER_SLACK_APP_TOKEN e DEVELOPER_SLACK_BOT_TOKEN (app do Developer em api.slack.com/apps)."
  echo "   Depois: $SECRET_SCRIPT  &&  kubectl rollout restart deployment/openclaw -n ai-agents"
  exit 1
fi
echo "   OK: Secret tem os tokens do Developer."
echo ""

echo "2. Pod tem conta 'developer' na config do Slack?"
POD=$(kubectl get pods -n ai-agents -l app=openclaw -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)
if [[ -z "$POD" ]]; then
  echo "   AVISO: Pod openclaw não encontrado. Rode: make up"
  exit 1
fi
if kubectl exec -n ai-agents "$POD" -c gateway -- cat /tmp/openclaw.json 2>/dev/null | grep -q '"developer"'; then
  # Verifica se é dentro de accounts (evitar falso positivo em bindings)
  if kubectl exec -n ai-agents "$POD" -c gateway -- cat /tmp/openclaw.json 2>/dev/null | grep -A1 '"accounts"' | grep -q '"developer"'; then
    echo "   OK: Config do pod tem accounts.developer."
  else
    echo "   OK: Config menciona developer (bindings ou accounts)."
  fi
else
  echo "   ERRO: Config do pod NÃO tem conta 'developer'. O gateway não vai rotear mensagens do app Developer para o agente."
  echo "   Confirme no .env: DEVELOPER_SLACK_APP_TOKEN e DEVELOPER_SLACK_BOT_TOKEN; rode $SECRET_SCRIPT e kubectl rollout restart deployment/openclaw -n ai-agents"
  exit 1
fi
echo ""

echo "3. Provider [developer] nos logs (últimas linhas)?"
if kubectl logs -n ai-agents deploy/openclaw -c gateway --tail=50 2>/dev/null | grep -q '\[developer\]'; then
  echo "   OK: [slack] [developer] starting provider apareceu nos logs."
else
  echo "   AVISO: Nenhuma linha [developer] nos últimos 50 logs. Pode ser que o pod tenha reiniciado há pouco."
fi
echo ""

echo "4. Próximos passos se ainda não responder:"
echo "   - App do Developer está no canal? (Integrações do canal → Adicionar apps → Developer APP)"
echo "   - Scopes do app: chat:write, channels:read, channels:history, app_mentions:read; evento app_mention."
echo "   - Doc: docs/08-technical-notes/developer-nao-responde-slack.md"
echo ""
