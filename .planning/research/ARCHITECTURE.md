# Architecture Research

**Domain:** Brownfield local-first AI agent orchestration platform (ClawDevs AI)
**Researched:** 2026-04-07
**Confidence:** HIGH (baseline), MEDIUM-HIGH (evolution path)

## Standard Architecture

### System Overview (Current Baseline)

The current system is a local multi-container architecture split into two planes:
- Control plane: Next.js frontend + FastAPI backend + RQ worker.
- Runtime plane: OpenClaw gateway + agent runtime + Ollama + search services.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Experience Layer                                                            │
│  Browser UI                                                                 │
│    -> Next.js Panel Frontend (3000)                                         │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                v
┌──────────────────────────────────────────────────────────────────────────────┐
│ Control API Layer                                                           │
│  FastAPI Backend (8000): auth, agents, sessions, tasks, metrics, ws         │
│  WS channels: dashboard, agents, approvals, cluster, crons, context-mode    │
└───────────────┬───────────────────────────────────────┬──────────────────────┘
                │                                       │
                v                                       v
┌──────────────────────────────────────┐    ┌──────────────────────────────────┐
│ Orchestration & Async Layer          │    │ Runtime Gateway Layer            │
│  RQ Worker + rq-scheduler            │    │  OpenClaw Gateway (18789)        │
│  periodic sync + task orchestration  │    │  agent sessions + tool execution │
└───────────────┬──────────────────────┘    └───────────────┬──────────────────┘
                │                                           │
                v                                           v
┌──────────────────────────────────────────────────────────────────────────────┐
│ Data/State Layer                                                            │
│  PostgreSQL (state), Redis (queue/cache), openclaw-data volume, panel-token │
│  ollama-data volume, postgres-data volume                                   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Baseline Startup Topology

`make up-all` currently starts services in this order:
1. `postgres`
2. `redis`
3. `ollama`
4. `searxng`
5. `panel-backend`
6. `token-init` (waits for backend health and writes shared token volume)
7. `searxng-proxy`
8. `panel-worker`
9. `panel-frontend`
10. `openclaw` (started by `run-openclaw.sh` after `up-all.sh`)

Backend startup (`lifespan`) runs:
1. DB migrations
2. admin bootstrap
3. agent bootstrap/sync
4. health monitor loop (feature-flagged)
5. context-mode metrics broadcaster

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Panel Frontend | Operator UX, dashboards, chat UI, settings | Next.js App Router + React Query + Axios + WS manager |
| Panel Backend | Auth, API/WS, orchestration coordination, monitoring endpoints | FastAPI + SQLModel + service modules |
| Panel Worker | Async workflows, periodic sync loops, queue processing | RQ worker + rq-scheduler |
| OpenClaw Gateway | Agent execution runtime and chat completion gateway | Dedicated container + internal token auth |
| Ollama | Local model inference and embeddings | Local runtime container |
| PostgreSQL | Durable app state (users, tasks, sessions, metrics) | Async SQLAlchemy/SQLModel + Alembic |
| Redis | Queue + scheduler state + transient metrics | RQ + Redis client |
| Token Init | Bootstrap panel agent token into shared volume | One-shot container job |

## Recommended Project Structure

This is an incremental structure target, not a rewrite. Keep existing folders and add bounded seams.

```text
control-panel/
├── backend/app/
│   ├── api/                    # HTTP + WebSocket endpoints
│   ├── core/                   # config/auth/db primitives
│   ├── models/                 # SQLModel entities
│   ├── services/               # domain/application services (existing)
│   ├── tasks/                  # queue jobs + periodic sync (existing)
│   ├── integrations/           # NEW: OpenClaw/GitHub/Redis/FS adapters
│   ├── bootstrap/              # NEW: startup actions + readiness gates
│   └── observability/          # NEW: SLO checks, health contracts, emitters
├── frontend/src/
│   ├── app/                    # routes, layouts, route handlers
│   ├── components/             # domain UI + primitives
│   ├── lib/                    # transport clients + monitoring helpers
│   ├── contracts/              # NEW: REST/WS schema contracts (zod/types)
│   └── features/               # NEW: feature modules by domain (optional)
└── scripts/docker/             # stack lifecycle scripts (existing)
```

### Structure Rationale

- **`integrations/` (backend):** isolates external dependency behavior (timeouts, retries, error mapping) from domain logic.
- **`bootstrap/` (backend):** separates lifecycle side effects from API creation so startup risk is controllable.
- **`contracts/` (frontend):** prevents silent API/WS drift by validating payloads close to boundaries.
- **Keep `scripts/docker/` as control entrypoint:** change internals incrementally, preserve existing operator workflow.

## Architectural Patterns

### Pattern 1: Health-Gated Bootstrap Chain (Keep, Then Formalize)

**What:** Ordered service startup with health checks and bounded timeouts.  
**When to use:** Local-first stacks where all dependencies run on one host.  
**Trade-offs:** Simple and explicit, but can become brittle as dependency graph grows.

