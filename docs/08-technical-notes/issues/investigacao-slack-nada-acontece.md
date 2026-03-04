# Investigação: pelo Slack nada acontece

**Data:** 2026-03-04  
**Contexto:** Mensagem no canal (#all-clawdevsai) mencionando @CyberSec ("ola") sem resposta.

## Causas identificadas (logs e eventos)

### 1. Pod OpenClaw não subia (Pending)

- **Evento:** `0/1 nodes are available: pod has unbound immediate PersistentVolumeClaims. not found`
- **Motivo:** O PV `openclaw-shared-workspace-pv` estava em estado **Released** (tinha sido vinculado a um PVC antigo que foi deletado). O PVC atual (`openclaw-shared-workspace-pvc`) não conseguia vincular porque o PV ainda tinha `claimRef` apontando para o PVC antigo.
- **Correção aplicada:**  
  `kubectl patch pv openclaw-shared-workspace-pv --type=json -p='[{"op": "remove", "path": "/spec/claimRef"}]'`  
  Depois disso o PVC passou a **Bound** e o pod pôde ser agendado.

### 2. Gateway OpenClaw crashando (Config invalid)

- **Log:** `Config invalid` — `memorySearch` em nível top-level; chaves legadas `contextPruning`, `compaction` não reconhecidas; `agents.defaults.model` migrado para `model.primary`.
- **Motivo:** Configuração no ConfigMap em formato antigo para a versão atual do OpenClaw (v2026.3.2).
- **Correção aplicada:** Atualização em `k8s/management-team/openclaw/configmap.yaml`:
  - `memorySearch` movido para `agents.defaults.memorySearch`
  - `agents.defaults.model` alterado para `{ "primary": "ollama/glm-5:cloud" }`
  - Remoção dos blocos top-level `memorySearch`, `contextPruning` e `compaction`
- **Ação:** `kubectl apply -f k8s/management-team/openclaw/configmap.yaml` e `kubectl rollout restart deployment/openclaw -n ai-agents`

### 3. Outros pods (não bloqueavam o Slack)

- **acefalo-monitor / acefalo-heartbeat** em ContainerCreating: ConfigMap `acefalo-scripts` não encontrado.  
  **Solução:** Rodar `make configmap-acefalo` e em seguida `make orchestrator-apply` (ou reaplicar os deployments do acefalo).
- **init-memory-structure** em Pending: dependia do mesmo PVC; passou a agendar após o ajuste do PV.

## Estado após as correções

- Pod **openclaw** em **Running** (1/1).
- Checklist `./scripts/ops/slack-openclaw-check.sh`: OK (Secret com tokens, pod ready, `slack.enabled = true` no pod).

## Sobre @CyberSec no Slack

No modelo **multi-account** (1 app Slack por agente), a menção **@CyberSec** no canal só é recebida pelo gateway se existir um **app Slack** para o CyberSec e os tokens estiverem no cluster:

1. No `.env`: `CYBERSEC_SLACK_APP_TOKEN` e `CYBERSEC_SLACK_BOT_TOKEN` preenchidos (criar app em api.slack.com se necessário).
2. Rodar `./scripts/openclaw/k8s-openclaw-secret-from-env.sh` e depois `kubectl rollout restart deployment/openclaw -n ai-agents`.

Se apenas o app do CEO (ClawdevsAI) estiver configurado, mensagens no canal são recebidas com `accountId: ceo` e roteadas para o agente CEO. Para o CyberSec responder quando alguém menciona @CyberSec, é preciso ter o app do CyberSec instalado no workspace/canal e os tokens no Secret.

## Comandos úteis

```bash
# Diagnóstico Slack/OpenClaw
./scripts/ops/slack-openclaw-check.sh

# Logs do gateway em tempo real
kubectl logs -n ai-agents -l app=openclaw -f --tail=50

# Se o PV voltar a Released (após delete do PVC)
kubectl patch pv openclaw-shared-workspace-pv --type=json -p='[{"op": "remove", "path": "/spec/claimRef"}]'
```
