# Phase 4: Compatibility and Rollout Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md.

**Date:** 2026-04-09
**Phase:** 04-compatibility-and-rollout-hardening
**Areas discussed:** Matriz de compatibilidade por rota, Estratégia de auth/sessão, Checklist de release readiness

---

## Matriz de compatibilidade por rota

| Option | Description | Selected |
|--------|-------------|----------|
| 1A | Tier A com interação + Tier B com render/navegação | ✓ |
| 1B | Todas as rotas com interação mínima | |
| 1C | Apenas rotas core já cobertas no shell smoke | |

**User's choice:** 1A
**Notes:** Priorização de risco: interação completa nas rotas mais críticas e cobertura leve no restante.

---

## Estratégia de auth/sessão

| Option | Description | Selected |
|--------|-------------|----------|
| 2A | E2E determinístico com intercepts (login sucesso/falha, 401/403, Authorization header) | ✓ |
| 2B | Intercepts + 1 verificação com backend real | |
| 2C | Somente backend real | |

**User's choice:** 2A
**Notes:** Foco em estabilidade e reprodutibilidade dos testes para gate de release.

---

## Checklist de release readiness

| Option | Description | Selected |
|--------|-------------|----------|
| 5A | typecheck + build + 3 specs Cypress + checklist manual curto | ✓ |
| 5B | typecheck + build + 3 specs Cypress (sem checklist manual) | |
| 5C | build + 1 smoke apenas | |

**User's choice:** 5A
**Notes:** Necessidade de evidência técnica automatizada + validação humana final rápida.

---

## the agent's Discretion

- Ajustar granularidade das asserções por rota dentro dos tiers definidos.
- Definir melhor composição dos testes (ajustes em specs existentes vs spec consolidado), mantendo gates acordados.

## Deferred Ideas

None.
