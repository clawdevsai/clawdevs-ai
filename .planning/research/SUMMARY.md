# Project Research Summary

**Project:** ClawDevs AI
**Domain:** Brownfield local-first AI agent orchestration platform
**Researched:** 2026-04-07
**Confidence:** MEDIUM

## Executive Summary

ClawDevs AI is a self-hosted control plane for operating AI agents end-to-end with governance, monitoring, and local runtime control. The research converges on a brownfield-safe strategy: keep the existing FastAPI + Next.js + Docker architecture, then harden it in phases instead of introducing a large platform rewrite.

The recommended build path is reliability-first: secure environment policy enforcement, deterministic startup behavior, strict API/WS contract boundaries, and outcome-based observability. This aligns with current validated requirements (working local stack, operational panel, backend APIs, broad backend tests) while directly closing active gaps (secret hardening, frontend critical-path test coverage, SLO-grade monitoring, and reduced script coupling).

The main risks are known and front-loaded: startup cascade failures, schema drift, unsafe defaults in shared environments, contract drift hidden by rewrites, and false-green monitoring. The mitigation is explicit phase ordering with hard gates at each layer before adding optimization features.

## Key Findings

### Recommended Stack

Research strongly recommends retaining the current core stack and focusing on controlled adjustments. This minimizes regression risk and respects project constraints around local/self-hosted operation.

**Core technologies:**
- FastAPI `0.135.1` + Uvicorn `0.34.0`: control-plane API and WS backbone; already production-shaped in this codebase.
- Python `3.12` + SQLModel `0.0.37` + Alembic `1.18.4`: stable backend runtime and migration flow.
- Next.js `16.2.0` + React `19.2.4` + TypeScript `5.8.3`: modern panel UI with App Router and existing route surface.
- PostgreSQL `18` + Redis `8` + RQ `2.6.0`/`rq-scheduler 0.14.0`: right complexity level for durable state + async orchestration.
- Docker-first local topology: core product value and operational baseline.

**Critical stack adjustments:**
- Pin mutable image tags (`latest`) to versions/digests.
- Enforce one backend lockfile authority (`uv.lock`) in CI.
- Roll out Argon2 hashing with dual-verify migration, not big-bang cutover.
- Keep Node runtime aligned to Next.js 16 constraints (Node 20+).

### Expected Features

**Must have (table stakes):**
- Deterministic local lifecycle (`up/down/health`) with reliable dependency gating.
- Auth and secure configuration defaults.
- Unified agent/session/task control plane with retry/inspect flows.
- Realtime monitoring with SLO-aligned indicators.
- Memory/RAG continuity controls.
- Approval and audit gates for sensitive actions.
- Frontend reliability for core operator routes.

**Should have (competitive):**
- Context-mode telemetry and optimization loop.
- Policy-aware execution control with governance-aware parallelism.
- SDD-native workflow integration in platform UX.
- Local sovereignty as default operating model.

**Defer (v2+):**
- Full multi-tenant SaaS controls.
- Native mobile control app.
- Broad cloud-provider abstraction as default path.
- Multi-node/cluster depth beyond current local profile.

### Architecture Approach

Adopt incremental boundary hardening, not structural rewrite: keep existing topology, then formalize `integrations/`, `bootstrap/`, and frontend `contracts/` seams. Follow three patterns: health-gated bootstrap chain, anti-corruption adapters for external I/O, and idempotent async jobs with stable job IDs and bounded retries.

**Major components:**
1. Panel Frontend (Next.js): operator workflows, dashboards, realtime status.
2. Panel Backend (FastAPI): auth, orchestration APIs, WS channels, service coordination.
3. Worker (RQ): async orchestration and periodic sync jobs.
4. Runtime services: OpenClaw gateway + Ollama for agent execution/inference.
5. Data plane: PostgreSQL (durable state) + Redis (queue/transient state).

### Critical Pitfalls

1. **Startup cascade failures**: prevent with explicit dependency graph, bounded waits, and failure-domain isolation.
2. **Schema drift from migration fallback**: block fallback schema creation in CI and enforce migration-head parity.
3. **Dev defaults leaking to shared environments**: fail startup on default secrets/unsafe sandbox policy outside local.
4. **REST/WS contract drift behind rewrites**: add versioned contracts and compatibility tests for rewrite + first-frame WS auth.
5. **Observability false green**: alert on user-flow SLOs, not only container liveness.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Security Baseline and Startup Hardening
**Rationale:** Every higher-level feature depends on secure and deterministic boot behavior.
**Delivers:** Environment policy checks, secret hardening gates, safer startup dependency checks, reduced startup blast radius.
**Addresses:** Secure config baseline, deterministic lifecycle, governance safety.
**Avoids:** Dev-default leakage, startup cascade failures.

