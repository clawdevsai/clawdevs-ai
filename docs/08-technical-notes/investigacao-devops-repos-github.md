# Investigação: DevOps não cria repositório no GitHub — causa raiz e resolução

**Data:** 2026-03-04  
**Status:** Resolvido

---

## Sintoma

- Usuário pediu ao DevOps (via Slack) para criar o repositório **user-api** na organização **clawdevs-ai**.
- O DevOps respondeu com um plano, mostrou o comando `gh repo create clawdevs-ai/user-api ...`, mas **não criou o repo** no GitHub e **não informou o erro** ao usuário.
- `~/clawdevs-shared/repos/` no host ficou vazio; https://github.com/clawdevs-ai não tinha repositórios.

---

## Causas identificadas (em ordem cronológica)

### 1. `gh` CLI e token — OK

- `gh` instalado no pod (`/usr/bin/gh`), autenticado como `clawdevsai` via `GH_TOKEN`.
- Scopes do token: `repo`, `workflow`, `read:user`, `user:email`.
- Secret `clawdevs-github-secret` presente com `GITHUB_USER=clawdevsai`, `GITHUB_ORG=clawdevs-ai`.

### 2. Path e mount — OK

- PVC `openclaw-shared-workspace-pvc` → `/workspace` no pod = `~/clawdevs-shared` no host.
- `/workspace/repos/` acessível e com permissão 777.

### 3. Exec bloqueado por aprovação no gateway (corrigido)

O OpenClaw usava por padrão `security: allowlist` e `ask: on-miss` para exec no gateway. Sem UI de aprovação no pod K8s, o fallback era **deny** e o comando `gh repo create` ficava como `approval-pending` e não rodava.

**Correção:** em `openclaw-config` (configmap.yaml), exec foi configurado por agente:
- **CEO:** `tools.exec.security: "deny"` (CEO não executa no host).
- **Demais agentes** (po, devops, architect, developer, qa, cybersec, ux, dba): `tools.exec` com `host: "gateway"`, `security: "full"`, `ask: "off"`.

