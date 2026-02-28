# Config OpenClaw (uso fora do K8s)

Configuração para rodar o OpenClaw **no host**: Telegram (só CEO) + Slack opcional (todos os agentes) + Ollama no cluster via port-forward.

## Regras de canal

- **Telegram:** somente o **agente CEO** conversa com o Diretor. Canal exclusivo CEO ↔ Diretor.
- **Slack:** **todos os agentes** podem conversar (CEO, PO, DevOps, Architect, etc.). Quando os agentes discutirem soluções entre si no Slack, é **obrigatório** usar **Ollama (LLM local com GPU)**.
- **Política rigorosa:** agentes diferentes do CEO não podem acessar outra plataforma além do Slack; apenas o CEO usa Telegram (e Slack).
- **Workspace único:** todos os agentes compartilham o mesmo workspace (ex.: `config/openclaw/workspace-ceo`).

## Telegram + Ollama (script pronto)

- **Config:** `openclaw.local.json5` — gateway local, canal Telegram, canal Slack (opcional), provedor Ollama em `http://127.0.0.1:11434/v1`.
- **Script:** `scripts/run-openclaw-telegram-ollama.sh` — faz port-forward do `svc/ollama-service` para 11434 e inicia `openclaw gateway`. Se `SLACK_APP_TOKEN` e `SLACK_BOT_TOKEN` estiverem no `.env`, o Slack é habilitado automaticamente.

Uso:

1. No cluster: `make up` (namespace ai-agents, redis, ollama, openclaw).
2. No host: defina `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` (ou `.env` na raiz). Para Slack: `SLACK_APP_TOKEN`, `SLACK_BOT_TOKEN` e opcionalmente `SLACK_DIRECTOR_USER_ID` (ver [docs OpenClaw Slack](https://docs.openclaw.ai/channels/slack)).
3. Execute:
   ```bash
   ./scripts/run-openclaw-telegram-ollama.sh
   ```
4. Envie uma mensagem ao **ClawDev bot** no Telegram (ou no Slack, se habilitado); a resposta sai do LLM Ollama.

Sem `TELEGRAM_CHAT_ID`: o script usa `dmPolicy: pairing`; aprove o primeiro DM com `openclaw pairing approve telegram <CODE>`.  
Sem `SLACK_DIRECTOR_USER_ID`: use `openclaw pairing approve slack <CODE>` no primeiro DM no Slack.

Ref: [openclaw-sub-agents-architecture.md](../../docs/openclaw-sub-agents-architecture.md)