### Phase 2: Migration and Runtime Safety Rails
**Rationale:** Database and queue correctness must be stable before contract expansion.
**Delivers:** Migration-head CI checks, fallback-schema prevention, queue reliability metrics, idempotent retry guarantees.
**Uses:** SQLModel/Alembic, Redis/RQ.
**Implements:** Lifespan decomposition and async job hardening.
**Avoids:** Silent schema drift, queue contention regressions.

### Phase 3: Integration Contract Stabilization (REST + WS)
**Rationale:** API and WS contract consistency is the core dependency for frontend reliability and safe evolution.
**Delivers:** Canonical API namespace, contract schemas/tests, WS handshake compatibility checks, adapterized integration boundaries.
**Uses:** FastAPI + Next.js contracts layer.
**Implements:** Anti-corruption adapters and boundary validation.
**Avoids:** Contract drift and silent UI breakage.

### Phase 4: SLO-Centered Observability and Degraded Mode
**Rationale:** Operations need outcome-level signal quality before optimization features.
**Delivers:** SLO definitions for critical flows, incident playbooks, degraded-mode UX states, traceable cross-service diagnostics.
**Addresses:** Monitoring baseline and operational readiness.
**Avoids:** False-green dashboards.

### Phase 5: Frontend Critical-Path Reliability Expansion
**Rationale:** Core routes are broad and realtime-heavy; test depth must match product surface.
**Delivers:** E2E coverage for `agents/sessions/tasks/monitoring/settings`, WS/reconnect scenarios, release gates.
**Addresses:** Frontend reliability requirement.
**Avoids:** Regression escape in operator-critical UX.

### Phase 6: Dependency Compatibility Governance
**Rationale:** After stabilization, prevent reintroducing drift via unmanaged upgrades.
**Delivers:** Version pin policy, upgrade cadence, matrix validation for Node/Python/container dependencies, rollback playbooks.
**Uses:** Existing Docker + package management pipeline.
**Implements:** Ongoing compatibility controls.
**Avoids:** Cross-container dependency drift.

### Phase Ordering Rationale

- Security/startup reliability is a prerequisite for all control-plane features.
- Data/migration correctness must precede API/WS contract locking.
- Contract stabilization must precede frontend test expansion to avoid brittle tests on moving interfaces.
- SLO observability should be in place before deeper optimization and compatibility automation.
- Final governance phase keeps the stabilized system from regressing.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3:** WS handshake/versioning and rewrite-compatibility strategy can be subtle under mixed route history.
- **Phase 4:** SLO threshold design and signal-to-noise tuning need system-specific calibration.
- **Phase 6:** Upgrade matrix and rollback policy should be validated against real release cadence.

Phases with standard patterns (skip research-phase):
- **Phase 1:** Secret-policy checks and fail-fast environment validation are well-established.
- **Phase 2:** Migration safety rails and idempotent job design are standard operational patterns.
- **Phase 5:** Critical-path E2E expansion follows known Cypress/Playwright reliability practices.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Strong repo evidence plus official compatibility docs and explicit versions. |
| Features | MEDIUM | Strong internal alignment; weaker external competitor benchmarking in this pass. |
| Architecture | HIGH | Clear current topology and bounded evolution path; low ambiguity in core seams. |
| Pitfalls | MEDIUM-HIGH | Risks are concrete and phase-mapped, but some scale behavior is inferred. |

**Overall confidence:** MEDIUM

### Gaps to Address

- Quantitative SLO thresholds for core flows are not yet specified; define baselines before alert hardening.
- Exact WS payload/version migration contract is not fully codified; lock schema versioning rules in Phase 3.
- Long-term multi-tenant design is intentionally deferred; keep explicit seam assumptions to avoid future rework.
- Competitor benchmarking depth is limited; run targeted market comparison only if go-to-market scope broadens.

## Sources

### Primary (HIGH confidence)
- `.planning/PROJECT.md` (product scope, constraints, active requirements, key decisions)
- `.planning/research/STACK.md`
- `.planning/research/FEATURES.md`
- `.planning/research/ARCHITECTURE.md`
- `.planning/research/PITFALLS.md`
- `.planning/codebase/ARCHITECTURE.md`
- `.planning/codebase/CONCERNS.md`
- `.planning/codebase/INTEGRATIONS.md`
- `.planning/codebase/TESTING.md`
- `README.md`, `Makefile`, backend/frontend manifests and Docker definitions

### Secondary (MEDIUM confidence)
- Next.js docs (installation and v16 upgrade compatibility)
- FastAPI security tutorial (`pwdlib[argon2]` guidance)
- Docker docs (image pinning best practices, Compose lifecycle)
- OpenTelemetry Python docs (phased observability instrumentation)

### Tertiary (LOW confidence)
- Broader competitor feature comparisons (explicitly limited in this research pass)

---
*Research completed: 2026-04-07*
*Ready for roadmap: yes*
