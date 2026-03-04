# CEO e PO conversando no Slack — o que falta

**Cenário:** Dar um problema ao CEO no #all-clawdevsai e o CEO **conversar com o PO** sobre o assunto na mesma thread (dois agentes visíveis: CEO APP e PO APP).

---

## O que já está pronto


| Item                            | Status                                                                                                                                                   |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bindings Slack**              | CEO e PO mapeados por `accountId` e por `peer` (DM) em `k8s/management-team/openclaw/configmap.yaml`.                                                    |
| **Multi-account no entrypoint** | `entrypoint.sh` monta `channels.slack.accounts` a partir de `CEO_SLACK_*`, `PO_SLACK_*`, etc.                                                            |
| **Conversa compartilhada**      | Doc [interacao-agentes-mensageria.md](../03-agents/agents-devs/interacao-agentes-mensageria.md): responder no **mesmo canal/thread**; um agente por vez. |
| **Fluxo tema para análise**     | [43-fluxo-slack-all-clawdevsai-tema-analise.md](43-fluxo-slack-all-clawdevsai-tema-analise.md): rodada de opiniões no #all-clawdevsai.                   |
| **Instrução no CEO**            | AGENTS.md do CEO (workspace-ceo-configmap): para discutir no Slack, **incluir menção ao agente** (ex.: @PO).                                             |


---

## O que falta (checklist)

### 1. App Slack do PO conectado ao gateway

- **Criar app do PO** em [api.slack.com/apps](https://api.slack.com/apps) (se ainda não existir).
- **Preencher no `.env`** (a partir do `.env.example`):
  - `PO_SLACK_APP_TOKEN` (Socket Mode — connections:write)
  - `PO_SLACK_BOT_TOKEN` (OAuth — scopes de bot: chat:write, channels:read, etc.)
- **Injetar no cluster:** `./scripts/k8s-openclaw-secret-from-env.sh` e `kubectl rollout restart deployment/openclaw -n ai-agents`.

Sem isso, só o app do CEO recebe eventos; o PO nunca é “acordado” quando alguém menciona @PO.

### 2. App do PO no canal #all-clawdevsai

- No Slack: canal **#all-clawdevsai** → Integrações → **Adicionar apps** → escolher o **app do PO**.
- Assim, quando o CEO (ou o Diretor) escrever **@PO** na thread, o evento vai para o app do PO e o gateway roteia para o agente `po`.

### 3. Comportamento do CEO (já incluído no AGENTS.md)

- O CEO deve **incluir a menção** quando quiser discutir com o PO no canal, por exemplo:
  - *“Temos este problema: [X]. @PO qual sua visão sobre o backlog para este tema?”*
- A mensagem é publicada pelo app do CEO; o app do PO recebe a menção e o agente PO responde **na mesma thread** com a identidade do PO (Marina, conforme SOUL).

### 4. SOUL do PO (e dos outros agentes)

- Garantir que a SOUL do PO (e de quem mais participar de conversas no canal) diga:
  - Responder **no mesmo canal/thread** onde a mensagem chegou (conversa compartilhada).
  - **Um agente por vez:** dar uma resposta e encerrar o turno.
- O doc [interacao-agentes-mensageria.md](../03-agents/agents-devs/interacao-agentes-mensageria.md) já é a referência; pode ser referenciado ou resumido na SOUL de cada agente.

---

## Fluxo resumido

1. **Diretor** (ou você) posta no #all-clawdevsai: *“Quero analisar: [problema X].”*
2. **CEO** responde no canal (ex.: resume o tema e traz o PO para a discussão).
3. **CEO** inclui na mensagem: *“@PO preciso da sua visão sobre backlog.”* → o app do PO recebe a menção.
4. **PO** (agente) é acordado pelo gateway e responde **na mesma thread** com sua análise.
5. **CEO** (ou Diretor) pode responder em seguida na mesma thread — um agente por vez.

---

## Alternativa: sessions_spawn (sem segundo avatar)

Se não quiser configurar o app do PO no Slack, o CEO pode usar **sessions_spawn** para delegar uma pergunta ao PO. O PO roda em background e **anuncia** o resultado de volta na sessão do CEO; a resposta aparece na mesma thread, mas como mensagem da sessão do CEO (não como “PO APP” separado). Funcional para “CEO pergunta e recebe resposta do PO na thread”; para **dois avatares** (CEO APP e PO APP) falando no canal, é necessário o app do PO + menção.

---

## Referências

- [42-slack-tokens-setup.md](../07-operations/42-slack-tokens-setup.md) — tokens e um app por agente
- [interacao-agentes-mensageria.md](../03-agents/agents-devs/interacao-agentes-mensageria.md) — conversa compartilhada, um agente por vez
- [43-fluxo-slack-all-clawdevsai-tema-analise.md](43-fluxo-slack-all-clawdevsai-tema-analise.md) — tema para análise no Slack
- [OpenClaw — Slack](https://docs.openclaw.ai/channels/slack)

