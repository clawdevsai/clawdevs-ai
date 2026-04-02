# Technology Stack

**Analysis Date:** 2026-04-02

## Languages

**Primary:**
- Python 3.12 - backend services and API in `control-panel/backend/app/` (version in `control-panel/backend/pyproject.toml`)
- TypeScript/JavaScript - frontend Next.js app in `control-panel/frontend/src/` (dependencies in `control-panel/frontend/package.json`)

**Secondary:**
- Shell - Docker/bootstrap scripts in `docker/base/bootstrap-scripts/`

## Runtime

**Environment:**
- Python >=3.12,<4.0 (backend) in `control-panel/backend/pyproject.toml`
- Node.js runtime (frontend) inferred from `control-panel/frontend/package.json` (version not pinned in repo)

**Package Manager:**
- Poetry (backend) via `control-panel/backend/pyproject.toml`
- pnpm (frontend) via `control-panel/frontend/package.json`
- Lockfile: `control-panel/backend/poetry.lock`, `control-panel/frontend/pnpm-lock.yaml`

## Frameworks

**Core:**
- FastAPI 0.135.1 - backend API framework in `control-panel/backend/pyproject.toml`
- Uvicorn 0.34.0 - ASGI server in `control-panel/backend/pyproject.toml`
- SQLModel 0.0.37 - ORM/data models in `control-panel/backend/pyproject.toml`
- Alembic 1.18.4 - migrations in `control-panel/backend/pyproject.toml` and `control-panel/backend/alembic.ini`
- Next.js 16.2.0 - frontend framework in `control-panel/frontend/package.json`
- React 19.2.4 - UI runtime in `control-panel/frontend/package.json`
- Tailwind CSS 4.2.2 - styling in `control-panel/frontend/package.json`

**Testing:**
- Pytest 8.4.0 + pytest-asyncio 0.25.3 - backend tests in `control-panel/backend/pyproject.toml`
- pytest-cov 6.1.0 - backend coverage in `control-panel/backend/pyproject.toml`
- Cypress ^15.13.0 - frontend e2e in `control-panel/frontend/package.json`

**Build/Dev:**
- TypeScript 5.8.3 - type-checking in `control-panel/frontend/package.json`
- ESLint 9.39.4 + eslint-config-next 16.2.0 - linting in `control-panel/frontend/package.json`
- PostCSS 8.5.3 - CSS pipeline in `control-panel/frontend/package.json`
- Orval 8.5.3 - OpenAPI client generation in `control-panel/frontend/package.json` and `control-panel/frontend/orval.config.ts`

## Key Dependencies

**Critical:**
- asyncpg 0.30.0 + psycopg[binary] 3.2.4 - Postgres drivers in `control-panel/backend/pyproject.toml`
- pgvector >=0.3.0 - vector extension support in `control-panel/backend/pyproject.toml`
- redis[hiredis] >=6.0.0 - Redis client in `control-panel/backend/pyproject.toml`
- rq 2.6.0 + rq-scheduler 0.14.0 - background job queue in `control-panel/backend/pyproject.toml`
- sse-starlette 2.3.6 - SSE streaming in `control-panel/backend/pyproject.toml`
- kubernetes 32.0.1 - K8s client used in `control-panel/backend/app/services/container_client.py`

**Infrastructure:**
- passlib[bcrypt] 1.7.4 + bcrypt 4.0.1 - password hashing in `control-panel/backend/pyproject.toml` and `control-panel/backend/app/core/auth.py`
- pyjwt[crypto] >=2.10.1 - JWT auth in `control-panel/backend/pyproject.toml` and `control-panel/backend/app/core/auth.py`
- httpx 0.28.1 + aiohttp >=3.9.1 - outbound HTTP clients in `control-panel/backend/pyproject.toml`
- axios 1.13.5 - frontend HTTP client in `control-panel/frontend/package.json`
- @tanstack/react-query 5.94.5 - client caching in `control-panel/frontend/package.json`

## Configuration

**Environment:**
- Backend settings via Pydantic BaseSettings with `env_prefix` = `PANEL_` and `env_file` = `.env` in `control-panel/backend/app/core/config.py`
- Root `.env` and `.env.example` present in repo (contents not inspected): `.env`, `.env.example`
- Frontend API routing via `BACKEND_URL`, `NEXT_PUBLIC_API_URL`, `API_INTERNAL_URL` in `control-panel/frontend/next.config.ts` and `control-panel/frontend/src/lib/api-base-url.ts`

**Build:**
- Next.js configuration in `control-panel/frontend/next.config.ts`
- OpenAPI client generation in `control-panel/frontend/orval.config.ts`
- Alembic config in `control-panel/backend/alembic.ini`

## Platform Requirements

**Development:**
- Docker bootstrap and OpenClaw gateway scripts in `docker/base/bootstrap-scripts/`
- OpenClaw config and agent definitions in `docker/base/openclaw-config/`

**Production:**
- Not detected

---

*Stack analysis: 2026-04-02*