**Example:**
```bash
# Current style (scripts/docker/up-all.sh)
docker run ... clawdevs-postgres
wait_for_health clawdevs-postgres 180
docker run ... clawdevs-panel-backend
wait_for_health clawdevs-panel-backend 180
docker run ... clawdevs-token-init
wait_for_exit_success clawdevs-token-init 180
```

### Pattern 2: Anti-Corruption Integration Adapters (Adopt Incrementally)

**What:** Concentrate external I/O rules in adapters with typed failure modes.  
**When to use:** OpenClaw/GitHub/Redis/filesystem interactions currently spread across services.  
**Trade-offs:** Adds layer indirection, but sharply reduces blast radius from integration changes.

**Example:**
```python
class GatewayTimeout(Exception): ...
class GatewayAuthError(Exception): ...

class OpenClawGatewayAdapter:
    async def run_turn(self, agent_slug: str, prompt: str) -> str:
        try:
            return await self._client.run_agent_turn(agent_slug, prompt, timeout=30)
        except TimeoutError as exc:
            raise GatewayTimeout(str(exc)) from exc
        except Exception as exc:
            raise GatewayAuthError(str(exc)) from exc
```

### Pattern 3: Idempotent Async Workflow Jobs (Keep and Expand)

**What:** Stable job IDs + bounded retries for long-running orchestration.  
**When to use:** CEO routing pipeline and deterministic task execution loops.  
**Trade-offs:** Strong resilience for transient failures, but requires clear state machine ownership.

**Example:**
```python
queue.enqueue(
    "app.tasks.task_orchestration.process_task_via_ceo",
    str(task_id),
    job_id=f"task-workflow:{task_id}",
    retry=Retry(max=3, interval=[30, 120, 300]),
)
```

## Data Flow

### Request Flow

```text
[Operator Action]
    ↓
[Frontend Page]
    ↓
[API/Proxy Boundary (/api or route handler)]
    ↓
[Backend Handler or OpenClaw Stream Route]
    ↓
[Service/Integration Adapter]
    ↓
[Postgres/Redis/OpenClaw/Ollama]
    ↓
[WS Broadcast + HTTP Response]
```

### State Management

```text
[React Query Cache]
    ↓ (subscribe/render)
[UI Components] ←→ [Mutations + Fetchers] → [/api/* + /ws/*]
    ↓                                            ↓
[Optimistic/derived state]                 [Backend + WS manager]
```

### Key Data Flows

1. **Realtime monitoring flow:** backend metrics + health loops -> WS channels -> dashboard cards/charts.
2. **Task orchestration flow:** GitHub/task creation -> queue enqueue -> CEO routing pipeline -> status/activity events -> UI.
3. **Session sync flow:** OpenClaw filesystem (`openclaw-data`) -> periodic sync jobs -> DB session/memory read models.
4. **Chat stream flow:** frontend `/openclaw/chat/stream` route -> OpenClaw SSE -> tokenized transcript updates in UI.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| OpenClaw Gateway | HTTP API + bearer token | Core runtime dependency; failures impact chat/orchestration paths. |
| Ollama | Internal HTTP endpoint | Model availability and latency directly affect agent response quality. |
| PostgreSQL | Async ORM + migrations | Startup migration currently on API lifespan path. |
| Redis | Queue/scheduler/cache | Worker and backend both depend on availability and keyspace health. |
| GitHub API | HTTP sync pull | Missing token/repo disables sync; should degrade gracefully. |
| SearXNG / Proxy | Internal search service | Supports retrieval/tooling flows in runtime plane. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Frontend ↔ Backend API | REST over `/api` rewrite/proxy | Mixed path conventions (`/metrics/*` vs `/api/health/*`) increase drift risk. |
| Frontend ↔ Backend WS | `/ws/{channel}` + first-frame auth | Good security posture; channel contract versioning still needed. |
| Backend ↔ Worker | Shared DB/Redis + job queue | Retry exists; visibility of stuck jobs needs stronger SLO metrics. |
| Backend/Worker ↔ OpenClaw Data Volume | Filesystem reads (`sessions.json`, `MEMORY.md`) | Tight coupling to runtime file layout; needs contract abstraction. |
| Token-init ↔ OpenClaw | Shared `panel-token` volume | Bootstrap coupling point; stale token handling should be explicit. |

## Failure Domain Map

