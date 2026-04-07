# Pitfalls Research

**Domain:** Brownfield local-first AI agent orchestration platform (ClawDevs AI)  
**Researched:** 2026-04-07  
**Confidence:** HIGH (repo-specific evidence), MEDIUM (scale thresholds/inferred growth behavior)

## Critical Pitfalls

### Pitfall 1: Script-Orchestrated Startup Cascade Failures

**Risk type:** Ops Risk  
**Impact:** High  
**Likelihood:** High  
**Priority:** P0

**Symptom:**  
Intermittent stack boot failures, panel endpoints partially available, worker jobs stalled, or OpenClaw-dependent flows degraded after restart.

**Root cause:**  
Service bring-up is imperative/script-driven with strict order dependencies (DB/Redis/backend/token-init/openclaw), so one degraded dependency can cascade.

**Prevention:**  
Replace ad-hoc ordering with declarative service dependency contracts and explicit readiness gates per integration boundary (backend, token-init, gateway, worker).

**Mitigation (when triggered):**  
Use a deterministic recovery runbook: isolate failing dependency, reset only impacted services/volumes, re-run ordered health gates, and block UI features tied to unhealthy dependencies.

**Warning signs:**  
Frequent manual restarts, flaky `wait_for_health` behavior, and recurring "works after second run" incidents.

**Phase to address:**  
Phase 1 - Operational Coupling Reduction and Startup Contract Hardening

---

### Pitfall 2: Silent Schema Drift from Auto-Migration + Fallback Schema Creation

**Risk type:** Technical Debt  
**Impact:** High  
**Likelihood:** Medium  
**Priority:** P0

**Symptom:**  
Environment-specific DB behavior, migration surprises in shared environments, or runtime errors after deployment despite local success.

**Root cause:**  
Automatic migration on backend startup plus `allow_schema_create_all_fallback` pathways can hide migration hygiene issues and create non-reproducible schemas.

**Prevention:**  
Enforce migration-only schema changes, disable fallback outside tightly controlled local recovery, and require migration diff checks in CI.

**Mitigation (when triggered):**  
Freeze writes, snapshot DB, diff live schema vs Alembic head, produce corrective migration, and re-run integration tests against restored replicas.

**Warning signs:**  
Unexpected table/column presence across environments, migration history drift, or "fixed by dropping local DB" patterns.

**Phase to address:**  
Phase 2 - Migration Safety Rails and Data Contract Governance

---

### Pitfall 3: Dev Defaults Leaking into Shared or Production-Like Environments

**Risk type:** Ops Risk  
**Impact:** High  
**Likelihood:** Medium  
**Priority:** P0

**Symptom:**  
Shared environments run with placeholder secrets, weak auth posture, or unsafe OpenClaw sandbox settings.

**Root cause:**  
Local-first defaults (`secret_key`, placeholder admin password, `OPENCLAW_SANDBOX_MODE=off`) are convenient for dev but dangerous without strict environment hygiene enforcement.

**Prevention:**  
Introduce startup policy checks that fail fast on default secrets/sandbox policies in non-local environments.

**Mitigation (when triggered):**  
Rotate affected credentials immediately, invalidate issued tokens, force re-auth, and audit recent agent/task activity for misuse.

**Warning signs:**  
`.env.example`-like values detected in running containers, unchanged secret values across environments, or missing policy validation logs.

**Phase to address:**  
Phase 1 - Security Baseline and Environment Policy Enforcement

---

### Pitfall 4: API/WS Contract Drift Hidden by Frontend Rewrites

**Risk type:** Product Risk  
**Impact:** High  
**Likelihood:** Medium  
**Priority:** P1

**Symptom:**  
UI appears reachable but core flows (sessions/tasks/realtime dashboards) fail with auth errors, stale data, or silent reconnect loops.

**Root cause:**  
Next rewrites abstract backend URLs, while WebSocket auth depends on first-frame token semantics; contract drift can escape early detection when only happy-path tests exist.

**Prevention:**  
Define and version API/WS contracts explicitly; add contract tests for rewrite rules, WS channel auth handshake, and payload schema compatibility.

**Mitigation (when triggered):**  
Pin frontend to last known-compatible backend contract, ship compatibility shim for changed fields/events, then roll forward with dual-read/dual-write transition tests.

**Warning signs:**  
Increase in client reconnects, per-channel auth failures, and front-end errors clustered around monitoring/context-mode channels.

**Phase to address:**  
Phase 3 - Integration Contract Stabilization (REST + WS)

---

### Pitfall 5: Observability False Green (Healthy Services, Broken User Outcomes)

**Risk type:** Ops Risk  
**Impact:** High  
**Likelihood:** Medium  
**Priority:** P1

**Symptom:**  
Containers show healthy, but users report failed orchestration actions, stuck approvals, or degraded agent workflows.

