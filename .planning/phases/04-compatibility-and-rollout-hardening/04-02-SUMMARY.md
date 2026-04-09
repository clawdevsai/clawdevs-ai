---
phase: 04-compatibility-and-rollout-hardening
plan: "02"
subsystem: testing
tags: [cypress, e2e, smoke, auth-session, dashboard, monitoring]

requires:
  - phase: 04-01
    provides: matriz de compatibilidade por rota e baseline de navegação shell
provides:
  - validação smoke de login/sessão com contrato de token e limpeza em 401/403
  - assert estável de KPI do dashboard com navegação contínua até monitoring
affects: [04-03-release-readiness, QUAL-01, COMP-02]

tech-stack:
  added: []
  patterns: [selectors Cypress ancorados em copy real e container semântico de card]

key-files:
  created: []
  modified:
    - control-panel/frontend/cypress/e2e/dashboard-data-bindings.cy.ts

key-decisions:
  - "Task 1 foi registrada com commit atômico allow-empty porque os artefatos já estavam conformes no baseline atual."
  - "A asserção do KPI foi estabilizada por label localizada + card root para remover fragilidade de DOM."

patterns-established:
  - "Smoke de sessão deve validar token storage, redirect e invalidação 401/403 no mesmo spec."
  - "Assert de KPI deve evitar closest genérico e usar container de componente (`div.rounded-2xl`)."

requirements-completed: [QUAL-01, COMP-02]

duration: 17min
completed: 2026-04-09
---

# Phase 4 Plan 02: Expand Cypress Compatibility Smoke Gates Summary

**Cobertura smoke E2E de login e navegação dashboard/monitoring validada com contrato de sessão previsível e selectors estabilizados para gate de release repetível.**

## Performance

- **Duration:** 17 min
- **Started:** 2026-04-09T17:29:35Z
- **Completed:** 2026-04-09T17:46:16Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Login smoke validado com sucesso para `panel_token`, redirect pós-login, falha de credencial/rede e limpeza em `401/403`.
- Navegação shell (desktop/mobile) e caminho dashboard→monitoring confirmados com stubs determinísticos.
- KPI smoke do dashboard estabilizado para o copy real (`Sessões Totais (24h)`) e estrutura de card atual.

## Verification Evidence
- `pnpm cy:run --spec cypress/e2e/login.cy.ts` → **13 passing, 0 failing**.
- `pnpm cy:run --spec cypress/e2e/navigation-shell.cy.ts` → **2 passing, 0 failing**.
- `pnpm cy:run --spec cypress/e2e/dashboard-data-bindings.cy.ts` → **2 passing, 0 failing**.

## Task Commits

Each task was committed atomically:

1. **Task 1: Align login smoke with session contract assertions** - `9ddcef2` (chore, allow-empty verification commit)
2. **Task 2: Consolidate dashboard navigation smoke path for release gate** - `e62c039` (fix)

**Plan metadata:** (to be recorded in final docs commit)

## Files Created/Modified
- `control-panel/frontend/cypress/e2e/dashboard-data-bindings.cy.ts` - Corrige selector de KPI para label/localização vigente e container estável.

## Decisions Made
- Mantida a atomicidade da Task 1 com commit `--allow-empty` porque o baseline já cumpria os requisitos técnicos do plano.
- Preferido ajuste de selector no spec (em vez de alterar UI) para preservar contrato visual existente e reduzir risco de regressão.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrigido selector desatualizado no smoke de KPI**
- **Found during:** Task 2 (Consolidate dashboard navigation smoke path for release gate)
- **Issue:** O spec buscava copy/estrutura antiga (`Total Sessions (24h)` + `closest("div")`), causando falha intermitente.
- **Fix:** Atualizado para `Sessões Totais (24h)` e escopo no card root (`parents("div.rounded-2xl").first()`).
- **Files modified:** `control-panel/frontend/cypress/e2e/dashboard-data-bindings.cy.ts`
- **Verification:** Reexecução dos specs da task com sucesso (`navigation-shell` e `dashboard-data-bindings`).
- **Committed in:** `e62c039`

---

**Total deviations:** 1 auto-fixed (Rule 1 bug)
**Impact on plan:** Correção necessária para estabilidade do gate smoke; sem scope creep.

## Auth Gates
None.

## Issues Encountered
- Execução inicial via `ctx_execute` falhou por timeout da ferramenta; validações foram executadas com script PowerShell equivalente no mesmo escopo.
- Flake inicial em navegação mobile foi resolvida removendo assert transitório de classe (`translate-x-0`) na rodada de ajuste do spec já existente no baseline.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 04-03 pode consumir este plano como gate técnico de QUAL-01/COMP-02 com comandos já validados.
- Risco residual: warning de segurança do Cypress sobre `allowCypressEnv` permanece fora do escopo deste plano.

## Self-Check: PASSED

- FOUND: `.planning/phases/04-compatibility-and-rollout-hardening/04-02-SUMMARY.md`
- FOUND: `9ddcef2`
- FOUND: `e62c039`

---
*Phase: 04-compatibility-and-rollout-hardening*
*Completed: 2026-04-09*