| Failure Domain | Trigger | Blast Radius | Current Containment | Evolution Priority |
|---------------|---------|--------------|---------------------|-------------------|
| Startup chain | one dependency unhealthy during boot | stack partially up, UI degraded | shell health waits + timeouts | P1 |
| API lifecycle side effects | migration/bootstrap/sync fail in lifespan | backend unavailable or delayed | exception logging, fail-fast | P2 |
| OpenClaw gateway | timeout/auth failure | chat + orchestration + health repair degraded | per-call try/except, some retries | P1 |
| Redis queue | connection/keyspace issues | worker processing stalls, delayed sync | worker startup ping + RQ retry | P2 |
| Filesystem sync coupling | malformed/unreadable runtime files | stale sessions/memory status in panel | error swallowing + periodic retry | P3 |
| Contract drift (REST/WS) | path/payload mismatch frontend/backend | silent UI regressions or auth loops | partial tests + runtime fallback | P1 |

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k users | Current monolithic control plane + local runtime is acceptable; prioritize correctness and observability over decomposition. |
| 1k-100k users | Split heavy background jobs from API lifecycle, add strict adapter boundaries, and enforce API/WS contract tests across releases. |
| 100k+ users | Introduce dedicated orchestration service boundaries, queue partitioning, and multi-node runtime/data strategies; keep local-first mode as profile, not default global topology. |

### Scaling Priorities

1. **First bottleneck:** integration coupling (OpenClaw + filesystem sync + mixed route contracts), not raw DB capacity.
2. **Second bottleneck:** queue and lifecycle contention (worker saturation, Redis scans, startup side effects).

## Anti-Patterns

### Anti-Pattern 1: Mixed API Namespace Strategy

**What people do:** Mix root-prefixed routes (`/metrics`) and `/api/*` routes, then rely on frontend proxy quirks.  
**Why it's wrong:** Route contracts become ambiguous and break silently during refactors.  
**Do this instead:** Define one canonical external namespace and support temporary compatibility aliases with deprecation logs.

### Anti-Pattern 2: Lifespan as Catch-All Orchestrator

**What people do:** Put migration, seed, sync, and monitor startup in one API lifecycle block.  
**Why it's wrong:** Non-critical failures can block API availability and widen startup blast radius.  
**Do this instead:** Keep only hard requirements in API startup; move optional/background initialization behind worker jobs and readiness gates.

### Anti-Pattern 3: Full Keyspace Polling in Health Paths

**What people do:** Use expensive keyspace scans (`KEYS` patterns) in recurring health loops.  
**Why it's wrong:** Polling cost grows with workload and can create self-inflicted latency.  
**Do this instead:** Use incremental/targeted metrics (`SCAN`/counters) and track sync lag explicitly.

## Incremental Evolution Path (Low-Risk)

### Priority 1: Contract Normalization Layer

- Add explicit REST/WS contract tests for current routes before changing behavior.
- Introduce canonical API namespace policy; keep compatibility aliases for existing consumers.
- Clarify frontend boundary ownership (`rewrite` vs route-handler proxy) and remove overlap only after parity tests pass.

### Priority 2: Integration Adapter Boundaries

- Move OpenClaw/GitHub/Redis/filesystem I/O into dedicated adapter modules.
- Standardize timeout/retry/error taxonomy and propagate typed failures.
- Migrate callers one module at a time to avoid broad regressions.

### Priority 3: Startup Risk Decomposition

- Keep migrations and minimal auth bootstrap in API lifespan.
- Shift non-critical sync/monitor initialization to worker-managed or deferred tasks.
- Add `readyz` checks for capability readiness (gateway token, DB reachable, queue healthy).

### Priority 4: Sync and Queue Reliability Hardening

- Replace broad periodic scans with incremental checkpoints where possible.
- Track queue depth, sync lag, and failed-job trend as first-class metrics.
- Add dead-letter handling and replay tooling for failed orchestration jobs.

### Priority 5: Degraded-Mode Operations

- Define per-boundary degraded behaviors (e.g., chat disabled when gateway unhealthy, monitoring read-only on Redis issues).
- Surface degraded states directly in control panel UX and logs.
- Tie alerts to user-flow SLOs instead of container liveness only.

## Sources

- `.planning/PROJECT.md`
- `.planning/codebase/ARCHITECTURE.md`
- `.planning/codebase/STRUCTURE.md`
- `.planning/codebase/INTEGRATIONS.md`
- `.planning/codebase/CONCERNS.md`
- `docs/architecture/overview.md`
- `Makefile`
- `scripts/docker/up-all.sh`
- `scripts/docker/run-openclaw.sh`
- `scripts/docker/generate-panel-token.sh`
- `control-panel/backend/app/main.py`
- `control-panel/backend/app/core/config.py`
- `control-panel/backend/app/core/database.py`
- `control-panel/backend/app/api/ws.py`
- `control-panel/backend/app/api/health.py`
- `control-panel/backend/app/services/openclaw_client.py`
- `control-panel/backend/app/services/health_monitor.py`
- `control-panel/backend/scripts/worker.py`
- `control-panel/backend/app/tasks/periodic_sync.py`
- `control-panel/backend/app/tasks/task_orchestration.py`
- `control-panel/frontend/next.config.ts`
- `control-panel/frontend/src/lib/api-base-url.ts`
- `control-panel/frontend/src/lib/ws.ts`
- `control-panel/frontend/src/app/api/[...slug]/route.ts`
- `control-panel/frontend/src/app/openclaw/chat/stream/route.ts`

---
*Architecture research for: brownfield local-first AI agent orchestration platform*
*Researched: 2026-04-07*