**Root cause:**  
Current health/broadcasting signals emphasize component liveness, while end-to-end SLO signals and alerting/escalation guarantees are externalized and inconsistent.

**Prevention:**  
Define SLOs for user-critical flows (session creation, task execution, WS freshness, OpenClaw round-trip latency) and alert from outcome metrics, not just liveness.

**Mitigation (when triggered):**  
Trigger degraded mode (disable non-critical automations), route to manual approval fallback, and use trace correlation across backend/worker/OpenClaw to isolate bottlenecks.

**Warning signs:**  
Healthy endpoints with increasing support incidents, rising queue latency, or more normalized 500s without actionable context.

**Phase to address:**  
Phase 4 - SLO-Centered Observability and Incident Playbooks

---

### Pitfall 6: Frontend Regression Escape in High-Surface Realtime UX

**Risk type:** Product Risk  
**Impact:** Medium-High  
**Likelihood:** High  
**Priority:** P1

**Symptom:**  
Monitoring/context-mode UI regressions ship undetected; login/chat pass but operational pages malfunction in real usage.

**Root cause:**  
Frontend test footprint is narrow (few E2E specs) relative to page/channel surface and lacks broad component-level coverage.

**Prevention:**  
Expand deterministic E2E for realtime channels and add focused component tests for high-change UI modules.

**Mitigation (when triggered):**  
Hotfix with feature flags to disable broken UX slices, backport stable rendering/data adapters, and enforce release gate on newly added critical path tests.

**Warning signs:**  
Frequent UI-only bugfixes after release, broken dashboards despite green CI, and manual QA dependence for core flows.

**Phase to address:**  
Phase 5 - Frontend Reliability Expansion (Realtime + Monitoring)

---

### Pitfall 7: Multi-Ecosystem Dependency Drift Causing Cross-Container Incompatibility

**Risk type:** Technical Debt  
**Impact:** Medium-High  
**Likelihood:** High  
**Priority:** P1

**Symptom:**  
After routine upgrades, one or more containers fail contract assumptions (API shape, package runtime behavior, build/tool mismatch).

**Root cause:**  
Fast-moving stack segments (Next/React/FastAPI/SQLAlchemy/Redis/Ollama/OpenClaw images) evolve at different cadences without a unified compatibility matrix.

**Prevention:**  
Adopt pinned version bands, scheduled upgrade windows, and compatibility CI matrix spanning frontend/backend/worker/OpenClaw boundaries.

**Mitigation (when triggered):**  
Rollback to last validated version set, isolate breaking dependency via bisect upgrade path, and release with compatibility notes plus migration guard tests.

**Warning signs:**  
Frequent "minor update" breakage, divergent lockfiles/images between contributors, and increased emergency pinning.

**Phase to address:**  
Phase 6 - Dependency Governance and Compatibility Matrix

---

## Prioritized Risk Register

| Pitfall | Type | Impact | Likelihood | Priority |
|---------|------|--------|------------|----------|
| Script-orchestrated startup cascades | Ops | High | High | P0 |
| Silent schema drift from migration fallback | Technical Debt | High | Medium | P0 |
| Dev defaults leaking into shared envs | Ops | High | Medium | P0 |
| API/WS contract drift behind rewrites | Product | High | Medium | P1 |
| Observability false green | Ops | High | Medium | P1 |
| Frontend regression escape | Product | Medium-High | High | P1 |
| Cross-container dependency drift | Technical Debt | Medium-High | High | P1 |

## Technical Debt Patterns

