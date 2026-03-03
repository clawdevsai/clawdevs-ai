# Development Team — Time técnico (100% offline)

Agentes técnicos: **DevOps**, **Architect**, **Developer**, **QA**, **CyberSec**, **UX**, **DBA**. Operam **100% offline** da internet (NetworkPolicy egress bloqueado); inferência via **Ollama GPU** no cluster por padrão.

Provedor de LLM por agente: ConfigMap `clawdevs-llm-providers` (chaves `agent_devops`, `agent_architect`, etc.). Valores: `ollama_local` | `ollama_cloud` | `openrouter` | `qwen_oauth` | `moonshot_ai` | `openai` | `huggingface_inference`. Padrão: **ollama_local**.

Na Fase 0 atual, o time técnico roda como **sub-agents** do gateway Management (CEO/PO); um deployment dedicado 100% offline pode ser adicionado em fases posteriores usando este ConfigMap e a NetworkPolicy.

**Revisão pós-Dev (slot único):** [revisao-pos-dev/](revisao-pos-dev/) consome `code:ready`, executa Architect→QA→CyberSec→DBA em sequência. **Pods separados (evolução 014):** [architect/](architect/), [qa/](qa/), [cybersec/](cybersec/), [dba/](dba/) formam um pipeline (replicas: 0 por padrão); `make agent-slots-configmap` e aplicar os manifestos; inicializar consumer groups com [scripts/redis-streams-init.sh](../scripts/redis-streams-init.sh).

## GitHub (todos os agentes)

Para que os agentes tenham acesso ao GitHub (gh CLI, push/pull, Issues, PRs), crie o Secret a partir do `.env`:

```bash
# Exporte do .env (ou defina GITHUB_TOKEN no shell) e crie o secret:
export $(grep -E '^GITHUB_TOKEN=|^GH_TOKEN=' .env 2>/dev/null | xargs)
kubectl create secret generic clawdevs-github-secret -n ai-agents \
  --from-literal=GITHUB_TOKEN="${GITHUB_TOKEN:?defina GITHUB_TOKEN no .env}" \
  --from-literal=GH_TOKEN="${GH_TOKEN:-$GITHUB_TOKEN}" \
  --dry-run=client -o yaml | kubectl apply -f -
```

Os deployments (architect, developer, qa, cybersec, dba, revisao-pos-dev, gateway-redis-adapter) e o OpenClaw já referenciam `clawdevs-github-secret` com `optional: true`; se o Secret não existir, os pods sobem sem as variáveis. Ver [secret-github.example.yaml](secret-github.example.yaml). Ref: [docs/20-ferramenta-github-gh.md](../docs/20-ferramenta-github-gh.md).

## Apply

```bash
kubectl apply -f k8s/development-team/configmap.yaml
# Opcional (quando houver pod dedicado): kubectl apply -f k8s/development-team/networkpolicy.yaml
```

Ref: [docs/04-infraestrutura.md](../docs/04-infraestrutura.md), [docs/14-seguranca-runtime-agentes.md](../docs/14-seguranca-runtime-agentes.md).
