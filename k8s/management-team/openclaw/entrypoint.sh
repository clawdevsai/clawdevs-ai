#!/bin/sh
# Injeta TELEGRAM_CHAT_ID e Slack (allowFrom, enabled) na config e inicia o gateway.
# Telegram: só CEO. Slack: todos os agentes; habilitado quando SLACK_APP_TOKEN e SLACK_BOT_TOKEN estão definidos.
set -e
CONFIG_SRC="/config/openclaw.json"
CONFIG_RUN="/tmp/openclaw.json"

# 1) Telegram
if [ -n "$TELEGRAM_CHAT_ID" ]; then
  sed "s/__TELEGRAM_CHAT_ID__/$TELEGRAM_CHAT_ID/g" "$CONFIG_SRC" > "$CONFIG_RUN"
else
  sed 's/"allowFrom": \["__TELEGRAM_CHAT_ID__"\]/"allowFrom": []/' "$CONFIG_SRC" | \
  sed 's/"dmPolicy": "allowlist"/"dmPolicy": "pairing"/' > "$CONFIG_RUN"
fi

# 2) Slack: habilitar e injetar allowFrom quando tokens presentes
if [ -n "$SLACK_APP_TOKEN" ] && [ -n "$SLACK_BOT_TOKEN" ]; then
  sed 's/"slack": { "enabled": false/"slack": { "enabled": true/' "$CONFIG_RUN" > "$CONFIG_RUN.tmp" && mv "$CONFIG_RUN.tmp" "$CONFIG_RUN"
  if [ -n "$SLACK_DIRECTOR_USER_ID" ]; then
    sed "s/__SLACK_DIRECTOR_USER_ID__/$SLACK_DIRECTOR_USER_ID/g" "$CONFIG_RUN" > "$CONFIG_RUN.tmp" && mv "$CONFIG_RUN.tmp" "$CONFIG_RUN"
  else
    sed 's/"allowFrom": \["__SLACK_DIRECTOR_USER_ID__"\]/"allowFrom": []/' "$CONFIG_RUN" > "$CONFIG_RUN.tmp" && mv "$CONFIG_RUN.tmp" "$CONFIG_RUN"
  fi
else
  sed 's/"allowFrom": \["__SLACK_DIRECTOR_USER_ID__"\]/"allowFrom": []/' "$CONFIG_RUN" > "$CONFIG_RUN.tmp" && mv "$CONFIG_RUN.tmp" "$CONFIG_RUN"
fi

export OPENCLAW_CONFIG_PATH="$CONFIG_RUN"
exec openclaw gateway --allow-unconfigured --port 18789 --bind lan