Shortcuts that look efficient now but compound maintenance risk.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Keeping orchestration logic in imperative shell scripts only | Fast edits, low initial overhead | Fragile startup ordering and opaque failure paths | MVP/local experiments only; not for shared env hardening |
| Allowing schema fallback to mask migration errors | Developer velocity during local recovery | Hidden schema divergence and unsafe rollout assumptions | Only in isolated local rescue scenarios |
| Relying on rewrite abstraction without contract tests | Cleaner frontend URLs | Broken integrations discovered late | Never acceptable for core WS/API channels |
| Treating liveness checks as production readiness | Easy "green" dashboards | User-impacting failures pass unnoticed | Never acceptable after first multi-user rollout |
| Deferring frontend realtime test expansion | Lower short-term test maintenance | High regressions on operational UI | Only while features are explicitly marked experimental |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Frontend rewrites -> backend API | Assuming rewrite success means contract compatibility | Add versioned contract tests for rewritten endpoints and payload shapes |
| Frontend WS channels -> backend | Sending auth in query/header instead of first frame semantics | Enforce handshake tests and channel auth conformance in CI |
| Backend -> OpenClaw gateway | Treating gateway as always-ready dependency | Add readiness circuit breaker and graceful degradation for gateway-dependent features |
| Backend/OpenClaw -> Ollama | Hard-coding model/runtime assumptions | Validate model availability and latency thresholds at startup + runtime |
| Token bootstrap volume sharing | Assuming token volume always fresh/synchronized | Add token freshness checks and deterministic rotation procedure |
| Worker -> DB/Redis/OpenClaw data volume | Ignoring partial dependency degradation | Implement worker startup guards and per-dependency backoff/alerting |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| WS fanout without channel-level backpressure | UI lag, reconnect storms, delayed metrics | Add per-channel buffering limits and dropped-message telemetry | Usually visible as concurrent operators/channels grow (10+ active dashboards) |
| LLM-dependent flows coupled to synchronous UX paths | Long task latency, blocked interactions | Decouple long-running orchestration from immediate UI response paths | Becomes acute when model latency spikes or inference queue increases |
| Startup health checks that only validate liveness | Fast boot marked healthy but workflows fail | Verify capability checks (token present, gateway reachable, migrations clean) | Surfaces under partial outages and rolling restarts |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Shipping with default secrets/placeholders | Account compromise and unauthorized control | Enforce non-default secret policy at startup for non-local profiles |
| Running OpenClaw with unsafe sandbox assumptions in shared envs | Unbounded agent execution risk | Gate sandbox mode by environment policy with deny-by-default in shared tiers |
| Storing long-lived panel tokens without rotation discipline | Persistent blast radius after token leak | Rotate tokens on schedule, scope permissions, and detect stale token usage |
| Blurring panel JWT and gateway token boundaries | Privilege escalation or cross-service misuse | Keep strict credential separation and explicit least-privilege mapping |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Health UI reports green while orchestration actions fail | Operator distrust and delayed response | Show flow-level health states tied to user outcomes, not only container status |
| Realtime dashboard silently reconnects without surfacing auth/contract errors | Hidden incident escalation | Expose channel-level error state and guided operator remediation |
| Feature-flagged behavior changes without UI affordances | Confusing, inconsistent behavior | Surface active flag state and compatibility notices in admin/monitoring views |

## "Looks Done But Isn't" Checklist

- [ ] **Startup Hardening:** Boot sequence verified under dependency failure injection (not only happy path).
- [ ] **Migration Safety:** Migration-only schema evolution enforced; fallback schema creation blocked outside local rescue mode.
- [ ] **Security Baseline:** Default secrets and unsafe sandbox settings fail startup in shared/prod-like profiles.
- [ ] **Contract Reliability:** REST rewrite and WS handshake contracts tested across frontend/backend versions.
- [ ] **Observability:** SLO alerts wired to user outcomes (task/session/approval success), not just service liveness.
- [ ] **Frontend Confidence:** Realtime monitoring/context-mode critical paths covered by deterministic E2E tests.
- [ ] **Upgrade Governance:** Compatibility matrix and rollback playbook validated before routine dependency upgrades.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Startup cascade failure | MEDIUM | Isolate failed dependency -> restart minimal affected set -> rerun readiness chain -> enable degraded mode until stable |
| Schema drift incident | HIGH | Stop writes -> snapshot/restore -> reconcile with migration head -> run targeted data validation + integration tests |
| Secret/sandbox misconfiguration | HIGH | Rotate credentials -> revoke active tokens -> enforce policy checks -> run security incident review |
| API/WS contract break | MEDIUM-HIGH | Re-pin compatible versions -> deploy shim/adapter -> add failing contract test before forward fix |
| Observability false green | MEDIUM | Add temporary synthetic checks + alert routes -> instrument missing flow metrics -> validate incident response loop |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Script-orchestrated startup cascades | Phase 1 - Operational Coupling Reduction | Chaos-style startup tests with controlled dependency failures pass consistently |
| Silent schema drift | Phase 2 - Migration Safety Rails | CI blocks fallback schema creation and validates migration head parity |
| Default secret/sandbox leakage | Phase 1 - Security Baseline Enforcement | Non-local startup fails with default credentials or unsafe sandbox policy |
| REST/WS contract drift | Phase 3 - Contract Stabilization | Contract suite passes for rewrite routes, WS auth first-frame, and payload versions |
| Observability false green | Phase 4 - SLO Observability | Alerting catches synthetic user-flow failures even when container liveness is green |
| Frontend realtime regression escape | Phase 5 - Frontend Reliability Expansion | Critical monitoring/context-mode E2E suite gates releases |
| Dependency drift | Phase 6 - Compatibility Governance | Upgrade pipeline runs matrix tests and documented rollback path |

## Sources

- `.planning/PROJECT.md` (constraints, active requirements, key decisions)
- `.planning/codebase/CONCERNS.md` (security, coupling, migration, observability, dependency risks)
- `.planning/codebase/TESTING.md` (coverage gaps, E2E scope, validation practices)
- `.planning/codebase/INTEGRATIONS.md` (API/WS contracts, token bootstrap, OpenClaw/Ollama/worker integrations)

---
*Pitfalls research for: brownfield local-first AI orchestration platform*  
*Researched: 2026-04-07*
