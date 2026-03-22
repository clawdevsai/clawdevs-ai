# Documentação operacional (clawdevs-ai)

- **O que a aplicação faz e exemplos de uso:** [aplicacao-e-exemplos.md](./aplicacao-e-exemplos.md)
- **Papel de cada agente (um arquivo por agente):** [agentes/README.md](./agentes/README.md)
- **Arquivos do workspace do agente (OpenClaw + ClawDevs):** [workspace-arquivos-agente.md](./workspace-arquivos-agente.md)

## Stack Kubernetes

| Recurso | Nome / observação |
|--------|-------------------|
| OpenClaw | `StatefulSet` `clawdevs-ai`, pod típico `clawdevs-ai-0`, container `openclaw` |
| Ollama | `Pod` `ollama`, `Service` `ollama` |
| PVC | `ollama-data` (`k8s/base/ollama-pvc.yaml`) |
| SearXNG | `k8s/base/searxng-deployment.yaml` |
| Rede | `k8s/base/networkpolicy-allow-egress.yaml` |
| Segredos | `openclaw-auth`, `ollama-auth` gerados por `k8s/kustomization.yaml` a partir de `k8s/.env` |
| Config agentes | `ConfigMap` `openclaw-agent-config` (arquivos em `k8s/base/openclaw-config/`) |

## Kustomize

- `kubectl apply -k k8s` usa apenas `k8s/base` (via `k8s/kustomization.yaml` → `resources: [base]`).
- GPU no Ollama: overlay `k8s/overlays/gpu` (RuntimeClass, device plugin, patch do pod `ollama`). Aplicar com `make openclaw-apply-gpu`, `make gpu-migrate-apply` (contexto `docker-desktop`) ou `kubectl apply -k k8s/overlays/gpu`.

## Segredos obrigatórios (`make preflight`)

Chaves que devem estar preenchidas em `k8s/.env`:

- `OPENCLAW_GATEWAY_TOKEN`
- `TELEGRAM_BOT_TOKEN_CEO`
- `TELEGRAM_CHAT_ID_CEO`
- `GITHUB_TOKEN`
- `GITHUB_ORG`
- `OLLAMA_API_KEY`

Demais variáveis: ver `k8s/.env.example`.

## Targets Make relevantes

- `make preflight` — valida segredos em `k8s/.env`
- `make manifests-validate` — `kubectl kustomize k8s`
- `make clawdevs-up` — Minikube + addons + `stack-apply` + status
- `make clawdevs-rebuild` — `destroy-all`, sobe cluster de novo, `storage-enable-expansion`, `stack-apply`
- `make stack-apply` — `ollama-apply` + `openclaw-apply`
- `make openclaw-apply` — `kubectl apply -k k8s` (contexto `KUBE_CONTEXT`, default `clawdevs-ai`)
- `make openclaw-apply-gpu` — aplica `k8s/overlays/gpu`
- `make openclaw-restart` / `make openclaw-logs` — `statefulset/clawdevs-ai`
- `make ollama-volume-apply` — PVC; `make ollama-apply` — recria pod `ollama`
- Fluxo Docker Desktop + GPU: `gpu-doctor`, `docker-k8s-check`, `gpu-plugin-apply`, `gpu-node-check`, `gpu-migrate-apply`

## Exec no pod OpenClaw

Usar o workload real, por exemplo:

```bash
kubectl --context=clawdevs-ai exec -it statefulset/clawdevs-ai -c openclaw -- bash
```

## Estrutura `k8s/` (resumo)

```text
k8s/
  .env
  .env.example
  kustomization.yaml
  base/
    kustomization.yaml
    openclaw-pod.yaml
    ollama-pod.yaml
    ollama-pvc.yaml
    networkpolicy-allow-egress.yaml
    searxng-deployment.yaml
    openclaw-config/
  overlays/
    gpu/
```
