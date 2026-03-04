# Developer não responde no Slack — checklist

Quando você menciona **@Developer** (ou "Developer APP") no canal e o agente não responde, verifique os pontos abaixo.

## 1. Conta Developer no gateway

No modelo **multi-account** (1 app Slack por agente), o Developer só recebe mensagens se existir a **conta** `developer` com tokens no cluster.

- **No `.env`** (raiz do repo): defina `DEVELOPER_SLACK_APP_TOKEN` e `DEVELOPER_SLACK_BOT_TOKEN` (tokens do app **Developer** em [api.slack.com/apps](https://api.slack.com/apps)).
- **No cluster:** rode `./scripts/openclaw/k8s-openclaw-secret-from-env.sh` e depois `kubectl rollout restart deployment/openclaw -n ai-agents`.
- **Validar:** use o script de diagnóstico: `./scripts/ops/slack-developer-check.sh` (verifica se a config do pod tem a conta `developer`).

Se você usa **um único app** (só `SLACK_APP_TOKEN` / `SLACK_BOT_TOKEN`), todas as mensagens vêm com `accountId: ceo` e só o CEO responde; para o Developer responder, é preciso um **app Slack separado** para o Developer e os dois tokens no Secret.

## 2. App Developer no canal

O app do Developer (bot) precisa estar **no canal** onde você escreve (ex.: #all-clawdevsai).

- No Slack: **Integrações** (ou configurações do canal) → **Adicionar apps** → escolher o app do Developer (ex.: "Developer APP") e adicionar ao canal.
- Se o app não estiver no canal, ele **não recebe** o evento `app_mention` e o gateway nunca invoca o agente Developer.

## 3. Scopes e eventos do app Developer

Em [api.slack.com/apps](https://api.slack.com/apps) → app do Developer → **OAuth & Permissions** → **Bot Token Scopes**, inclua:

- **`chat:write`** — para enviar respostas
- **`channels:read`** — para resolver canal (evita `missing_scope` nos logs)
- **`channels:history`** — para ler mensagens do canal
- **`app_mentions:read`** — para receber menções @Developer
- **`users:read`** (recomendado) — para resolver usuários

Em **Event Subscriptions** (ou **Subscribe to bot events**):

- **`app_mention`** — evento quando alguém menciona o bot no canal

Depois: **Reinstall to Workspace** para aplicar os scopes.

## 4. Menção correta

Ao escrever no canal, use a **menção real** ao bot (selecionando "Developer APP" no autocomplete ao digitar @). Se você digitar só `@Developer` como texto e não escolher o app na lista, o Slack pode não enviar o evento para o app certo.

## 5. Logs e Ollama

- **Logs do gateway:** `kubectl logs -n ai-agents deploy/openclaw -c gateway --tail=100`  
  Procure por `[developer]`, `embedded run`, ou erros. Se aparecer `[slack] [developer] starting provider`, o provider subiu; se após uma mensagem não houver `embedded run` para o developer, a mensagem pode não estar chegando (conta/canal/evento).
- **Ollama:** se o modelo estiver lento ou indisponível, o agente pode demorar ou não responder. Verifique: `kubectl get pods -n ai-agents -l app=ollama`.

## Resumo rápido

| Verificação | Ação |
|------------|------|
| Tokens Developer no cluster | `DEVELOPER_SLACK_APP_TOKEN` e `DEVELOPER_SLACK_BOT_TOKEN` no `.env` → `./scripts/openclaw/k8s-openclaw-secret-from-env.sh` → `kubectl rollout restart deployment/openclaw -n ai-agents` |
| App no canal | Adicionar o app do Developer ao canal #all-clawdevsai (Integrações → Adicionar apps) |
| Scopes | `chat:write`, `channels:read`, `channels:history`, `app_mentions:read`; evento `app_mention` |
| Menção | Usar @ e selecionar o bot "Developer APP" no autocomplete |

## Referências

- [42-slack-tokens-setup.md](../07-operations/42-slack-tokens-setup.md) — scopes e Event Subscriptions
- [investigacao-slack-nada-acontece.md](issues/investigacao-slack-nada-acontece.md) — multi-account e tokens
- [slack-mencoes-azul-bot-id.md](slack-mencoes-azul-bot-id.md) — menções entre bots