Ref: [Exec tool](https://docs.openclaw.ai/tools/exec), [Exec approvals](https://docs.openclaw.ai/tools/exec-approvals).

### 4. Falso positivo — agente diz que criou sem verificar (corrigido)

O modelo respondia em texto que "criou o repositório" sem ter chamado a tool `exec` ou sem ter lido a saída.

**Correção:** regras no TOOLS.md e soul-devops exigem:
- Invocar a tool `exec` com o comando real.
- Ler a saída do exec antes de afirmar sucesso.
- Reportar o texto exato do erro se falhar.

### 5. OAuth App access restrictions na organização (causa raiz final — resolvido)

Mesmo com exec funcionando, `gh repo create clawdevs-ai/...` retornava:

```
GraphQL: Although you appear to have the correct authorization credentials,
the `clawdevs-ai` organization has enabled OAuth App access restrictions,
meaning that data access to third-parties is limited.
```

Isso bloqueava **todas** as operações na org (criar repo, listar, atualizar) tanto via `gh` quanto via API REST (HTTP 403). A criação na conta pessoal `clawdevsai` funcionava normalmente.

**Correção:** o owner da org removeu as restrições de OAuth apps:
- **https://github.com/organizations/clawdevs-ai/settings/oauth_application_policy**
- **"Remove restrictions"** → Policy: No restrictions.

Após isso, `gh repo create clawdevs-ai/user-api` executou com sucesso e o repo foi criado.

---

## Estado atual (resolvido)

| Item | Estado |
|------|--------|
| `gh` no pod | OK (`/usr/bin/gh`) |
| Token / auth | OK (clawdevsai, scopes repo+workflow) |
| `GITHUB_ORG` | `clawdevs-ai` (no secret e no pod) |
| Exec no gateway | OK (security=full, ask=off por agente; CEO=deny) |
| OAuth App policy da org | **No restrictions** |
| Repo `clawdevs-ai/user-api` | **Criado** (private) |
| TOOLS.md / soul-devops | Regras de verificação antes de afirmar sucesso |

---

## Como investigar (logs e K8s)

O agente **DevOps** roda dentro do **gateway OpenClaw** (não é um pod separado). O deployment é `openclaw` no namespace `ai-agents`, container `gateway`.

### Ver logs do gateway

```bash
kubectl logs -n ai-agents deploy/openclaw -c gateway -f
kubectl logs -n ai-agents deploy/openclaw -c gateway --tail=200
kubectl logs -n ai-agents deploy/openclaw -c gateway --tail=500 | grep -E 'exec|gh|repo create'
```

### Verificar ambiente no pod

```bash
kubectl exec -n ai-agents deploy/openclaw -c gateway -- sh -c 'which gh; echo GITHUB_ORG=$GITHUB_ORG; echo GITHUB_USER=$GITHUB_USER; gh auth status'
```

### Verificar workspace e repos

```bash
kubectl exec -n ai-agents deploy/openclaw -c gateway -- ls -la /workspace/repos/
```

### Teste rápido de criação

```bash
kubectl exec -n ai-agents deploy/openclaw -c gateway -- sh -c 'gh repo create $GITHUB_ORG/test-temp --private --clone=false 2>&1'
```

### Script de diagnóstico Slack

```bash
./scripts/ops/slack-devops-check.sh
```

### 6. LLM sem GPU — timeout em modelos locais (corrigido)

- **Problema:** modelos locais (`qwen2.5:3b`, `deepseek-r1:8b`) rodavam em CPU (`size_vram: 0` no `ollama ps`), causando `LLM request timed out`. Modelos cloud (`ministral-3:14b-cloud`) funcionavam mas não geravam tool calls via OpenClaw (discovery falhou: `Failed to discover Ollama models`).
- **Causa:** Minikube iniciado com `--gpus=all` passava os devices (`/dev/nvidia*`) mas não as libs do driver NVIDIA (`libnvidia-ml.so`, `libcuda.so`, etc.) e o NVIDIA Container Toolkit não estava configurado dentro do container. O `nvidia-device-plugin` reportava `Incompatible strategy detected auto` / `No devices found`.
- **Correção (2026-03-04):**
  1. Copiar driver libs do host (`/usr/lib/x86_64-linux-gnu/libnvidia*.so*`, `libcuda*.so*`) + `nvidia-smi` para dentro do container Minikube.
  2. Configurar Docker runtime nvidia via `nvidia-ctk runtime configure --runtime=docker --set-as-default`.
  3. Gerar CDI spec via `nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`.
  4. Reiniciar Docker (SIGHUP) + rollout restart `nvidia-device-plugin-daemonset`.
  5. Adicionar `nvidia.com/gpu: "1"` nos `resources.requests` e `resources.limits` do deployment Ollama.
- **Automatização:** `make gpu-setup` (`scripts/ops/minikube-gpu-setup.sh`) — deve ser executado após cada `minikube start --gpus=all`.
- **Validação:** `kubectl exec -n ai-agents deploy/ollama-gpu -- ollama ps` deve mostrar `100% GPU` na coluna PROCESSOR.

---

## Referências

- `k8s/management-team/openclaw/configmap.yaml` — config OpenClaw (tools.exec por agente).
- `k8s/management-team/openclaw/workspace-devops-configmap.yaml` — TOOLS.md + GITHUB-CONTEXT.md do DevOps.
- `k8s/development-team/devops/soul/configmap.yaml` — SOUL do DevOps (regras de verificação).
- `docs/05-tools-and-skills/github-org-clawdevs-ai.md` — dados da organização e OAuth restriction.
- `docs/05-tools-and-skills/skills/github/SKILL.md` — skill github com fluxo de criação e tratamento de erros.
- `docs/08-technical-notes/devops-nao-responde-slack.md` — checklist se o DevOps não responder no Slack.
- `scripts/ops/slack-devops-check.sh` — diagnóstico de tokens e conta devops no cluster.
- `scripts/ops/minikube-gpu-setup.sh` — setup GPU pós-restart do Minikube (make gpu-setup).
- `k8s/ollama/deployment.yaml` — deployment Ollama com `nvidia.com/gpu: "1"`.
