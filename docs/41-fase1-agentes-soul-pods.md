# Fase 1 — Agentes: SOUL, pods e fluxo E2E

Roteiro da **Fase 1** do ClawDevs: definição canônica dos 9 agentes, SOUL (identidade e prompts), pods CEO/PO (nuvem) e técnicos (100% offline), código de conduta e fluxo evento-driven com exemplo E2E (Operação 2FA). Issues **010–019** em [docs/issues/README.md](issues/README.md).

## Escopo (issues 010–017)

| Issue | Título | Entregável |
|-------|--------|------------|
| **010** | Definição canônica dos nove agentes | [02-agentes.md](02-agentes.md); função, restrições, line-up, conflitos. |
| **011** | SOUL — identidade e prompts | Um SOUL por agente em [docs/soul/](soul/); integração com OpenClaw (SOUL.md no workspace ou por agente). |
| **012** | Pods CEO e PO (nuvem) | Deployment management-team com OpenClaw; Telegram; provedores nuvem (secrets). |
| **013** | Pod Developer (OpenCode + Ollama) | Deployment com OpenCode, PVC, GPU Lock; consumo Redis/eventos. |
| **014** | Pods Architect, QA, CyberSec, UX | Deployments ou Jobs event-driven; Ollama + GPU Lock; Redis Streams (ex.: code:ready). |
| **015** | Código de conduta e restrições | Regras "nunca fazer" por agente; [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md); guardrails VFM/ADL (ref.). |
| **016** | E2E Operação 2FA | Cenário documentado; fases (planejamento → fechamento); Redis; riscos. Ver [42-fluxo-e2e-operacao-2fa.md](42-fluxo-e2e-operacao-2fa.md). |
| **017** | Autonomia nível 4 | Matriz de escalonamento, CEO desempate, digest diário, five strikes, orçamento degradação (doc/operacional). |

## Estado atual (início da Fase 1)

- **010:** Definição em [02-agentes.md](02-agentes.md) e issues; tabela de conflitos referenciada.
- **011:** SOUL em [docs/soul/](soul/) (CEO, PO, DevOps, Architect, Developer, QA, CyberSec, UX, DBA, GovernanceProposer). CEO já tem SOUL injetado via [k8s/openclaw/workspace-ceo-configmap.yaml](../k8s/openclaw/workspace-ceo-configmap.yaml). Demais agentes: ConfigMap [k8s/soul/](../k8s/soul/) com SOUL compacto por agente (uso em workspaces ou referência).
- **012:** [k8s/management-team/](../k8s/management-team/) com deployment openclaw-management (CEO/PO), workspace CEO, secrets Telegram; provedor nuvem via llm-providers e secrets.
- **013:** Pod Developer em [k8s/developer/](../k8s/developer/) (PVC, consumer task:backlog, GPU Lock); `make developer-configmap` + `kubectl apply -f k8s/developer/`. OpenCode: integrar na imagem ou como evolução.
- **014:** Slot único Revisão pós-Dev (125) em [k8s/revisao-pos-dev/](../k8s/revisao-pos-dev/) implementa **Architect, QA, CyberSec e DBA** em sequência (um consumidor de code:ready, GPU Lock uma vez). Pods separados por agente (Architect, QA, CyberSec, UX como deployments individuais) são evolução opcional; hoje o slot atende 014.
- **015:** [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) com resumo por agente e link para soul/ e 02-agentes.
- **016:** [08-exemplo-de-fluxo.md](08-exemplo-de-fluxo.md) e [42-fluxo-e2e-operacao-2fa.md](42-fluxo-e2e-operacao-2fa.md) com fases, Redis e riscos.
- **017:** Documentação em 06-operacoes e issues; mecanismos (five strikes, digest) para implementação operacional.

## Topologia alvo (Fase 1)

- **Pods CEO/PO (nuvem):** Um deployment OpenClaw (management-team) com canal Telegram e provedores em nuvem (Ollama Cloud, OpenRouter, OpenAI, etc.). Único ponto de contato com o Diretor.
- **Pods técnicos (100% offline):** Um ou mais deployments/jobs com OpenClaw sub-agents (Developer, Architect, QA, CyberSec, UX, DBA, DevOps) usando apenas Ollama no cluster e Redis; NetworkPolicy sem egress. Slot único de revisão (code:ready) já implementado na Fase 0.
- **Fluxo:** Diretor → Telegram → CEO → PO → Redis (cmd:strategy, task:backlog, draft.2.issue, code:ready) → consumidores técnicos → GPU Lock → Ollama → resultado de volta ao Redis/CEO.

## Próximos passos

1. Completar integração SOUL para todos os agentes (workspace por agente ou SOUL.md por agente no OpenClaw).
2. Validar management-team com provedor nuvem (secret e llm-providers) e documentar em 09-setup ou 37-deploy.
3. Definir e aplicar deployments para time técnico (um pod OpenClaw técnico 100% offline ou um pod por agente, conforme issue 013/014).
4. Operacionalizar 017 (matriz de escalonamento, digest, five strikes) no orquestrador quando houver fluxo completo.

Referências: [.cursor/plans/plano_clawdevs_fases_5ff4260b.plan.md](../.cursor/plans/plano_clawdevs_fases_5ff4260b.plan.md), [docs/issues/README.md](issues/README.md).
