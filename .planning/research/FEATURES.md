# Feature Research

**Domain:** Brownfield local-first AI agent orchestration platform (ClawDevs AI)
**Researched:** 2026-04-07
**Confidence:** MEDIUM

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Deterministic local stack lifecycle (`up`, `down`, health checks) | Local-first orchestration is unusable if bootstrap is brittle | MEDIUM | Existing Makefile/scripts are present; risk is operational coupling and cascading startup failures. |
| Auth + secure configuration baseline (JWT, admin auth, secret injection) | Any control plane managing agent execution needs access control and safe defaults | MEDIUM | Auth exists; active gap is secret hardening and policy-safe defaults. Risk: insecure env drift. |
| Agent/session/task control plane (create, run, inspect, retry) | Users expect one place to operate agent work, not ad-hoc CLI state | MEDIUM | Route/API surface exists (`agents`, `sessions`, `tasks`, `chat`); risk is cross-service runtime complexity. |
| Health/metrics/monitoring dashboards with realtime updates | Operators expect fast diagnosis for local multi-service stacks | MEDIUM | Monitoring and WS exist; active gap is SLO-oriented signal quality and alert discipline. |
| Memory and retrieval controls (memory lifecycle + RAG hooks) | Persistent context is expected in modern agent platforms | HIGH | Memory and RAG modules exist; risk is lifecycle/index consistency across sync jobs. |
| Approval/audit checkpoints for sensitive actions | Agent orchestration needs human oversight when actions are high impact | MEDIUM | Approvals/governance APIs exist; risk is policy drift if approvals are bypassed by config. |
| Frontend reliability for critical workflows | Control-plane UX regressions directly block operations | MEDIUM | Current concern: frontend E2E is narrower than feature surface; expand beyond login/chat. |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Context-mode telemetry + optimization loop | Makes token/context efficiency observable and tunable in day-to-day operations | HIGH | `context_mode*`, metrics broadcaster, and semantic optimization hooks create measurable cost/perf leverage. |
| SDD-native workflow in platform (`sdd` routes + templates) | Bakes specification-first delivery into operational tooling, not separate docs | MEDIUM | Strong fit with current repo workflow; risk is adoption friction if UX is not streamlined. |
| Policy-aware execution control (parallelism gates + governance engine) | Enables safer autonomy: higher throughput without losing control | HIGH | Uses `parallelism_gate`, governance services, and permissions; risk is policy complexity explosion. |
| Local sovereignty by default (no cloud dependency in primary path) | Differentiates for teams needing privacy, offline tolerance, and infra control | MEDIUM | Aligns with PROJECT core value; risk is slower adoption of cloud-only capabilities. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Full multi-tenant SaaS control plane now | Looks scalable/commercially attractive | Conflicts with current local-first architecture and adds auth/isolation/billing complexity too early | Keep single-tenant/local-first core; design tenancy seams first, implement later if needed |
| Native mobile app for control operations | Perceived convenience for operators | Splits focus from critical web workflows and increases QA matrix | Responsive web control panel + notification hooks |
| Broad cloud provider abstraction as default path | Teams want optional vendor flexibility | Increases integration surface and operational drift; weakens local-first core value | Maintain local runtime default; add optional connectors behind explicit adapters |
| Fully autonomous execution without approvals | Promises speed | Raises risk for destructive actions and weakens governance guarantees | Keep human-in-the-loop approval tiers with policy-based auto-approve only for low-risk actions |

## Feature Dependencies

```
[Local Stack Lifecycle]
    └──requires──> [Auth + Secure Config]
                        └──requires──> [Agent/Session/Task Control Plane]
                                             ├──requires──> [Memory + RAG Controls]
                                             └──requires──> [Monitoring + Realtime Signals]

[Approval/Audit Checkpoints] ──requires──> [Auth + Secure Config]
[Policy-Aware Execution Control] ──enhances──> [Approval/Audit Checkpoints]
[Context-Mode Optimization] ──enhances──> [Agent/Session/Task Control Plane]
[Full Multi-tenant SaaS] ──conflicts──> [Local Sovereignty by Default]
```

### Dependency Notes

- **Local lifecycle requires secure config first:** unstable or insecure startup invalidates all higher-level features.
- **Control plane requires auth:** session/task/agent operations must be identity-bound for safety and auditability.
- **Memory requires stable session/task primitives:** retrieval quality drops when conversation/task state is inconsistent.
- **Policy-aware execution enhances approvals:** policy engines reduce manual load while preserving governance boundaries.
- **Multi-tenant SaaS conflicts with local-first default:** both can coexist long-term, but not as simultaneous near-term priorities.

## MVP Definition

### Launch With (v1)

Minimum viable product for this brownfield milestone: reliable local operations plus safety/reliability closure.

- [ ] Secure-by-default local operation (secret hardening + safe execution policies)
- [ ] Stable agent/session/task/chat operations through one web control plane
- [ ] Monitoring baseline tied to SLO-style health indicators for core services
- [ ] Approval/governance gates on sensitive actions
- [ ] Memory/RAG continuity for operational workflows
- [ ] Frontend regression coverage for critical routes (`agents`, `sessions`, `tasks`, `monitoring`, `settings`)

### Add After Validation (v1.x)

Features to add once core is working and stable.

- [ ] Context optimization recommendations (semantic tuning, compression hints) after baseline metrics are trusted
- [ ] Policy automation expansion (risk-tiered auto-approval for low-risk actions) after governance audit quality is proven
- [ ] Cron optimization/anomaly surfacing once operational telemetry has low noise

### Future Consideration (v2+)

Features to defer until core scope is validated.

- [ ] Optional cloud-provider connectors (adapter-based, not default path)
- [ ] Multi-node/cluster-wide orchestration depth beyond current local stack assumptions
- [ ] Multi-tenant SaaS controls only after tenancy boundaries are explicitly designed and tested

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Secure-by-default auth/config hardening | HIGH | MEDIUM | P1 |
| Agent/session/task/chat control plane stability | HIGH | MEDIUM | P1 |
| SLO-oriented monitoring and realtime health signals | HIGH | MEDIUM | P1 |
| Memory/RAG operational continuity | HIGH | HIGH | P1 |
| Frontend critical-path regression coverage | HIGH | MEDIUM | P1 |
| Context-mode optimization loop | MEDIUM | HIGH | P2 |
| Policy-aware execution automation | MEDIUM | HIGH | P2 |
| Optional cloud connectors | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

Brownfield note: this pass is intentionally product-internal and scope-driven. External competitor comparison was not the primary input.

| Feature | Competitor A | Competitor B | Our Approach |
|---------|--------------|--------------|--------------|
| Local-first default operations | Not assessed in this pass | Not assessed in this pass | Keep as core value and roadmap anchor |
| Governance + approvals in orchestration | Not assessed in this pass | Not assessed in this pass | Treat as table stakes for safe autonomy |
| Context efficiency observability | Not assessed in this pass | Not assessed in this pass | Position as primary differentiator |

## Sources

- `.planning/PROJECT.md` (core value, validated/active requirements, out-of-scope boundaries)
- `.planning/codebase/ARCHITECTURE.md` (component and route/service architecture)
- `.planning/codebase/CONCERNS.md` (risk hotspots and active operational concerns)
- `README.md` (stack operation model and constraints)
- Route/module inventory from `control-panel/backend/app/api`, `control-panel/backend/app/services`, `control-panel/frontend/src/app`

---
*Feature research for: brownfield local-first AI agent orchestration platform*
*Researched: 2026-04-07*
