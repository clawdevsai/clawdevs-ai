# Stack Research

**Domain:** Brownfield local-first AI agent orchestration platform (ClawDevs AI)
**Researched:** 2026-04-07
**Confidence:** HIGH

## Current Baseline (As-Is)

### Core Technologies

| Technology | Version | Purpose | Current Fit |
|------------|---------|---------|-------------|
| FastAPI + Uvicorn | `fastapi==0.135.1`, `uvicorn==0.34.0` | Control-plane HTTP API | Strong fit for async API + typed contracts in existing backend. |
| Python runtime | `>=3.12,<4.0` | Backend and worker runtime | Matches current dependency set and Docker images (`python:3.12-slim`). |
| SQLModel + SQLAlchemy + Alembic | `sqlmodel==0.0.37`, `alembic==1.18.4` | Data modeling and migrations | Already integrated with startup migration flow and PostgreSQL. |
| PostgreSQL | `postgres:18-alpine` image | System of record + relational state | Good local-first default with mature tooling and backup model. |
| Redis + RQ | `redis:8-alpine`, `rq==2.6.0`, `rq-scheduler==0.14.0` | Background jobs and scheduling | Correct complexity level for current orchestration workloads. |
| Next.js + React | `next==16.2.0`, `react==19.2.4` | Control-plane frontend | Modern stack with App Router and good TS ecosystem coverage. |
| Dockerized local stack | Makefile-driven, 10 services | Reproducible local/self-hosted runtime | Core project value proposition; already operational. |

### Supporting Libraries (Current)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| TanStack Query | `5.94.5` | Frontend server-state/cache | Keep as default for API-driven views and polling UX. |
| Orval | `8.5.3` | OpenAPI client generation | Keep for backend/frontend contract sync after API changes. |
| SSE + WebSockets | `sse-starlette==2.3.6` + FastAPI WS | Streaming and realtime updates | Keep mixed model (SSE for streams, WS for bidirectional events). |
| JWT stack | `pyjwt[crypto]`, `passlib[bcrypt]`, `bcrypt` | Panel auth and token verification | Keep short-term; migrate hashing strategy gradually (see adjustments). |

### Development Tools (Current)

| Tool | Purpose | Notes |
|------|---------|-------|
| `uv` | Backend dependency/runtime tool | Already used in Dockerfiles (`uv sync`) and team workflow docs. |
| `pnpm` | Frontend package manager | Locked via `packageManager: pnpm@10.32.1`. |
| Cypress | E2E testing | Already wired into Makefile targets. |
| Makefile + Docker | Local orchestration and lifecycle commands | Existing bootstrap flow must remain stable. |

## Recommended Stack (Brownfield-Safe)

### Keep (No Migration Now)

| Area | Decision | Why |
|------|----------|-----|
| Control plane framework | Keep FastAPI + Next.js | Explicit project constraint and lowest regression path. |
| Queue model | Keep Redis + RQ | RQ is intentionally simple and sufficient for current background jobs. |
| Persistence model | Keep PostgreSQL + Redis split | Aligns with current boundaries and avoids costly data-layer rewrites. |
| Local runtime strategy | Keep Docker-first self-hosted model | Core product value and already validated operationally. |

### Adjust (Justified Changes Only)

