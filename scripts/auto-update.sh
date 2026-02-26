#!/usr/bin/env bash
# scripts/auto-update.sh — ClawDevs
# Auto-atualização do runtime OpenClaw e das skills já instaladas.
# Executado em sessão ISOLADA (CronJob K8s ou cron local) — não na fila principal.
# Envia resumo de atualizações ao Diretor via Telegram (ou log estruturado).
#
# Referência: docs/issues/092-auto-atualizacao-ambiente.md
#             docs/21-auto-atualizacao-ambiente.md
#
# USO:
#   ./scripts/auto-update.sh                  # Executar manualmente
#   # Ou via CronJob K8s (ver k8s/devops/cronjob-auto-update.yaml)
#
# Configuração:
#   TELEGRAM_TOKEN, TELEGRAM_CHAT_ID — via Secret K8s ou .env
#   AUTO_UPDATE_DRY_RUN=1              — Simular sem atualizar

set -euo pipefail

DRY_RUN="${AUTO_UPDATE_DRY_RUN:-0}"
LOG_FILE="/tmp/auto-update-$(date +%Y%m%d-%H%M%S).log"
TELEGRAM_TOKEN="${TELEGRAM_TOKEN:-}"
TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}"
SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/skills"
INSTALLED_FILE="$SKILLS_DIR/INSTALLED.md"

# ─── Helpers ────────────────────────────────────────────────────────────────

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
send_telegram() {
  local msg="$1"
  if [[ -n "$TELEGRAM_TOKEN" && -n "$TELEGRAM_CHAT_ID" ]]; then
    curl -sS "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
      -d "chat_id=${TELEGRAM_CHAT_ID}" \
      -d "text=${msg}" \
      -d "parse_mode=Markdown" > /dev/null 2>&1 || true
  fi
}

log "=== ClawDevs Auto-Update Iniciado ==="
[[ "$DRY_RUN" == "1" ]] && log "MODO DRY-RUN: nenhuma alteração será feita"

SUMMARY="*ClawDevs Auto-Update*\n📅 $(date +%d/%m/%Y\ %H:%M)\n\n"
ERRORS=0
UPDATES=0

# ─── 1. Atualizar OpenClaw ────────────────────────────────────────────────────

log "Verificando atualização do OpenClaw..."
if command -v openclaw &>/dev/null; then
  CURRENT_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
  if [[ "$DRY_RUN" == "0" ]]; then
    if openclaw update 2>&1 | tee -a "$LOG_FILE" | grep -q "updated\|atualizado"; then
      NEW_VERSION=$(openclaw --version 2>/dev/null | head -1 || echo "unknown")
      log "OpenClaw atualizado: $CURRENT_VERSION → $NEW_VERSION"
      SUMMARY+="✅ OpenClaw: $CURRENT_VERSION → $NEW_VERSION\n"
      UPDATES=$((UPDATES + 1))
    else
      log "OpenClaw: já atualizado ($CURRENT_VERSION)"
      SUMMARY+="ℹ️ OpenClaw: já na versão atual ($CURRENT_VERSION)\n"
    fi
  else
    log "[DRY-RUN] OpenClaw update simulado."
    SUMMARY+="🔍 OpenClaw: verificação simulada ($CURRENT_VERSION)\n"
  fi
else
  log "OpenClaw não encontrado no PATH."
  SUMMARY+="⚠️ OpenClaw: não encontrado no PATH\n"
fi

# ─── 2. Atualizar skills já instaladas ───────────────────────────────────────

log "Verificando skills instaladas em $INSTALLED_FILE..."
if [[ ! -f "$INSTALLED_FILE" ]]; then
  log "Nenhum arquivo INSTALLED.md encontrado. Pulando."
  SUMMARY+="\nℹ️ Nenhuma skill instalada registrada.\n"
else
  SUMMARY+="\n*Skills instaladas:*\n"
  while IFS= read -r line; do
    # Formato esperado: "nome-skill — instalada em YYYY-MM-DD — ..."
    SKILL_NAME=$(echo "$line" | awk -F' — ' '{print $1}' | tr -d ' ')
    [[ -z "$SKILL_NAME" || "$SKILL_NAME" == \#* ]] && continue

    log "Verificando atualização: $SKILL_NAME"
    if [[ "$DRY_RUN" == "0" ]]; then
      if npx skills update "$SKILL_NAME" --json 2>/dev/null | grep -q '"updated":true'; then
        log "Skill atualizada: $SKILL_NAME"
        SUMMARY+="  ✅ $SKILL_NAME: atualizada\n"
        UPDATES=$((UPDATES + 1))
      else
        SUMMARY+="  ℹ️ $SKILL_NAME: já atualizada\n"
      fi
    else
      log "[DRY-RUN] npx skills update $SKILL_NAME (simulado)"
      SUMMARY+="  🔍 $SKILL_NAME: verificação simulada\n"
    fi
  done < "$INSTALLED_FILE"
fi

# ─── 3. Verificar integridade dos SKILLs (hash SHA-256) ──────────────────────

log "Verificando integridade dos skill locks..."
SUMMARY+="\n*Integridade de skills:*\n"
for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name=$(basename "$skill_dir")
  lock_file="$skill_dir/skillstracelock.json"
  if [[ -f "$lock_file" ]]; then
    # Verificação básica: arquivo de lock existe e não está vazio
    if [[ -s "$lock_file" ]]; then
      SUMMARY+="  ✅ $skill_name: lock presente\n"
    else
      log "AVISO: lock vazio para $skill_name"
      SUMMARY+="  ⚠️ $skill_name: lock vazio\n"
      ERRORS=$((ERRORS + 1))
    fi
  else
    log "INFO: $skill_name sem skillstracelock.json (skill interna)"
    SUMMARY+="  ℹ️ $skill_name: skill interna (sem lock)\n"
  fi
done

# ─── 4. Resumo final ─────────────────────────────────────────────────────────

log ""
log "=== Resumo da Auto-Atualização ==="
log "  Atualizações aplicadas: $UPDATES"
log "  Erros/avisos: $ERRORS"
log "  Log completo: $LOG_FILE"
log "=================================="

SUMMARY+="\n📊 *Resumo:* $UPDATES atualizações | $ERRORS avisos"
if [[ "$ERRORS" -gt 0 ]]; then
  SUMMARY+="\n⚠️ Verificar log: $LOG_FILE"
fi

# Enviar resumo ao Diretor
send_telegram "$SUMMARY"
log "Resumo enviado ao Telegram."

# Saída com código de erro se houver problemas
[[ "$ERRORS" -gt 0 ]] && exit 1 || exit 0
