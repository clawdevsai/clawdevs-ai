# Phase 4: Compatibility and Rollout Hardening - Context

**Gathered:** 2026-04-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Garantir que a migração visual para o padrão Mosaic preserve comportamento funcional existente, sem regressão de autenticação/sessão, e com evidência clara de prontidão para release.

Foco desta fase:
- compatibilidade por rota e navegação
- estabilidade de auth/sessão do ponto de vista do usuário
- cobertura smoke Cypress para login + dashboard navigation
- checklist final de release readiness

Fora de escopo:
- novas funcionalidades de produto
- mudanças de contrato de API backend

</domain>

<decisions>
## Implementation Decisions

### Matriz de compatibilidade por rota
- **D-01:** Adotar matriz em dois níveis.
- **D-02:** **Tier A (must-pass com interação):** `/login`, `/`, `/monitoring`, `/chat`, `/sessions`, `/tasks`.
- **D-03:** **Tier B (render + navegação):** `/approvals`, `/agents`, `/settings`, `/cluster`, `/crons`, `/sdd`, `/memory`.

### Auth e sessão
- **D-04:** Validar fluxo auth/sessão com E2E determinístico via intercepts.
- **D-05:** Cobrir explicitamente:
  - login com sucesso (`panel_token` salvo + redirect para `/`)
  - login com falha
  - `401/403` limpando token e redirecionando para `/login`
  - envio de `Authorization: Bearer <token>` após login.

### Release readiness
- **D-06:** Gate de saída obrigatório com:
  - `pnpm typecheck`
  - `pnpm build`
  - `pnpm cy:run --spec cypress/e2e/login.cy.ts`
  - `pnpm cy:run --spec cypress/e2e/navigation-shell.cy.ts`
  - `pnpm cy:run --spec cypress/e2e/dashboard-data-bindings.cy.ts`
- **D-07:** Incluir checklist manual curto (login, dashboard, monitoring) como parte da validação final.

### the agent's Discretion
- Profundidade exata das asserções por rota dentro de cada tier.
- Estrutura final dos specs (um consolidado vs ajustes incrementais), desde que os gates D-06 sejam atendidos.
- Dados de fixtures e stubs específicos para reduzir flake mantendo rastreabilidade aos requisitos.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Planejamento e requisitos
- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/PROJECT.md`
- `.planning/STATE.md`

### Auth/sessão e navegação
- `control-panel/frontend/src/app/login/page.tsx`
- `control-panel/frontend/src/lib/axios-instance.ts`
- `control-panel/frontend/src/components/layout/app-layout.tsx`
- `control-panel/frontend/src/components/layout/header.tsx`
- `control-panel/frontend/src/components/layout/sidebar.tsx`

### Testes E2E existentes (base para fase 4)
- `control-panel/frontend/cypress/e2e/login.cy.ts`
- `control-panel/frontend/cypress/e2e/navigation-shell.cy.ts`
- `control-panel/frontend/cypress/e2e/dashboard-data-bindings.cy.ts`
- `control-panel/frontend/cypress/support/commands.ts`
- `control-panel/frontend/cypress.config.ts`

</canonical_refs>

<specifics>
## User-Specific Preferences

- Preferência por validação pragmática com evidência executável.
- Manter foco em preservação de comportamento existente, sem expansão de escopo.
- Critério de pronto baseado em gates objetivos + checklist manual curto.

</specifics>