| Adjustment | Recommendation | Why Now | Migration / Compatibility Risk |
|------------|----------------|---------|-------------------------------|
| Mutable image tags | Replace `latest` tags (`ollama`, `searxng`, `curlimages/curl`) with pinned version or digest | Docker docs note mutable tags hurt reproducibility and auditability | Low risk technically; medium operational risk if update cadence is not defined. |
| Python lockfile policy | Make `uv.lock` authoritative; either remove `poetry.lock` from active flow or auto-sync it | Runtime/build path already uses `uv`; dual lockfiles drift easily | Medium process risk; low runtime risk if done with CI check. |
| Password hashing baseline | Plan phased move toward `pwdlib[argon2]` for new/rotated hashes while preserving legacy verify path | FastAPI security guidance now recommends Argon2 via `pwdlib` | Medium auth risk if done in-place; must support dual verification during transition. |
| Observability (optional, phased) | Add OpenTelemetry instrumentation behind feature flag for backend + worker traces/metrics/logs | Multi-service orchestration benefits from correlated telemetry | Low initial risk if opt-in; medium complexity if enforced globally too early. |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not (for this milestone) |
|----------|-------------|-------------|-------------------------------|
| Background processing | Redis + RQ | Celery | Higher operational complexity and migration cost without immediate payoff. |
| Vector/retrieval storage | PostgreSQL + pgvector | Dedicated vector DB | Premature split increases ops burden in local-first deployment. |
| Frontend framework | Next.js 16 | Vite + React Router | Would be a full frontend platform migration with little near-term value. |
| Local orchestration | Makefile + Docker | Kubernetes-first local stack | Too heavy for current installability constraints on conventional machines. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Floating container tags in production-like workflows | Non-deterministic rebuilds and weak supply-chain traceability | Pin image tags/digests and rotate intentionally. |
| Concurrent package managers for backend installs (`uv` + `poetry` operationally) | Lockfile drift and inconsistent environments | Single authority (`uv.lock`) with CI enforcement. |
| Big-bang auth hash migration | Can lock users out and break existing credentials | Dual-hash verification rollout with gradual rehash. |

## Stack Patterns by Variant

**If target is single-node local operation (default):**
- Keep current stack as-is with only pinning/hardening adjustments.
- Prefer operational simplicity over distributed-platform features.

**If target shifts to multi-node/team-hosted deployments:**
- Keep FastAPI/Next/Postgres/Redis, then add OTel pipeline and stricter image pinning policy first.
- Re-evaluate queue layer only after measured throughput/SLA pressure.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Next.js `16.x` | Node.js `>=20.9`, TypeScript `>=5.1` | Current frontend (`next 16.2.0`, TS `5.8.3`, Node 20 image) is compatible. |
| RQ `2.6.0` | Redis `>=5` (or Valkey `>=7.2`) | Current Redis `8` runtime is within supported range. |
| FastAPI `0.135.1` | Python `3.12` | Matches backend runtime constraints and Docker base image. |
| PostgreSQL image `18` | `psycopg 3.x`, Alembic/SQLModel stack | Current backend DB drivers are aligned with Postgres 18 runtime. |

## Installation (Current Project Flow)

```bash
# Full local stack (recommended for this repo)
make up-all

# Backend-only dependency sync (authoritative manager)
cd control-panel/backend && uv sync

# Frontend dependencies
cd control-panel/frontend && pnpm install
```

## Migration & Compatibility Risks to Track

1. Auth migration: introduce Argon2 only with dual verification and on-login rehashing.
2. Lockfile authority: enforce one backend lockfile source of truth in CI to prevent drift.
3. Container pinning: create a monthly patch update cadence to avoid stale CVEs.
4. Node runtime alignment: keep frontend on Node 20+ minimum; avoid unplanned major jumps until Cypress/build matrix is validated.

## Sources

- Internal baseline:
  - `.planning/PROJECT.md` (constraints and compatibility requirements) [HIGH]
  - `.planning/codebase/STACK.md` (current stack map) [HIGH]
  - `.planning/codebase/INTEGRATIONS.md` (service boundaries/integrations) [HIGH]
  - `README.md` and `Makefile` (operational lifecycle) [HIGH]
  - `control-panel/backend/pyproject.toml`, `control-panel/frontend/package.json`, `docker/*/Dockerfile` [HIGH]
- Official docs:
  - Next.js installation and v16 upgrade guide (Node/TS compatibility): https://nextjs.org/docs/app/getting-started/installation, https://nextjs.org/docs/app/guides/upgrading/version-16 [HIGH]
  - FastAPI OAuth2/JWT security tutorial (`pwdlib[argon2]` recommendation): https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ [MEDIUM]
  - RQ official docs (Redis compatibility and scheduler model): https://python-rq.org/ [HIGH]
  - Docker best practices (pinning image versions/digests): https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ [HIGH]
  - Docker Compose docs (multi-container lifecycle model): https://docs.docker.com/compose/ [HIGH]
  - PostgreSQL current docs (current major line): https://www.postgresql.org/docs/current/ [HIGH]
  - OpenTelemetry Python getting started (trace/metric/log support): https://opentelemetry.io/docs/languages/python/getting-started/ [MEDIUM]
